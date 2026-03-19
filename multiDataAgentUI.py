"""Gradio interface for CSV-based agent analysis.

This demo is useful for discussing lightweight deployment patterns in an
agentic AI course.
"""

import asyncio
import os
from pathlib import Path

import gradio as gr
import pandas as pd
from dotenv import load_dotenv

from multiDataAgent import run_analysis

load_dotenv()

conversation_log: list[dict[str, str]] = []


async def process_file(file_obj, chat_history):
    global conversation_log
    conversation_log.clear()
    chat_history = chat_history or []

    if not file_obj or not hasattr(file_obj, "name"):
        chat_history.append({"role": "system", "content": "Unable to read the uploaded file."})
        yield chat_history, None
        return

    file_path = file_obj.name
    if not Path(file_path).exists():
        chat_history.append({"role": "system", "content": f"File not found: {file_path}"})
        yield chat_history, None
        return

    chat_history.append(
        {"role": "system", "content": "CSV file loaded. Starting chunk-level analysis..."}
    )
    yield chat_history, None

    async for update in run_analysis(file_path, chunk_size=1000):
        chat_history.append({"role": "assistant", "content": update})
        conversation_log.append({"source": "assistant", "content": update})
        yield chat_history, None

    df_log = pd.DataFrame(conversation_log)
    log_file = "conversation_log.csv"
    df_log.to_csv(log_file, index=False, encoding="utf-8-sig")

    chat_history.append({"role": "system", "content": "Analysis complete."})
    yield chat_history, log_file


with gr.Blocks() as demo:
    gr.Markdown("### Agentic AI CSV Analysis Demo")

    file_input = gr.File(label="Upload CSV")
    chat_display = gr.Chatbot(label="Streaming Analysis", type="messages")
    download_log = gr.File(label="Download Conversation Log")
    start_btn = gr.Button("Start Analysis")

    start_btn.click(
        fn=process_file,
        inputs=[file_input, chat_display],
        outputs=[chat_display, download_log],
    )


demo.queue().launch()
