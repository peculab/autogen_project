"""Streaming chunk-level CSV analysis pipeline.

This file provides a more course-ready version of the original example.
It yields intermediate analysis updates and finishes with a final synthesis.
"""

import asyncio
import os
from typing import AsyncGenerator

import pandas as pd
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

from dataAgent import process_chunk

load_dotenv()


async def run_analysis(csv_file_path: str, chunk_size: int = 100) -> AsyncGenerator[str, None]:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-8b")

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
            chunk=chunk,
            start_idx=idx * chunk_size,
            total_records=total_records,
            model_client=model_client,
            termination_condition=termination_condition,
        )
        for idx, chunk in enumerate(chunks)
    ]

    for coro in asyncio.as_completed(tasks):
        chunk_messages = await coro
        for msg in chunk_messages:
            batch_range = f"{msg['batch_start']}-{msg['batch_end']}"
            yield f"[{batch_range}][{msg['source']}] {msg['content']}"


async def collect_analysis(csv_file_path: str, chunk_size: int = 100) -> str:
    lines: list[str] = []
    async for update in run_analysis(csv_file_path, chunk_size):
        lines.append(update)
    return "\n\n".join(lines)


if __name__ == "__main__":
    target_file = os.getenv("CSV_FILE_PATH", "cuboai_baby_diary.csv")
    print(asyncio.run(collect_analysis(target_file)))
