import os
import asyncio
import pandas as pd
from dotenv import load_dotenv
import gradio as gr

# 根據你的專案結構調整下列 import
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.agents.web_surfer import MultimodalWebSurfer

load_dotenv()

async def process_chunk(chunk, start_idx, total_records, model_client_8b, model_client_flash, termination_condition):
    # ------------------ 第一階段：數據分析 ------------------
    chunk_data = chunk.to_dict(orient='records')
    phase1_prompt = (
        f"目前正在處理第 {start_idx} 至 {start_idx + len(chunk) - 1} 筆資料（共 {total_records} 筆）。\n"
        f"以下為該批次資料:\n{chunk_data}\n\n"
        "請根據以上資料進行詳細分析，識別出寶寶的日常行為特徵與照護需求，並整理出關鍵數據，作為後續寶寶照護建議的參考。\n"
        "請提供一份完整的分析結果摘要。"
    )
    
    data_agent_8b = AssistantAgent("data_agent", model_client_8b)
    web_surfer_8b = MultimodalWebSurfer("web_surfer", model_client_8b)
    assistant_8b = AssistantAgent("assistant", model_client_8b)
    user_proxy = UserProxyAgent("user_proxy")
    
    team_phase1 = RoundRobinGroupChat(
        [data_agent_8b, web_surfer_8b, assistant_8b, user_proxy],
        termination_condition=termination_condition
    )
    
    phase1_messages = []
    async for event in team_phase1.run_stream(task=phase1_prompt):
        if isinstance(event, TextMessage):
            print(f"[Phase1][{event.source}] => {event.content}\n")
            phase1_messages.append({
                "phase": "phase1",
                "batch_start": start_idx,
                "batch_end": start_idx + len(chunk) - 1,
                "source": event.source,
                "content": event.content,
                "prompt_tokens": event.models_usage.prompt_tokens if event.models_usage else None,
                "completion_tokens": event.models_usage.completion_tokens if event.models_usage else None,
            })
    analysis_summary = "\n".join(msg["content"] for msg in phase1_messages)
    
    # ------------------ 第二階段：整合寶寶照護建議 ------------------
    phase2_prompt = (
        "根據以下先前的分析結果，請整合並產出一份完整且具參考價值的寶寶照護建議：\n\n"
        f"{analysis_summary}\n\n"
        "請利用外部網站搜尋功能（由 MultimodalWebSurfer 執行），搜尋最新的寶寶照護建議資訊（例如餵食、睡眠、尿布更換等），"
        "並將搜尋結果整合到最終回覆中。請提供具體建議與相關參考資訊。"
    )
    
    assistant_flash = AssistantAgent("assistant", model_client_flash)
    web_surfer_flash = MultimodalWebSurfer("web_surfer", model_client_flash)
    user_proxy_flash = UserProxyAgent("user_proxy")
    
    team_phase2 = RoundRobinGroupChat(
        [assistant_flash, web_surfer_flash, user_proxy_flash],
        termination_condition=termination_condition
    )
    
    phase2_messages = []
    async for event in team_phase2.run_stream(task=phase2_prompt):
        if isinstance(event, TextMessage):
            print(f"[Phase2][{event.source}] => {event.content}\n")
            phase2_messages.append({
                "phase": "phase2",
                "batch_start": start_idx,
                "batch_end": start_idx + len(chunk) - 1,
                "source": event.source,
                "content": event.content,
                "prompt_tokens": event.models_usage.prompt_tokens if event.models_usage else None,
                "completion_tokens": event.models_usage.completion_tokens if event.models_usage else None,
            })
    
    return phase1_messages + phase2_messages

async def process_agent(uploaded_file):
    csv_file_path = uploaded_file.name
    chunk_size = 1000
    chunks = list(pd.read_csv(csv_file_path, chunksize=chunk_size))
    total_records = sum(chunk.shape[0] for chunk in chunks)
    
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    model_client_8b = OpenAIChatCompletionClient(
        model="gemini-1.5-flash-8b",
        api_key=gemini_api_key,
    )
    model_client_flash = OpenAIChatCompletionClient(
        model="gemini-2.0-flash",
        api_key=gemini_api_key,
    )
    termination_condition = TextMentionTermination("exit")
    
    all_messages = []
    progress_log = ""
    
    for idx, chunk in enumerate(chunks):
        start_idx = idx * chunk_size
        progress_log += f"處理批次 {idx+1} / {len(chunks)} 中...\n"
        yield progress_log, None
        chunk_messages = await process_chunk(chunk, start_idx, total_records, model_client_8b, model_client_flash, termination_condition)
        all_messages.extend(chunk_messages)
        progress_log += f"批次 {idx+1} 完成。\n"
        yield progress_log, None
    
    df_log = pd.DataFrame(all_messages)
    output_file = "all_conversation_log.csv"
    df_log.to_csv(output_file, index=False, encoding="utf-8-sig")
    progress_log += "所有批次處理完成，CSV 檔案已產生。\n"
    yield progress_log, output_file

async def gradio_run_agent(uploaded_file):
    async for progress, file_path in process_agent(uploaded_file):
        yield progress, file_path

def main():
    with gr.Blocks() as demo:
        gr.Markdown("## 多代理人 CSV 處理與寶寶照護建議產出")
        gr.Markdown("請上傳 CSV 檔案，系統將依據每批次資料進行分析，並整合產出寶寶照護建議。")
        
        file_input = gr.File(label="上傳 CSV 檔案", file_count="single")
        progress_text = gr.Textbox(label="處理進度", lines=10)
        download_file = gr.File(label="下載結果 CSV", interactive=False)
        run_button = gr.Button("開始處理")
        
        # 移除 stream=True 參數，或根據需要更新 gradio 套件
        run_button.click(
            fn=gradio_run_agent,
            inputs=file_input,
            outputs=[progress_text, download_file]
        )
    
    demo.launch()

if __name__ == '__main__':
    main()
