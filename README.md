# 🧠 RagApp – End-to-End Retrieval-Augmented Generation (RAG) System

**RagApp** is a full-stack, extensible project for building **Retrieval-Augmented Generation (RAG)** systems from scratch — covering everything from data ingestion to LLM-based response generation and deployment.

---

<p align="center">
  <img src="ragapp.png" alt="Quantization Overview">
</p>


---
This repo is designed for:

* **Hands-on learning** (understand each piece of RAG systems)
* **Modular experimentation** (swap databases, models, retrievers)
* **Scaling to production** (deployment, orchestration, monitoring)

> 🔧 Currently in **Phase 2** — migrating from MongoDB → Postgres/pgvector for scalable vector search and orchestration.

---

## ✅ Highlights

* 🔎 **Retriever-Generator separation** (clean, modular architecture)
* 🚀 **FastAPI backend** (async-first, OpenAPI ready)
* 🧠 **LLM flexibility**: OpenAI, Ollama (on-prem), Cohere, Sentence Transformers
* 📦 **Database options**: MongoDB (Motor) ✅ → Postgres + pgvector (in progress)
* 🔍 **Vector search**: Qdrant (current) → pgvector (planned)
* 🧪 **LangChain (PDF parsing + chunking only)**, keeping rest lightweight
* 🐳 **Dockerized services** (MongoDB, Postgres, Qdrant)
* 🔁 **CI/CD-ready** architecture (phase 3 roadmap)

---

## 📦 Tech Stack (v1 → v2)

### **Phase 1 – RagApp-MongoDB-v1 (Latest Stable)**

* FastAPI + Uvicorn
* MongoDB (Motor async driver)
* Qdrant for embeddings
* Ollama (local LLMs), OpenAI, Cohere
* Sentence Transformers (open-source embeddings)
* LangChain (document loaders + chunking only)
* Docker Compose for services

✅ Stable and functional baseline with **MongoDB + Qdrant**.

---

### **Phase 2 – Scaling Up (In Progress 🚧)**

* **Postgres + Alembic migrations (done)**
* **pgvector integration (coming soon)**
* Refactored backend to support dual database setup
* Running hybrid **Postgres + Qdrant** stack smoothly

Next → replace Qdrant with **pgvector-only architecture**.

---

### **Phase 3 – Advanced Orchestration (Planned 🚀)**

* Celery + RabbitMQ for background tasks & distributed pipelines
* Advanced RAG strategies (re-ranking, multi-query, hybrid retrieval)
* Deployment-ready infra (cloud/K8s, monitoring, scaling)

---

## ⚡ Quickstart

### 1. Clone & Setup

```bash
git clone https://github.com/silvaxxx1/RagApp.git
cd RagApp
```

### 2. Install Dependencies

```bash
uv init
uv add -r requirements.txt
```

### 3. Environment Variables

```bash
cp uv.example .env
```

Update `.env` with your API keys and configs.

### 4. Run Services (Docker)

```bash
cd docker
cp .env.example .env   # update with credentials
docker-compose up -d
```

### 5. Run the Backend

```bash
uvicorn app.main:app --reload
```

Access Swagger UI at → [http://localhost:5000/docs](http://localhost:5000/docs)

---

## 🗺️ Roadmap

* [x] **Phase 1** – MongoDB + Qdrant baseline
* [x] Alembic migrations with Postgres
* [ ] Full pgvector migration (replace Qdrant)
* [ ] RAG pipeline orchestration improvements
* [ ] Background tasks with Celery + RabbitMQ
* [ ] Advanced RAG methods (re-ranking, hybrid, multi-query)
* [ ] Production deployment templates (Docker/K8s, CI/CD)

---

## 🤝 Contributing

Fork, clone, and build along!
Ideas, PRs, and discussions are welcome as we evolve RagApp into a **production-grade RAG template** for the community.

---

## 📄 License

MIT License – see [LICENSE](./LICENSE)

---
