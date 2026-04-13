# ⚖️ Multi-Agent Legal Document Analyzer

An AI-powered system that analyzes legal contracts using a **multi-agent architecture** to detect risks, classify clauses, identify compliance issues, and generate structured legal reports.

---

## 🚀 Live Demo

👉 Streamlit App:  
https://ai-data-science-agent-bishnu.streamlit.app/

---

## ✨ Features

- 🤖 Multi-Agent Workflow using LangGraph  
- ⚠️ Risk Detection (Low / Medium / High)  
- 📋 Compliance Issue Identification  
- 🧠 Clause Explanation in Simple English  
- 📊 Professional Legal Report Generation  
- 📄 PDF & Text Input Support  
- 🎨 Clean and Interactive UI (Streamlit)  
- ⚡ Fast LLM inference using Groq API  

---

## 🏗️ Architecture

The system follows a **multi-agent pipeline**:
```
Parser Agent  
↓  
Classifier Agent  
↓  
Risk Agent  
↓  
Explanation Agent  
↓  
Compliance Agent  
↓  
Report Agent  

Each agent performs a specific task and passes structured outputs to the next stage.
```
---

## 📁 Project Structure
```
legal-ai-agent/
│
├── app.py                  # Streamlit UI
├── requirements.txt
├── .env                    # API keys (not pushed)
│
├── agents/
│   ├── parser.py
│   ├── classifier.py
│   ├── risk_agent.py
│   ├── compliance_agent.py
│   ├── explanation_agent.py
│   └── report_agent.py
│
├── graph/
│   └── workflow.py         # LangGraph workflow
│
├── rag/
│   ├── memory_store.py
│   ├── retriever.py
│   └── vector_store.py
│
├── utils/
│   ├── llm.py              # Groq / LLM integration
│   └── pdf_reader.py
│
└── chroma_db/              # Vector DB (optional)
```
---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```
git clone https://github.com/YOUR_USERNAME/legal-ai-agent.git  
cd legal-ai-agent  
```
---

### 2️⃣ Create Virtual Environment
```
python -m venv venv  
venv\Scripts\activate   # Windows  
```
---

### 3️⃣ Install Dependencies
```
pip install -r requirements.txt  
```
---

### 4️⃣ Environment Variables
```
Create a `.env` file in the root directory:

GROQ_API_KEY=your_api_key_here  
```
---

## ▶️ Run the Application
```
python -m streamlit run app.py  
```
Then open:
```
http://localhost:8501  
```
---

## 🧪 How It Works

1. Upload or paste a legal document  
2. Parser extracts clauses  
3. Classifier categorizes clauses  
4. Risk agent detects risk levels  
5. Compliance agent finds missing clauses  
6. Explanation agent simplifies clauses  
7. Report agent generates final report  

---

## 🎯 Use Cases

- 📑 Contract Review Automation  
- ⚖️ Legal Risk Analysis  
- 🏢 Business Agreement Validation  
- 🧠 AI Legal Assistant  
- 📊 Compliance Auditing  

---

## 📸 Screenshots

(Add screenshots here)

---

## 🔐 Security Note

- Do NOT commit `.env` file  
- Keep API keys private  

---

## 🚀 Future Improvements

- Highlight risky clauses inside document  
- Multi-language support  
- Cloud deployment  
- User authentication  
- Advanced legal RAG  

---

## 👨‍💻 Author

**Bishnu Agarwal**  
M.Tech (CSDP - Computer Science and Data Processing), IIT Kharagpur  
AI / ML / Data Science  

---

## ⭐ Support

If you like this project:

⭐ Star the repository  
🍴 Fork it  
📢 Share it  
