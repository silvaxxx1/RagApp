Here's the updated `README.md` with your custom `uvicorn` command added under the **"Run the Backend Server"** section:

---

````markdown
# 🧠 RagApp – End-to-End Retrieval-Augmented Generation (RAG) System

**RagApp** is a minimal yet extensible full-stack project to build a complete **Retrieval-Augmented Generation (RAG)** system from scratch — covering every major component from data ingestion to LLM-based response generation and deployment.

This project is designed for **hands-on learning**, **modular experimentation**, and evolving into a **production-ready architecture** using best practices in backend, LLM orchestration, and modern tooling.

> 🔧 We will incrementally evolve this into a production-ready, full-stack RAG system.

---

## ✅ What to Expect

- 🔎 Clean, modular architecture with retriever-generator separation  
- 🚀 FastAPI backend (async-first, OpenAPI support)  
- 🧠 Support for OpenAI and local LLMs (via API)  
- 📦 Easy setup using `uv` and Python 3.12+  
- 🧪 Focus on **fast prototyping**, **inference efficiency**, and **open-source extensibility**  
- 🔁 Full development cycle: dev → test → deploy  

---

## 📦 Project Setup

### 1. Prerequisites

- Python ≥ 3.12  
- [`uv`](https://github.com/astral-sh/uv) package manager  
  *(Install with `pip install uv` if not already installed)*

---

### 2. Clone the Repository

```bash
git clone https://github.com/silvaxxx1/RagApp.git
cd RagApp
````

---

### 3. Install Dependencies

```bash
uv init
uv add -r requirements.txt
```

> This sets up a virtual environment (`.venv`) and installs all required packages.

---

### 4. Set Up Environment Variables

Copy the example config:

```bash
cp uv.example .env
```

Edit `.env` to add your OpenAI key and other configs:

```env
APP_NAME="RagApp"
APP_VERSION="0.1"
OPENAI_API_KEY="your-openai-key-here"
```

---

### 5. Run the Backend Server

To run locally with default settings:

```bash
uvicorn app.main:app --reload
```

To expose the server on all interfaces and custom port:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

Then open [http://localhost:5000/docs](http://localhost:5000/docs) to see the interactive Swagger UI.

---

## 📌 Work in Progress

This repository is under active development. Upcoming features include:

* 📄 Document chunking and embedding
* 🔍 Vector DB integration (FAISS/Chroma)
* 🧠 Prompting and LLM generation modules
* ⚙️ RAG pipeline orchestration
* 🖥️ Optional frontend (React/Tailwind or minimal HTML)
* 🚀 Dockerized and cloud deployment setup

---

## 🗺️ Roadmap

* [x] Init project with `uv` and FastAPI
* [ ] Embedding pipeline with OpenAI/Transformers
* [ ] Vector search integration
* [ ] Generation + post-processing logic
* [ ] Full RAG chain API
* [ ] CI/CD & Docker deployment

---

## 🤝 Contributing

Feel free to fork, clone, and build along! PRs and ideas are welcome.
Let’s create a clean, reusable, and battle-tested open RAG template for all.

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](./LICENSE) for details.

