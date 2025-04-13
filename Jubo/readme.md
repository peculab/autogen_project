# 🩺 Health Record Monitor Automation with AI Analysis

這是一個基於 Python + Playwright + Gemini AI 的自動化健康數據擷取與分析工具。  
專為 Jubo Health Demo 系統設計，實現以下自動化流程：

1. ⏱ 自動掃描指定時間區段的健康數據
2. 📊 自動提取有效數據並保存為 CSV
3. 🤖 使用 Gemini AI 自動生成健康照護建議
4. 🌐 自動生成美觀的 HTML 報告並自動打開瀏覽器查看

## 🚀 功能特色

- 自動登入 Jubo Health Demo 平台
- 自動遍歷所有時間區段，檢查是否有資料
- 抓取健康數據表格，並匯出 CSV
- 呼叫 Gemini AI，生成照護建議（英文）
- 生成可視化 HTML 報告，結合 AI 分析與原始數據
- 完成後自動開啟瀏覽器檢視報告

## 🛠️ 技術棧

- Python 3.8+
- [Playwright](https://playwright.dev/python/)
- [Google Gemini AI](https://ai.google.dev/)
- Pandas
- Markdown2
- dotenv