import os
from dotenv import load_dotenv
import asyncio

# 載入 .env 檔案中的環境變數
load_dotenv()

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.agents.web_surfer import MultimodalWebSurfer

async def main():
    # 從 .env 讀取 Gemini API 金鑰
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    
    # 使用 Gemini API，指定 model 為 "gemini-1.5-flash-8b"
    model_client = OpenAIChatCompletionClient(
        model="gemini-1.5-flash-8b",
        api_key=gemini_api_key,
    )
    
    # 建立各代理人
    assistant = AssistantAgent("assistant", model_client)
    web_surfer = MultimodalWebSurfer("web_surfer", model_client)
    user_proxy = UserProxyAgent("user_proxy")
    
    # 當對話中出現 "exit" 時即終止對話
    termination_condition = TextMentionTermination("exit")
    
    # 建立一個循環團隊，讓各代理人依序參與討論
    team = RoundRobinGroupChat(
        [web_surfer, assistant, user_proxy],
        termination_condition=termination_condition
    )
    
    # 啟動團隊對話，任務是「搜尋 Gemini 的相關資訊，並撰寫一份簡短摘要」
    await Console(team.run_stream(task="請搜尋 Gemini 的相關資訊，並撰寫一份簡短摘要。"))

if __name__ == '__main__':
    asyncio.run(main())