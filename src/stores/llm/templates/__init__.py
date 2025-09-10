from fastapi import FastAPI
from routes import base, data, nlp
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProvidersFactory import VectorDBProvidersFactory
from stores.llm.templates.template_parser import TemplateParser
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

app = FastAPI()

async def startup_span():
    settings = get_settings()

    postgres_connec = (
        f"postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_MAIN_DATABASE}"
    )
    app.db_engine = create_async_engine(postgres_connec, echo=True, future=True)
    app.db_client = sessionmaker(
        app.db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    # --- LLM Clients ---
    llm_provider = LLMProviderFactory(settings)
    vectordb_provider_factory = VectorDBProvidersFactory(settings)

    app.generation_client = llm_provider.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_gen_model(model_id=settings.GENERATION_MODEL_ID)

    app.embedding_client = llm_provider.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_emb_model(
        model_id=settings.EMBEDDING_MODEL_ID,
        emb_size=settings.EMBEDDING_MODEL_SIZE
    )

    # --- Vector DB Client ---
    app.vectordb_client = vectordb_provider_factory.create(provider=settings.VECTOR_DB_BACKEND)
    app.vectordb_client.connect(distance_method=settings.VECTOR_DB_METHOD)

    # --- Template Parser ---
    app.template_parser = TemplateParser(
        language=settings.PRIMARY_LANG,
        default_language=settings.DEFAULT_LANG
    )

async def shutdown_span():
    await app.db_engine.dispose()
    app.vectordb_client.disconnect()

app.on_event("startup")(startup_span)
app.on_event("shutdown")(shutdown_span)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)
