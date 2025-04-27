import os
import asyncio
import json
import threading
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
from google import genai
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage
from EMOwithSnow import generate_mood_trend_plot

# ✅ 初始化 Flask 與 SocketIO
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
socketio = SocketIO(app, async_mode='threading')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ✅ 載入 .env 並初始化 Gemini
dotenv_path = find_dotenv()
#print(f"✅ 目前使用的 .env 路徑: {dotenv_path}")
load_dotenv(dotenv_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
#print(GEMINI_API_KEY)

# ✅ 建立 Gemini 客戶端與模型
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# ✅ 封裝 autogen client
class GeminiChatCompletionClient:
    def __init__(self, model="gemini-1.5-flash-8b"):
        self.model = model
        self.model_info = {"vision": False}

    async def create(self, messages, **kwargs):
        parts = []
        for m in messages:
            if hasattr(m, 'content'):
                parts.append(str(m.content))
            elif isinstance(m, dict) and 'content' in m:
                parts.append(str(m['content']))
        content = "\n".join(parts)
        response = client.models.generate_content(
            model=self.model,
            contents=content
        )
        return type("Response", (), {
            "text": response.text,
            "content": response.text,
            "usage": {
                "prompt_tokens": {"value": 0},
                "completion_tokens": {"value": 0}
            }
        })

model_client = GeminiChatCompletionClient()

# ✅ 多 Agent 分析（保留原來程式碼）
from multiagent import run_multiagent_analysis

# ✅ Flask 路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        socketio.emit('update', {'message': '🟢 檔案上傳成功，開始分析中...'})
        threading.Thread(target=background_task, args=(file_path,)).start()
        return 'File uploaded and processing started.', 200

def background_task(file_path):
    try:
        df = pd.read_csv(file_path)
        user_id = os.path.splitext(os.path.basename(file_path))[0]
        plot_path = generate_mood_trend_plot(user_id, df)
        socketio.emit('plot_generated', {'plot_url': '/' + plot_path})
        asyncio.run(run_multiagent_analysis(socketio, user_id, df))
    except Exception as e:
        socketio.emit('update', {'message': f"❌ 分析過程出現錯誤: {str(e)}"})

# ✅ Gemini 聊天區支援即時回應
@socketio.on('chat_message')
def handle_user_chat(data):
    user_message = data.get('message', '').strip()
    if not user_message:
        return
    
    socketio.emit('ai_reply', {'message': '💬 Gemini 正在思考中，請稍候...'})

    def chat_reply():
        try:
            response = client.models.generate_content(
                model="gemini-2.5-pro-exp-03-25",
                contents=f"你是心理諮商師，要用正體中文來回應，以下的對話內容：{user_message}",
            )
            
            reply = response.text.strip()
            #print("🔁 Gemini 即時回應：", reply)
            socketio.emit('ai_reply', {'message': reply})
        except Exception as e:
            #print("❌ 發生錯誤：", str(e))
            socketio.emit('ai_reply', {'message': f"⚠️ 發生錯誤：{str(e)}"})

    threading.Thread(target=chat_reply).start()

if __name__ == '__main__':
    socketio.run(app, debug=True)
