# AutoGen Gemini 示例

本專案展示如何使用 AutoGen 框架與 Gemini API 來實現兩種不同的應用範例：

1. **main.py**  
   一個簡單的範例，透過 Gemini 模型回答單一查詢（"What is the capital of France?"）。

2. **multiAgent.py**  
   一個多代理人協作對話範例，利用 RoundRobinGroupChat 將三個代理人（Assistant、WebSurfer 與 UserProxy）組成團隊，完成「請搜尋 Gemini 的相關資訊，並撰寫一份簡短摘要」的任務。

3. **dataAgent.py**  
   這是一個多代理人協作對話範例，利用 RoundRobinGroupChat 將四個代理人（DataAgent、MultimodalWebSurfer、Assistant 與 UserProxy）組成團隊，分批處理 CSV 資料，並要求 MultimodalWebSurfer 搜尋外部網站，納入最新的寶寶照護建議資訊，最終將所有對話內容整合並輸出為 CSV。

---

## 功能介紹

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
