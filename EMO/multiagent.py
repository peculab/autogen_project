import os
import asyncio
import json
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

load_dotenv()

async def process_user_diary(socketio, user_id, user_entries):
    model_client = OpenAIChatCompletionClient(
        model="gemini-2.0-flash",
        api_key=os.getenv("GEMINI_API_KEY"),
    )

    # 只取前 5 筆資料，並將 Timestamp 轉為字串避免 JSON 序列化問題
    records = user_entries.to_dict(orient='records')
    if len(records) > 5:
        prompt_records = json.dumps(records[:5], ensure_ascii=False, indent=2, default=str) + "\n... (以下省略)"
    else:
        prompt_records = json.dumps(records, ensure_ascii=False, indent=2, default=str)
        
    # 更新 prompt，要求 AI 根據日記產生全新的正向建議，
    # 並在回覆最後直接輸出最終建議，格式必須以『最終建議：』開頭
    prompt = (
        f"目前正在處理用戶 {user_id} 的日記，共 {len(user_entries)} 則。\n"
        f"日記內容（僅顯示前 5 筆）：\n{prompt_records}\n\n"
        "請仔細分析上述日記，找出用戶的情緒與思考模式，並根據你的分析生成一段全新的正向心情建議，內容必須包含：\n"
        "1. 情緒與思考模式的詳細分析\n"
        "2. 實際可行的行動方案建議\n"
        "3. AI 教練如何提供個性化互動建議\n\n"
        "請注意：請僅生成全新內容，不要重複上述提示。請在回覆最後直接輸出最終建議，格式必須以『最終建議：』開頭，後面跟上你的建議內容。\n"
        "例如：\n"
        "最終建議：根據分析，建議您每天進行10分鐘冥想，並根據心情記錄調整作息，同時與 AI 教練定期討論情緒管理策略。\n\n"
        "請務必遵守上述要求。"
    )

    # 建立合法的 agent 名稱及顯示用對照字典
    analysis_agent = AssistantAgent("analysis_expert", model_client)
    coaching_agent = AssistantAgent("ai_coach", model_client)
    display_names = {
         "analysis_expert": "分析專家",
         "ai_coach": "AI 教練"
    }

    team = RoundRobinGroupChat([analysis_agent, coaching_agent])
    
    final_recommendation = None

    try:
        async for event in team.run_stream(task=prompt):
            if isinstance(event, TextMessage):
                display_name = display_names.get(event.source, event.source)
                message_text = f"🤖 [{display_name}]：{event.content}"
                # 若訊息過長，僅截取前 500 個字顯示
                if len(message_text) > 500:
                    message_text = message_text[:500] + " ... (內容過長)"
                socketio.emit('update', {'message': message_text})
                
                # 如果訊息中包含「最終建議：」則從中提取建議內容並更新【建議】區塊
                if "最終建議：" in event.content:
                    final_recommendation = event.content.split("最終建議：")[-1].strip()
                    socketio.emit('suggestions', {'suggestions': final_recommendation})
    except asyncio.exceptions.CancelledError:
        # 若因取消操作而發生 CancelledError，忽略即可
        pass

async def run_multiagent_analysis(socketio, user_id, user_entries):
    await process_user_diary(socketio, user_id, user_entries)
