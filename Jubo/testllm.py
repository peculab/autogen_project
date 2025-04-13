import os
from dotenv import find_dotenv, load_dotenv
from google import genai

load_dotenv(override=True)

dotenv_path = find_dotenv()
print(f"✅ 目前使用的 .env 路徑: {dotenv_path}")

load_dotenv(dotenv_path)
print(os.getenv('GEMINI_API_KEY'))

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
response = client.models.generate_content(
        model="gemini-2.5-pro-preview-03-25",
        contents="給我一段50字的故事",
)

print(response.text)