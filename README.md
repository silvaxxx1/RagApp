# 🧠 RagApp – End-to-End Retrieval-Augmented Generation (RAG) System

**RagApp** is a full-stack, extensible project for building **Retrieval-Augmented Generation (RAG)** systems — from data ingestion to LLM-based responses and deployment.

---

<p align="center">
  <img src="ragapp.png" alt="RagApp Architecture" width="700"/>
</p>

---

## ✅ Highlights – Version 2.0.0 (v2)

1. **Full Migration to PostgreSQL + PGVector** ✅

   * MongoDB completely replaced.
   * PGVector now fully implemented for vector search.

2. **Dual Vector DB Support** 🟢

   * Qdrant remains fully functional alongside PGVector.
   * Developers can **switch between PGVector and Qdrant** easily via a single `.env` variable (`VECTOR_DB_PROVIDER`).
   * Unified interface ensures seamless vector DB operations.

3. **Orchestration & Performance Improvements** ⚡

   * Optimized async pipelines and indexing workflows.
   * Faster and more robust search and ingestion.

4. **Deployment Ready** 🚀

   * v2 backend is fully stable.
   * Next steps: integrate **Celery + Redis** for distributed tasks and scaling.

---

### 📦 Tech Stack (v2)

* FastAPI + Uvicorn (async-first)
* PostgreSQL + PGVector (primary vector DB)
* Qdrant (optional, fully supported)
* OpenAI, Ollama, Cohere, Sentence Transformers for embeddings
* Dockerized services
* Unified vector DB interface (PGVector ↔ Qdrant)

---

### ⚡ Quickstart

1. **Clone & Setup**

```bash
git clone https://github.com/silvaxxx1/RagApp.git
cd RagApp
```

2. **Install Dependencies**

```bash
uv init
uv add -r requirements.txt
```

3. **Configure Environment Variables**

```bash
cp uv.example .env
```

* Update `.env` for your API keys and set `VECTOR_DB_PROVIDER` to `pgvector` or `qdrant`.

4. **Run Services (Docker)**

```bash
cd docker
docker-compose up -d
```

5. **Run the Backend**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

Access Swagger UI: [http://localhost:5000/docs](http://localhost:5000/docs)

---

### 🗺️ Roadmap

* [x] Full migration to PostgreSQL + PGVector
* [x] Dual vector DB support (PGVector + Qdrant)
* [x] Unified DB interface for easy switching
* [x] Orchestration and async pipeline improvements
* [ ] Background tasks with Celery + Redis
* [ ] Advanced RAG strategies (re-ranking, hybrid, multi-query)
* [ ] Production deployment templates (Docker/K8s, CI/CD)

---


