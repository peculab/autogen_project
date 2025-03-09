import os
import asyncio
import pandas as pd
from dotenv import load_dotenv

# 根據你的專案結構調整下列 import
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.agents.web_surfer import MultimodalWebSurfer

load_dotenv()

async def process_chunk(chunk, start_idx, total_records, model_client_8b, model_client_flash, termination_condition):
    """
    處理單一批次資料，分為兩個階段：
    
    第一階段 (8b 模型)：  
      - 將該批次資料轉成 dict 格式  
      - 組出提示，要求各代理人根據資料進行詳細分析，識別寶寶的日常行為特徵與照護需求，並整理出關鍵數據（分析摘要）
    
    第二階段 (flash 2.0 模型)：  
      - 以第一階段分析結果為參考，請求代理人（assistant 搭配 flash 2.0 模型）結合 MultimodalWebSurfer 的外部網站搜尋功能，
        搜尋最新寶寶照護建議資訊（例如餵食、睡眠、尿布更換等），整合後產生完整建議
    最後將兩階段的所有回覆訊息整合返回。
    """
    # ------------------ 第一階段：分析數據 ------------------
    chunk_data = chunk.to_dict(orient='records')
    phase1_prompt = (
        f"目前正在處理第 {start_idx} 至 {start_idx + len(chunk) - 1} 筆資料（共 {total_records} 筆）。\n"
        f"以下為該批次資料:\n{chunk_data}\n\n"
        "請根據以上資料進行詳細分析，識別出寶寶的日常行為特徵與照護需求，並整理出關鍵數據，作為後續寶寶照護建議的參考。\n"
        "請提供一份完整的分析結果摘要。"
    )
    
    # 第一階段使用 8b 模型建立代理人（全部皆以 8b 模型執行）
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
    # 將第一階段回覆內容合併成分析摘要（這裡以所有回覆內容串接）
    analysis_summary = "\n".join(msg["content"] for msg in phase1_messages)
    
    # ------------------ 第二階段：整合照護建議 ------------------
    phase2_prompt = (
        "根據以下先前的分析結果，請整合並產出一份完整且具參考價值的寶寶照護建議：\n\n"
        f"{analysis_summary}\n\n"
        "請利用外部網站搜尋功能（由 MultimodalWebSurfer 執行），搜尋最新的寶寶照護建議資訊（例如餵食、睡眠、尿布更換等），"
        "並將搜尋結果整合到最終回覆中。請提供具體建議與相關參考資訊。"
    )
    
    # 第二階段使用 flash 2.0 模型建立代理人（assistant 及 web_surfer 採用 flash 模型）
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
    
    # 回傳兩階段的所有訊息
    return phase1_messages + phase2_messages

async def main():
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        print("請檢查 .env 檔案中的 GEMINI_API_KEY。")
        return

    # 建立兩個不同的模型用戶端
    # 第一階段採用 8b 模型
    model_client_8b = OpenAIChatCompletionClient(
        model="gemini-1.5-flash-8b",
        api_key=gemini_api_key,
    )
    # 第二階段採用 flash 2.0 模型
    model_client_flash = OpenAIChatCompletionClient(
        model="gemini-2.0-flash",
        api_key=gemini_api_key,
    )
    
    termination_condition = TextMentionTermination("exit")
    
    # 以 chunksize 方式讀取 CSV 檔案
    csv_file_path = "cuboai_baby_diary.csv"
    chunk_size = 1000
    chunks = list(pd.read_csv(csv_file_path, chunksize=chunk_size))
    total_records = sum(chunk.shape[0] for chunk in chunks)
    
    # 同時處理所有批次資料（利用 asyncio.gather 並行執行）
    tasks = [
        process_chunk(chunk, idx * chunk_size, total_records, model_client_8b, model_client_flash, termination_condition)
        for idx, chunk in enumerate(chunks)
    ]
    
    results = await asyncio.gather(*tasks)
    # 將所有批次的訊息平坦化成一個清單
    all_messages = [msg for batch in results for msg in batch]
    
    # 整理對話紀錄為 DataFrame 並存成 CSV
    df_log = pd.DataFrame(all_messages)
    output_file = "all_conversation_log.csv"
    df_log.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"已將所有對話紀錄輸出為 {output_file}")

if __name__ == '__main__':
    asyncio.run(main())