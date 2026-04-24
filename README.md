# 🏫 Smart Campus Intelligence System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![GenAI](https://img.shields.io/badge/AI-Generative-green)

## 🚀 Overview
A Generative AI-powered smart campus system that integrates Computer Vision, Vector Databases, and Large Language Models (LLMs) to automate attendance, enable intelligent querying, and provide real-time analytics.

---

## 🧠 Features

- **👤 Face Recognition Enrollment**  
  Converts student faces into 512-dimensional vector embeddings using DeepFace (Facenet512). No raw images are stored, ensuring privacy.

- **📸 Real-Time Attendance Marking**  
  Detects and recognizes faces from live camera feed using cosine similarity search in ChromaDB, automatically marking attendance.

- **💬 AI Query Engine (RAG)**  
  Ask questions in natural language. Powered by LangChain and Google Gemini to retrieve and generate context-aware answers.

- **📊 Analytics Dashboard**  
  Interactive dashboards using Plotly for student insights, trends, and performance monitoring.

---

## 🛠️ Tech Stack

- **Core Language:** Python 3.11  
- **Web Dashboard:** Streamlit  
- **Face Recognition:** DeepFace (Facenet512)  
- **Vector Database:** ChromaDB  
- **LLM & RAG:** Google Gemini + LangChain  
- **Computer Vision:** OpenCV  
- **Visualization:** Plotly  

---

## ⚙️ How It Works

1. **Enrollment:** Face → DeepFace → 512-d vector  
2. **Storage:** Stored securely in ChromaDB with metadata  
3. **Recognition:** Live camera → vector → similarity search  
4. **AI Querying:** RAG pipeline fetches relevant data and generates answers  

---

## ⚡ Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/Smart-Campus-Intelligence-System.git
cd Smart-Campus-Intelligence-System
