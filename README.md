# 🧠 RagApp – End-to-End Retrieval-Augmented Generation (RAG) System

**RagApp** is a full-stack, extensible project for building **Retrieval-Augmented Generation (RAG)** systems from scratch — covering everything from data ingestion to LLM-based response generation and deployment.

---

<p align="center">
  <img src="ragapp.png" alt="RagApp Architecture" width="700"/>
</p>

---

This repo is designed for:

* **Hands-on learning** (understand each piece of RAG systems)
* **Modular experimentation** (swap databases, models, retrievers)
* **Scaling to production** (deployment, orchestration, monitoring)

> 🔧 Currently in **Phase 2 – v2.0.0** — migrated fully to **Postgres + PGVector**, keeping **Qdrant functional** (dual vector DB), with improved orchestration and async pipelines.

---

## ✅ Highlights (v2.0.0)

1. **Dual Vector DB Support**

   * Fully migrated to **Postgres + PGVector** for scalable vector search.
   * **Qdrant** still operational, enabling hybrid/dual DB setups.
   * Switching between vector DBs is now as simple as changing a **single string in `.env`**.

2. **Orchestration Improvements**

   * Streamlined async pipelines and indexing workflows.
   * More robust backend architecture for concurrent queries and vector operations.

3. **Future Plans / Next Steps**

   * Deployment-ready backend.
   * Scaling with **Celery + Redis** for distributed task management.
   * Continuous RAG pipeline enhancements (re-ranking, hybrid retrieval, multi-query).

---

## 📦 Tech Stack (v1 → v2)

### **Phase 1 – RagApp-MongoDB-v1**

* FastAPI + Uvicorn
* MongoDB (Motor async driver)
* Qdrant for embeddings
* Ollama (local LLMs), OpenAI, Cohere
* Sentence Transformers (open-source embeddings)
* LangChain (document loaders + chunking only)
* Docker Compose for services

✅ Stable baseline with **MongoDB + Qdrant**.

---

### **Phase 2 – RagApp-v2 (Dual Vector DB & Orchestration Upgrade 🚀)**

* **Postgres + PGVector fully integrated** (Qdrant still functional)
* Refactored backend to support **dual database setup**
* Async workflows & indexing improved for better performance
* Switching vector DB is configurable via `.env`
* Ready for deployment and scaling

Next → integrate **Celery + Redis** for distributed tasks and scaling.

---

### **Phase 3 – Advanced Orchestration (Planned)**

* Celery + RabbitMQ / Redis for background tasks
* Advanced RAG strategies (re-ranking, multi-query, hybrid retrieval)
* Production deployment templates (Docker/K8s, monitoring, CI/CD)

---

## ⚡ Quickstart (v2.0.0)

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

Update `.env` with your API keys and **VECTOR\_DB\_PROVIDER** for switching DBs.

### 4. Run Services (Docker)

```bash
cd docker
cp .env.example .env   # update with credentials
docker-compose up -d
```

### 5. Run the Backend (from src root)

```bash
uvicorn main:app --reload
```

or with custom host/port:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

Access Swagger UI → [http://localhost:5000/docs](http://localhost:5000/docs)

---

## 🗺️ Roadmap (v2.0.0)

* [x] **Phase 1** – MongoDB + Qdrant baseline
* [x] **Alembic migrations with Postgres**
* [x] **Full PGVector migration + dual DB support**
* [x] **Orchestration improvements**
* [ ] Background tasks with Celery + Redis
* [ ] Advanced RAG methods (re-ranking, hybrid, multi-query)
* [ ] Production deployment templates (Docker/K8s, CI/CD)

---

## 🤝 Contributing

Fork, clone, and build along!
Ideas, PRs, and discussions are welcome as we evolve RagApp into a **production-grade RAG template**.

---

## 📄 License

MIT License – see [LICENSE](./LICENSE)

---

This version clearly communicates:

* Postgres + PGVector migration ✅
* Dual vector DB support (PGVector + Qdrant)
* Orchestration improvements
* Next steps (Celery + Redis, scaling)


