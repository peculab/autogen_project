import os
import re
import json
import asyncio
import sys
import pandas as pd
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

# 如果有使用終止條件，可自行定義，否則可移除
class TextMentionTermination:
    def __init__(self, termination_text):
        self.termination_text = termination_text

    def check(self, text):
        return self.termination_text in text

load_dotenv()

# 定義評分項目
ITEMS = [
    "引導",
    "評估(口語、跟讀的內容有關)",
    "評估(非口語、寶寶自發性動作、跟讀的內容有關)",
    "延伸討論",
    "複述",
    "開放式問題",
    "填空",
    "回想",
    "人事時地物問句",
    "連結生活經驗",
    "備註"
]

def parse_json_response(response_text):
    """
    解析 Gemini API 回傳的 JSON 格式結果，
    預期回傳內容為有效 JSON，鍵為 ITEMS 中各項，
    值為 "1" 或空字串。若缺少項目則自動補空。
    """
    try:
        result = json.loads(response_text)
        for item in ITEMS:
            if item not in result:
                result[item] = ""
        return result
    except Exception as e:
        print(f"解析 JSON 失敗：{e}")
        return {item: "" for item in ITEMS}

async def process_chunk_score(chunk, start_idx, total_records, model_client_8b, model_client_flash, termination_condition):
    evaluation_results = []
    dialogues = chunk["dialogue"].tolist()
    
    for dialogue in dialogues:
        # 系統提示：要求對每一句話依據編碼規則評估是否觸及到各項目，
        # 若觸及則標記為 1，否則留空，回覆必須為有效 JSON 格式。
        messages = [
            {"role": "system", "content": (
                "你是一位親子對話分析專家，請根據以下編碼規則評估家長唸故事書時的每一句話，"
                "判斷是否觸及下列各項：\n" +
                "\n".join(ITEMS) +
                "\n\n請依據評估結果，對每個項目：若觸及則標記為 1，否則留空，"
                "請僅以有效 JSON 格式回覆，鍵為項目名稱，值為 '1' 或空字串。"
            )},
            {"role": "user", "content": dialogue}
        ]
        
        try:
            response = await model_client_8b.chat(messages=messages)
            response_text = response["choices"][0]["message"]["content"]
            eval_dict = parse_json_response(response_text)
        except Exception as e:
            print(f"API 呼叫失敗，錯誤：{e}")
            eval_dict = {item: "" for item in ITEMS}
        
        evaluation_results.append(eval_dict)
    
    # 將每一句話的評估結果展開成多個欄位，並與原始逐字稿合併
    eval_df = pd.DataFrame(evaluation_results)
    chunk = chunk.rename(columns={"dialogue": "對話內容"})
    combined = pd.concat([chunk, eval_df], axis=1)
    return combined

async def run_analysis(csv_file_path, chunk_size):
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    model_client_8b = OpenAIChatCompletionClient("gemini-1.5-flash-8b", gemini_api_key)
    model_client_flash = OpenAIChatCompletionClient("gemini-2.0-flash", gemini_api_key)
    termination_condition = TextMentionTermination("exit")

    chunks = list(pd.read_csv(csv_file_path, chunksize=chunk_size))
    total_records = sum(chunk.shape[0] for chunk in chunks)

    tasks = [
        process_chunk_score(chunk, idx * chunk_size, total_records, model_client_8b, model_client_flash, termination_condition)
        for idx, chunk in enumerate(chunks)
    ]
    
    processed_chunks = await asyncio.gather(*tasks)
    final_df = pd.concat(processed_chunks, ignore_index=True)
    
    output_file = "113.csv"
    final_df.to_csv(output_file, index=False, encoding="utf-8-sig")
    return f"分數表已生成：{output_file}"

async def analyze_file(csv_file_path):
    chunk_size = 100  # 可根據檔案大小調整
    result = await run_analysis(csv_file_path, chunk_size)
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python RDai.py <path_to_csv>")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    result = asyncio.run(analyze_file(csv_file_path))
    print(result)

if __name__ == "__main__":
    main()