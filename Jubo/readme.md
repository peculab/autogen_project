# 🩺 Health Record Monitor Automation with AI Analysis

This project is an automated pipeline for **health data extraction, analysis, and reporting**, powered by:

- Playwright (web automation)
- Google Gemini (LLM-based analysis)
- Python data processing

It demonstrates how to build a **real-world agentic AI workflow**, combining data collection, AI reasoning, and automated reporting.

---

## 🔹 Overview

This system performs an end-to-end workflow:

1. Automatically logs into a health monitoring system  
2. Scans multiple time ranges for available data  
3. Extracts structured health records  
4. Generates AI-based care recommendations using Gemini  
5. Produces both CSV data files and HTML reports  
6. Automatically opens the report for review  

This pipeline represents a **practical example of AI-powered workflow automation**.

---

## 🔹 Key Features

- Automated login and navigation (Playwright)
- Dynamic time-range scanning
- Structured data extraction from web UI
- CSV export for downstream analysis
- AI-generated medical insights (Gemini)
- HTML report generation with visualization
- End-to-end automation (no manual steps)

---

## 🔹 Example Output

### 📊 Data Output
- CSV file with structured patient data  
- Includes time range, vital signs, and metadata  

### 🤖 AI Analysis Output
- Categorized health insights:
  - Hypertension  
  - Abnormal Body Temperature  
  - Abnormal Respiratory Rate  

- Structured recommendations:
  - Identified issues  
  - Suggested care actions  

### 🌐 HTML Report
- Clean, readable UI
- Combined AI insights + raw data table
- Automatically opened in browser

---

## 🔹 Tech Stack

- Python 3.8+
- Playwright (web automation)
- Google Gemini API (LLM)
- Pandas (data processing)
- Markdown2 (HTML conversion)
- dotenv (environment management)

---

## 🔹 How It Works

### Step 1 — Login Automation
The system logs into the target platform using credentials stored in `.env`.

### Step 2 — Data Scanning
It iterates through multiple predefined time ranges:

- Last 24 Hours  
- Last 3 Days  
- Last 7 Days  
- Last 14 Days  
- Last 30 Days  

### Step 3 — Data Extraction
Structured data is extracted from the web interface and stored in memory.

### Step 4 — AI Analysis
The system sends formatted data to Gemini for analysis and generates:

- Health issue classification  
- Professional care recommendations  

### Step 5 — Report Generation
- CSV file is saved  
- HTML report is generated  
- Browser opens automatically  

---

## 🔹 Educational Value

This project is designed as a **teaching-ready case study** for:

> *Agentic AI Engineering: Building Real-World LLM Agent Systems*

It demonstrates:

- End-to-end AI workflows  
- LLM integration in real systems  
- Automation + reasoning pipelines  
- Applied AI in healthcare scenarios  

---

## 🔹 Real-World Relevance

This system reflects real industry patterns:

- AI-assisted decision support  
- Automated monitoring systems  
- Data-to-insight pipelines  
- AI-enhanced reporting tools  

---

## 🔹 Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
playwright install