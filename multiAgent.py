"""Introductory multi-agent collaboration example.

Agents collaborate to research a topic and produce a short synthesis.
This example is appropriate for an introductory lesson on agent roles,
turn-taking, and web-assisted reasoning.
"""

import asyncio
import os

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-8b")

    if not gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not set. Please update your .env file.")

    model_client = OpenAIChatCompletionClient(
        model=model_name,
        api_key=gemini_api_key,
    )

    assistant = AssistantAgent("assistant", model_client)
    web_surfer = MultimodalWebSurfer("web_surfer", model_client)
    user_proxy = UserProxyAgent("user_proxy")

    termination_condition = TextMentionTermination("exit")

    team = RoundRobinGroupChat(
        [web_surfer, assistant, user_proxy],
        termination_condition=termination_condition,
    )

    task = (
        "Research recent information about Gemini model capabilities, "
        "then write a concise summary for a technical practitioner. "
        "Type 'exit' when the task is complete."
    )

    await Console(team.run_stream(task=task))


if __name__ == "__main__":
    asyncio.run(main())
