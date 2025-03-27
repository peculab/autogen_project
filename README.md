# AutoGen Gemini 範例與寶寶照護分析工具

本專案展示了如何使用 [AutoGen](https://github.com/microsoft/AutoGen) 框架結合 Gemini API，構建多代理人協作系統，實現從資料分析到社群媒體自動發文的完整工作流程。專案涵蓋多個範例，分別展示不同場景下的代理人對話、資料處理與外部應用整合。

---

## 範例說明

### 1. 多代理人 CSV 資料分析
- **dataAgent.py**  
  讀取 CSV 格式的寶寶日記資料（例如 `cuboai_baby_diary.csv`），分批（chunk）處理數據，並由多個代理人協作：
  - **AssistantAgent**：負責分析數據與提供照護建議。
  - **MultimodalWebSurfer**：透過外部網站搜尋最新寶寶照護資訊。
  - **UserProxyAgent**：模擬使用者參與。
  
  分析結果會彙整後輸出至 CSV 檔案 `all_conversation_log.csv`。

- **multiDataAgent.py**  
  進一步展示多模型協作：
  - 使用 Gemini 的不同模型（如 `gemini-1.5-flash-8b` 與 `gemini-2.0-flash`）分別處理初步分析與結果整合。
  - 多階段 prompt 協同處理 CSV 資料，最終生成包含分析細節的回應，並以非同步方式逐步回傳結果。

- **multiDataAgentUI.py**  
  基於 Gradio 建立互動式使用者介面：
  - 使用者可上傳 CSV 檔案，系統自動將檔案分區塊讀取、生成摘要，並由代理人依序進行分析。
  - 介面支援即時顯示分析進度與對話紀錄，最後將完整對話保存為 `conversation_log.csv`。

### 2. 多代理人對話範例
- **multiAgent.py**  
  展示簡單的多代理人對話系統：
  - 建立包含 **AssistantAgent**、**MultimodalWebSurfer** 與 **UserProxyAgent** 的團隊。
  - 利用輪詢方式進行對話，任務為搜尋 Gemini 相關資訊並撰寫簡短摘要，直到收到 `"exit"` 終止指令。

### 3. 自動化社群媒體發文
- **postAI.py**  
  利用 [Playwright](https://playwright.dev/) 自動化 Facebook 貼文流程：
  - 從 `.env` 讀取 Facebook 帳號與密碼。
  - 模擬使用者登入 Facebook、打開發文對話框並輸入內容，最後自動發佈貼文。
  - 過程中會截圖以供除錯與確認。

---

## 前置需求

- **Python 版本**：3.10 或更新版本
- **必備套件**：
  - `python-dotenv`
  - `autogen-agentchat`
  - `autogen-ext[openai]`
  - `pandas`
  - `gradio`
  - `playwright`
  - 其他依賴請參考各模組的 requirements

- **瀏覽器二進位檔**（僅針對 `postAI.py` 使用 Playwright）  
  安裝後執行：
  ```bash
  playwright install
