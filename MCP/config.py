# config.py

import os
from dotenv import load_dotenv, find_dotenv

# ✅ 載入 .env 環境變數
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# ✅ 預設模型設定
DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'gemini-1.5-flash-8b')  
MODEL_PROVIDER = os.getenv('MODEL_PROVIDER', 'gemini')  
# 'gemini' (Google) / 'openai' (OpenAI) / 'hf' (HuggingFace)

# ✅ API KEY 設定
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
HF_API_KEY = os.getenv('HF_API_KEY', '')

# ✅ 其他可擴充設定
DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
