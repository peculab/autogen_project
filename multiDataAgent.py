import os
import asyncio
import pandas as pd
import gradio as gr
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from your_script import process_chunk, TextMentionTermination

load_dotenv()

async def run_analysis(csv_file_path, chunk_size):
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    model_client_8b = OpenAIChatCompletionClient("gemini-1.5-flash-8b", gemini_api_key)
    model_client_flash = OpenAIChatCompletionClient("gemini-2.0-flash", gemini_api_key)
    termination_condition = TextMentionTermination("exit")

    chunks = list(pd.read_csv(csv_file_path, chunksize=chunk_size))
    total_records = sum(chunk.shape[0] for chunk in chunks)

    tasks = [
        process_chunk(chunk, idx * chunk_size, total_records, model_client_8b, model_client_flash, termination_condition)
        for idx, chunk in enumerate(chunks)
    ]

    results = []
    for coro in asyncio.as_completed(tasks):
        chunk_messages = await coro
        for msg in chunk_messages:
            phase = msg['phase']
            source = msg['source']
            batch_range = f"{msg['batch_start']}-{msg['batch_end']}"
            content = msg['content']
            yield f"[{phase.upper()}][{batch_range}][{source}] {content}"

async def analyze_file(file_obj):
    csv_file_path = file_obj.name
    chunk_size = 100  # 自行調整
    result = ""
    async for update in run_analysis(csv_file_path, chunk_size):
        result += update + "\n\n"
        yield result

iface = gr.Interface(
    analyze_file,
    inputs=gr.File(label="上傳CSV檔案"),
    outputs=gr.Textbox(label="即時分析結果", lines=25, max_lines=50),
    title="寶寶照護即時分析系統",
    allow_flagging=False,
)

iface.launch()
