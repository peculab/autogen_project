# Multi-Agent Sentiment Analysis

這個專案是一個基於 Flask 的多代理（Multi-Agent）即時分析系統，用於分析使用者上傳的日記數據並生成個性化的情緒建議。專案的主要特點包括：

- 使用多個 AI Agent 分工合作進行分析與建議生成
- 實時顯示各個 Agent 的分析過程及輸出
- 自動提取最終建議並展示給使用者

## 功能概覽

- **即時分析進度**：通過 Socket.IO 持續更新分析進度，展示不同 Agent 的行為和輸出內容。
- **多輪互動**：系統支持多輪的 Agent 分析互動，確保生成高質量的情緒建議。
- **即時顯示結果**：將分析結果直接返回前端，包括提取的「最終建議」。
- **簡化視覺化**：透過簡潔的即時進度與建議區塊，提升使用者的閱讀體驗。

## 如何運行專案

1. 確保本地已安裝 Python 3.8 或更高版本，以及以下環境需求：
    - Flask
    - Python-dotenv
    - 其他必要套件（可參考 `requirements.txt`）

2. 配置環境變數：
    - 創建一個 `.env` 文件
    - 在 `.env` 文件中加入以下內容：
      ```
      GEMINI_API_KEY=your_openai_api_key
      ```

3. 安裝依賴：
    ```
    pip install -r requirements.txt
    ```

4. 啟動伺服器：
    ```
    flask run
    ```
    預設會在 `http://127.0.0.1:5000` 啟動。

5. 開啟瀏覽器，將日記數據上傳至網頁介面，並觀察即時分析進度。

## 程式碼簡介

- **`app.py`**  
  Flask 應用主入口，處理使用者上傳日記、觸發分析任務，並返回前端顯示的分析結果。

- **`multiagent.py`**  
  實作多代理分析邏輯，協同多個 AI Agent 對日記數據進行分析與建議生成，並透過 WebSocket 持續傳送更新至前端。

- **`EMOwithSnow.py`**  
  提供日記數據的情緒分析與趨勢圖生成邏輯，將結果保存為圖表供前端使用。

- **`requirements.txt`**  
  列出本專案所需的 Python 套件和相應版本。

## 貢獻與反饋

歡迎提交 Issue 或 Pull Request，幫助我們改進系統性能與使用體驗！

## 授權

[MIT License](LICENSE)