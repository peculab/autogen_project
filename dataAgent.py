"""Chunk-based CSV analysis with multiple agents.

This script demonstrates how to process structured data in chunks, ask
multiple agents to collaborate on analysis, and persist the conversation log.
It is intended as a workflow automation example for teaching.
"""

import asyncio
import os
from typing import Any

import pandas as pd
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

load_dotenv()


def _build_prompt(chunk: pd.DataFrame, start_idx: int, total_records: int) -> str:
    chunk_data = chunk.to_dict(orient="records")
    end_idx = start_idx + len(chunk) - 1
    return (
        f"You are analyzing records {start_idx} to {end_idx} out of {total_records}.\n"
        f"Batch data:\n{chunk_data}\n\n"
        "Work together to do the following:\n"
        "1. Identify relevant patterns in the batch.\n"
        "2. Highlight practical insights supported by the data.\n"
        "3. Use web search when helpful to add recent external context.\n"
        "4. Provide a concise final recommendation for a human operator."
    )


async def process_chunk(
    chunk: pd.DataFrame,
    start_idx: int,
    total_records: int,
    model_client: OpenAIChatCompletionClient,
    termination_condition: TextMentionTermination,
) -> list[dict[str, Any]]:
    prompt = _build_prompt(chunk, start_idx, total_records)

    local_data_agent = AssistantAgent("data_agent", model_client)
    local_web_surfer = MultimodalWebSurfer("web_surfer", model_client)
    local_assistant = AssistantAgent("assistant", model_client)
    local_user_proxy = UserProxyAgent("user_proxy")

    local_team = RoundRobinGroupChat(
        [local_data_agent, local_web_surfer, local_assistant, local_user_proxy],
        termination_condition=termination_condition,
    )

    messages: list[dict[str, Any]] = []
    async for event in local_team.run_stream(task=prompt):
        if isinstance(event, TextMessage):
            print(f"[{event.source}] => {event.content}\n")
            messages.append(
                {
                    "batch_start": start_idx,
                    "batch_end": start_idx + len(chunk) - 1,
                    "source": event.source,
                    "content": event.content,
                    "type": event.type,
                    "prompt_tokens": event.models_usage.prompt_tokens if event.models_usage else None,
                    "completion_tokens": event.models_usage.completion_tokens if event.models_usage else None,
                }
            )
    return messages


async def main() -> None:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    csv_file_path = os.getenv("CSV_FILE_PATH", "cuboai_baby_diary.csv")
    chunk_size = int(os.getenv("CSV_CHUNK_SIZE", "1000"))

    if not gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not set. Please update your .env file.")

    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")

    model_client = OpenAIChatCompletionClient(
        model=model_name,
        api_key=gemini_api_key,
    )

    termination_condition = TextMentionTermination("exit")
    chunks = list(pd.read_csv(csv_file_path, chunksize=chunk_size))
    total_records = sum(chunk.shape[0] for chunk in chunks)

    tasks = [
        process_chunk(
            chunk,
            idx * chunk_size,
            total_records,
            model_client,
            termination_condition,
        )
        for idx, chunk in enumerate(chunks)
    ]

    results = await asyncio.gather(*tasks)
    all_messages = [msg for batch in results for msg in batch]

    df_log = pd.DataFrame(all_messages)
    output_file = "all_conversation_log.csv"
    df_log.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"Saved conversation log to {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
