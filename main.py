"""Minimal Gemini-compatible chat completion example.

This file is intended as a beginner-friendly starting point for the course
"Agentic AI Engineering: Building Real-World LLM Agent Systems".
"""

import asyncio
import os

from autogen_core.models import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-8b")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set. Please update your .env file.")

    model_client = OpenAIChatCompletionClient(
        model=model_name,
        api_key=api_key,
    )

    response = await model_client.create(
        [UserMessage(content="What is the capital of France?", source="user")]
    )
    print("Model response:", response)


if __name__ == "__main__":
    asyncio.run(main())
