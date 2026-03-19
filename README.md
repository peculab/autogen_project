# Agentic AI Engineering with AutoGen and Gemini

This repository contains teaching-ready examples for **building real-world LLM agent systems** with AutoGen-style multi-agent workflows, Gemini models, and lightweight application interfaces.

The project can support a professional course such as:

**Agentic AI Engineering: Building Real-World LLM Agent Systems**

It is designed around the same themes highlighted in the UW PCE proposal:
- LLM-based agent architectures
- multi-agent collaboration
- tool use and workflow automation
- retrieval and grounded reasoning
- deployment-oriented application design

## Why this repository matters

Many generative AI tutorials stop at prompt engineering. This repository goes one step further and shows how to build **agentic AI systems** that can:
- coordinate multiple agents
- process structured data such as CSV files
- combine analysis with external tools or web access
- support real user workflows through web apps and dashboards

These materials can be adapted into a short professional course, an advanced elective, or a capstone-oriented applied AI offering.

## Repository map

### Core teaching examples

- `main.py`
  - Minimal LLM client example using a Gemini-compatible chat completion interface.
  - Good for introducing environment setup, model calls, and async execution.

- `multiAgent.py`
  - Introductory multi-agent collaboration example.
  - Demonstrates how a researcher, a web-enabled agent, and a user proxy can work together on a task.
  - Best aligned with **Module 2: Multi-Agent Collaboration**.

- `dataAgent.py`
  - Chunk-based structured data analysis workflow for CSV files.
  - Demonstrates multi-agent reasoning over records, prompt construction, and logging of outputs.
  - Best aligned with **Module 4: Workflow Automation**.

- `multiDataAgent.py`
  - Streaming, chunk-level analysis pipeline with optional synthesis.
  - Best aligned with **Modules 3-4: Tool Use and Workflow Automation**.

- `multiDataAgentUI.py`
  - Gradio-based front end for uploading CSV files and receiving streaming analysis updates.
  - Best aligned with **Module 6: Deployment and Evaluation**.

### Applied application demos

- `EMO/`
  - Multi-agent diary and sentiment analysis application.
  - Demonstrates Flask, Socket.IO, charting, and agent collaboration for user-facing applications.

- `MCP/`
  - A multi-agent application using a Model Context Protocol-style abstraction.
  - Useful for discussing model portability and system architecture choices.

- `Jubo/`
  - Playwright-based healthcare workflow automation and Gemini-assisted reporting examples.
  - Useful for real-world workflow orchestration and domain-specific AI applications.

- `DRai/`
  - Batch transcript evaluation and PDF reporting pipeline.
  - Useful for discussing applied evaluation workflows and report generation.

## Suggested course mapping

### Module 1 - Foundations of Agentic AI
- `main.py`
- `multiAgent.py`

### Module 2 - Multi-Agent Collaboration
- `multiAgent.py`
- `EMO/multiagent.py`
- `MCP/multiagent.py`

### Module 3 - Tool Use and Function Calling
- `Jubo/playwright_gemini_html.py`
- examples extended from `multiDataAgent.py`

### Module 4 - Workflow Automation
- `dataAgent.py`
- `multiDataAgent.py`
- `DRai/DRai.py`

### Module 5 - RAG and Knowledge Systems
- This repository does not yet include a full RAG module.
- A natural next upgrade would be adding a `course/week5_rag.ipynb` example using FAISS and domain documents.

### Module 6 - Deployment and Evaluation
- `multiDataAgentUI.py`
- `EMO/app.py`
- `MCP/app.py`

## Learning outcomes supported by this repo

Using these examples, learners can practice how to:
1. design an LLM-based agent workflow
2. build multi-agent systems for structured and unstructured tasks
3. integrate external tools into an AI workflow
4. process real data and log intermediate reasoning outputs
5. build lightweight user interfaces for applied AI systems
6. turn prototypes into portfolio-ready projects

## Recommended audience

This repository is especially suitable for:
- software engineers moving into AI engineering
- data analysts transitioning toward LLM application development
- technical professionals learning applied agent workflows
- instructors building project-based agentic AI courses

## Quick start

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

Install the dependencies required by the specific demo you want to run. Common packages used in this repository include:

```bash
pip install python-dotenv pandas gradio playwright autogen-agentchat autogen-ext[openai]
```

Install Playwright browsers when needed:

```bash
playwright install
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```dotenv
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

Optional variables used by some demos:

```dotenv
CSV_FILE_PATH=cuboai_baby_diary.csv
FACEBOOK_EMAIL=your_email
FACEBOOK_PASSWORD=your_password
```

### 4. Run a simple example

```bash
python main.py
```

### 5. Run the multi-agent example

```bash
python multiAgent.py
```

## Current limitations and next upgrades

This repository already demonstrates strong foundations for an applied course, but the following upgrades would make it even more course-ready:
- add a dedicated English notebook sequence under `course/`
- add a full RAG example with embeddings and a vector store
- standardize logging and evaluation metrics across demos
- add Docker or cloud deployment examples for capstone projects

## Educational note

Some original materials in this repository were first written in Chinese. This version updates the top-level documentation in English and better aligns the codebase with a professional course proposal focused on **agentic AI engineering**.

## License

MIT License. See `LICENSE` for details.
