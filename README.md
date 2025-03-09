# AutoGen Gemini 範例

- **單一查詢範例（main.py）**  
  從 `.env` 載入 Gemini API 金鑰，使用 `OpenAIChatCompletionClient` 連接 Gemini 模型，並發送一個查詢訊息，回傳結果印出至終端機。

- **多代理人對話範例（multiAgent.py）**  
  利用 AutoGen 框架建立一個多代理人團隊：
  - **AssistantAgent** 與 **MultimodalWebSurfer**：負責回答與資訊檢索。
  - **UserProxyAgent**：模擬使用者參與對話。  
  團隊以輪詢方式進行對話，直到對話中出現 `"exit"` 關鍵字為止。

- **多代理人檔案 I/O 範例（dataAgent.py）**  
  利用 AutoGen 框架建立一個多代理人團隊：
  - **DataAgent** 與 **MultimodalWebSurfer**：分別負責 CSV 資料分析、外部資訊檢索與問題解答。
  - **UserProxyAgent**：模擬使用者參與對話。  
  團隊以輪詢方式進行對話，直到對話中出現 `"exit"` 關鍵字為止。

- **多代理人檔案 I/O 與多模型範例（multiDataAgent.py）**  
  利用 AutoGen 框架建立一個多代理人團隊：
  - 多模型使用：使用 model_client_data_web（gemini-1.5-flash-8b）供 data_agent 與 web_surfer 使用，進行初步資料分析。使用 model_client_assistant（gemini-2.0-flash）供 assistant 使用，依據先前分析結果整合外部資訊，生成最終的寶寶照護建議。
  - 多 prompt 寫法：第一階段的 prompt (prompt_8b) 用於要求代理人從 CSV 資料中分析寶寶的日常行為與照護需求。第二階段的 prompt (prompt_flash) 則要求代理人參考前一階段分析結果，結合外部網站搜尋到的最新資訊，生成完整且具參考價值的照護建議。
  - 多代理人協作：四個代理人（data_agent、MultimodalWebSurfer、assistant 與 user_proxy）共同組成一個團隊（RoundRobinGroupChat），分階段協同完成任務，最終將所有對話內容整合後輸出為 CSV。

- **多代理人檔案 I/O 與多模型 UI 範例（multiDataAgentUI.py）** 
  使用 Gradio + Gemini API + AutoGen AgentChat 建立一個 寶寶照護數據分析工具，可讀取 CSV 格式的寶寶照護數據，並自動摘要與分析，提供有價值的建議。
---

## 前置需求

- Python 3.10 或更新版本
- [pip](https://pip.pypa.io/en/stable/installation/)
- 安裝以下 Python 套件：
  - `python-dotenv`
  - `autogen-agentchat`
  - `autogen-ext[openai]`
  - `playwright` (multiAgent.py 中用於 WebSurfer)  
    並執行以下命令下載瀏覽器二進位檔：
    ```bash
    playwright install
    ```

---

## 安裝與設定

1. **Clone 專案**

   ```bash
   git clone <repository-url>
   cd <repository-folder>
