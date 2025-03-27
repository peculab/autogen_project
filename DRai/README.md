# Gemini 評估與報表生成工具

本專案整合了兩個主要功能模組，分別針對家長唸故事書逐字稿的批次評估以及報表 PDF 的生成：

- **DRai.py**：從 CSV 檔案中讀取逐字稿，透過 [Google Gemini API](https://ai.google.dev/gemini-api/docs) 批次評估對話內容，並將評估結果輸出至 CSV 檔案中。
- **getPDF.py**：依據 CSV 資料或文字內容，生成包含統計與表格的 PDF 報表，並提供 Gradio 使用者介面方便使用者互動產生報表。

---

## 功能概述

### DRai.py

- **自動欄位識別**  
  根據 CSV 檔案內容，自動選取存放逐字稿的欄位，優先順序為 `text`、`utterance`、`content`、`dialogue` 等。

- **批次請求與 API 呼叫**  
  將多筆逐字稿合併成批次請求給 Gemini API，並要求模型依照預設的評分項目（例如 "引導"、"評估(口語、跟讀的內容有關)"、"延伸討論" 等）產生 JSON 格式回覆。各筆結果以自訂的分隔符（預設為 `-----`）隔開，藉此減少 API 呼叫次數。

- **結果解析與即時存檔**  
  程式會解析回傳的 JSON 結果（同時處理可能被 Markdown 反引號包圍的情況），並補齊缺少的評分項目。每個批次處理完後，結果會即時寫入 `113_batch.csv`，以防中途錯誤導致資料遺失。

- **API 請求延遲**  
  為避免短時間內大量請求，每處理一個批次後程式會延遲 1 秒。

### getPDF.py

- **PDF 報表生成**  
  利用 [FPDF](https://pyfpdf.github.io/fpdf2/) 將 CSV 或文字資料生成 PDF 報表。報表中包含漂亮的表格展示、交替背景色處理以及自動分頁功能。

- **中文字型偵測與載入**  
  在 Windows 系統中，程式會搜尋候選中文字型（例如 `kaiu.ttf`），並載入至 PDF 報表中。若找不到合適的中文字型，將會顯示錯誤訊息。

- **Markdown 表格解析**  
  支援從 Markdown 格式的表格文字提取資料並轉換成 pandas DataFrame，方便以表格形式呈現在 PDF 報表中。

- **Gradio 使用者介面**  
  提供基於 Gradio 的網頁介面，使用者可上傳 CSV 檔案並輸入自訂分析指令（預設指令已包含評分規則）。系統會將 CSV 資料分區塊處理，每個區塊呼叫 Gemini API 取得回應，最終合併所有回應生成 PDF 報表，方便下載與分享。

---

## 安裝與環境設定

1. **Python 套件安裝**  
   請先確保已安裝下列 Python 套件：
   - pandas
   - python-dotenv
   - google (或相應的 Gemini API 套件)
   - fpdf
   - gradio
   - requests

2. **設定環境變數**  
   在專案根目錄下建立 `.env` 檔案，並加入有效的 Gemini API 金鑰