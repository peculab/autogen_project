# 🧠 Gemini Evaluation & Report Generation System

This project provides an end-to-end pipeline for **analyzing conversational transcripts using LLMs (Google Gemini)** and generating structured **PDF reports with visualized insights**.

It is designed for both **research and educational use**, particularly in human-centered AI, learning analytics, and agent-based systems.

---

## 🔹 Overview

This system integrates two core components:

- **DRai.py** → LLM-based transcript evaluation (CSV → structured analysis)
- **getPDF.py** → Automated report generation (analysis → formatted PDF + UI)

Together, they form a complete pipeline:

> **Raw Data → LLM Analysis → Structured Output → PDF Report**

---

## 🔹 Key Features

### 1. LLM-Based Transcript Analysis
- Batch processing of conversational data from CSV files  
- Automatic detection of text columns (e.g., `text`, `dialogue`, `content`)  
- Uses **Google Gemini API** for classification and evaluation  
- Supports structured JSON output for downstream processing  

---

### 2. Intelligent Batch Processing
- Groups multiple rows into a single API request  
- Reduces API cost and latency  
- Uses delimiters to separate responses  
- Includes retry-safe incremental saving  

---

### 3. Robust Output Handling
- Handles malformed JSON responses  
- Automatically fills missing classification fields  
- Saves intermediate results to avoid data loss  

---

### 4. PDF Report Generation
- Converts analysis results into well-formatted PDF reports  
- Supports:
  - Structured tables  
  - Alternating row colors  
  - Automatic pagination  
- Detects and loads Chinese fonts if available  

---

### 5. Markdown Table Parsing
- Converts LLM-generated Markdown tables into pandas DataFrames  
- Enables seamless transformation into PDF tables  

---

### 6. Interactive UI (Gradio)
- Upload CSV files  
- Input custom analysis prompts  
- Generate reports in one click  
- Download final PDF output  

---

## 🔹 Example Workflow

1. Upload CSV transcript data  
2. Define evaluation prompt (or use default)  
3. System processes data in batches  
4. Gemini generates structured analysis  
5. Results are aggregated  
6. PDF report is generated automatically  

---

## 🔹 Default Evaluation Categories

The system supports customizable classification.  
Default categories include:

- Guidance  
- Evaluation (verbal / non-verbal)  
- Extended discussion  
- Repetition  
- Open-ended questions  
- Fill-in responses  
- Recall  
- WH-questions  
- Real-life connection  
- Notes  

---

## 🔹 Use Cases

This system can be applied to:

- Learning analytics  
- Classroom interaction analysis  
- Parent-child reading behavior analysis  
- AI-assisted educational evaluation  
- Conversational data mining  
- Human-centered AI systems  

---

## 🔹 Educational Applications

This project is ideal for courses such as:

- Agentic AI Systems  
- Human-Centered AI  
- AI in Education  
- LLM Applications  

Students can learn:

- How to structure LLM prompts  
- How to process large datasets with LLMs  
- How to build end-to-end AI pipelines  
- How to generate interpretable AI outputs  

---

## 🔹 Installation

Install required packages:

```bash
pip install pandas python-dotenv google-generativeai fpdf gradio requests