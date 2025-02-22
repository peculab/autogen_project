# AutoGen Gemini 示例

本專案展示如何使用 AutoGen 框架與 Gemini API 來實現兩種不同的應用範例：

1. **main.py**  
   一個簡單的範例，透過 Gemini 模型回答單一查詢（"What is the capital of France?"）。

2. **multiAgent.py**  
   一個多代理人協作對話範例，利用 RoundRobinGroupChat 將三個代理人（Assistant、WebSurfer 與 UserProxy）組成團隊，完成「請搜尋 Gemini 的相關資訊，並撰寫一份簡短摘要」的任務。

---

## 目錄

- [功能介紹](#功能介紹)
- [前置需求](#前置需求)
- [安裝與設定](#安裝與設定)
- [使用方式](#使用方式)
  - [運行 main.py](#運行-mainpy)
  - [運行 multiAgent.py](#運行-multiagentpy)
- [程式碼說明](#程式碼說明)
  - [main.py](#mainpy)
  - [multiAgent.py](#multiagentpy)
- [License](#license)
- [貢獻](#貢獻)

---

## 功能介紹

- **單一查詢範例（main.py）**  
  從 `.env` 載入 Gemini API 金鑰，使用 `OpenAIChatCompletionClient` 連接 Gemini 模型，並發送一個查詢訊息，回傳結果印出至終端機。

- **多代理人對話範例（multiAgent.py）**  
  利用 AutoGen 框架建立一個多代理人團隊：
  - **AssistantAgent** 與 **MultimodalWebSurfer**：負責回答與資訊檢索。
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
