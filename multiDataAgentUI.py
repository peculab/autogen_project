import os
import pandas as pd
import gradio as gr
import asyncio
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core import CancellationToken

load_dotenv()

conversation_log = []

# 讀取環境變數中的 API Key
api_key = os.getenv("GEMINI_API_KEY")
model_client = OpenAIChatCompletionClient(model="gemini-1.5-flash-8b", api_key=api_key)

# CSV 摘要函式
def summarize_csv_in_chunks(file_path, chunk_size=1000, max_chunks=5):
    summaries = []
    try:
        for i, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size)):
            if i >= max_chunks:
                break
            summary = f"【區塊 {i+1}】\n前3行資料：\n{chunk.head(3).to_csv(index=False)}\n區塊行數：{chunk.shape[0]}"
            summaries.append(summary)
    except Exception as e:
        return f"讀取或摘要檔案時發生錯誤：{e}"
    return "\n".join(summaries)

async def process_file(file_obj, chat_history):
    global conversation_log
    conversation_log.clear()

    if hasattr(file_obj, "name"):
        file_path = file_obj.name
    else:
        chat_history.append({"role": "system", "content": "無法取得上傳檔案的路徑"})
        yield chat_history, None
        return

    chat_history.append({"role": "system", "content": "CSV 資料已讀取完畢，開始進行摘要及分析..."})
    yield chat_history, None

    # Debug 訊息
    print("已成功讀取 CSV 檔案，開始處理每個區塊...")

    for i, chunk in enumerate(pd.read_csv(file_path, chunksize=1000)):
        summary_text = f"區塊 {i+1} 摘要:\n{chunk.head(3).to_csv(index=False)}\n區塊行數：{chunk.shape[0]}"
        
        # 確保 AssistantAgent 有執行
        print(f"開始分析區塊 {i+1} ...")

        analysis_agent = AssistantAgent(
            name=f"analysis_agent_{i+1}",
            model_client=model_client
        )

        chat_history.append({"role": "system", "content": summary_text})
        yield chat_history, None  # **顯示 CSV 摘要，確保 UI 會即時更新**

        # **確保 run_stream() 產生的 AI 回應能即時顯示**
        cancellation_token = CancellationToken()
        async for event in analysis_agent.run_stream(
            task=f"請根據以下摘要進行分析，識別寶寶日常行為特徵與照護需求，整理關鍵數據：\n{summary_text}",
            cancellation_token=cancellation_token  
        ):
            if isinstance(event, TextMessage):
                ai_response = event.content
                chat_history.append({"role": "assistant", "content": ai_response})
                conversation_log.append({"source": "assistant", "content": ai_response})
                
                print(f"💬 Assistant 回應（區塊 {i+1}）: {ai_response}")  # Debug
                yield chat_history, None  # **確保 UI 會即時更新 AI 回應**

    # **分析完成，儲存對話紀錄**
    df_log = pd.DataFrame(conversation_log)
    log_file = "conversation_log.csv"
    df_log.to_csv(log_file, index=False, encoding="utf-8-sig")

    chat_history.append({"role": "system", "content": "🎯 分析完成！"})
    print("🎯 所有區塊分析完成！")
    yield chat_history, log_file

def send_user_msg(msg, chat_history):
    chat_history.append({"role": "user", "content": msg})
    return chat_history, ""

with gr.Blocks() as demo:
    gr.Markdown("### AI 寶寶照護分析系統")

    file_input = gr.File(label="上傳 CSV")
    chat_display = gr.Chatbot(label="對話紀錄", type="messages")
    download_log = gr.File(label="下載對話記錄")

    start_btn = gr.Button("開始分析")

    start_btn.click(
        fn=process_file,
        inputs=[file_input, chat_display],
        outputs=[chat_display, download_log]
    )
demo.queue().launch()
