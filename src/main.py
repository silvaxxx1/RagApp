from fastapi import FastAPI
from routes import base , data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings 
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProvidersFactory import VectorDBProvidersFactory
app = FastAPI()

async def startup_span():
    settings = get_settings()
    app.mongodb_connec = AsyncIOMotorClient(get_settings().MONGODB_URL)
    app.mongodb = app.mongodb_connec[get_settings().MONGODB_DATABASE]  # database object
    llm_provider = LLMProviderFactory(settings)
    vectordb_provider_factory = VectorDBProvidersFactory(settings) 


    # generation_client 
    app_generation_client = llm_provider.create(provider=settings.GENERATION_BACKEND)
    app_generation_client.set_gen_model(model_id = settings.GENERATION_MODEL_ID)
    # embedding_client
    app.embedding_client = llm_provider.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_emb_model(model_id = settings.EMBEDDING_MODEL_ID, emb_size = settings.EMBEDDING_MODEL_SIZE)
    app.vectordb_client = vectordb_provider_factory.create(provider=settings.VECTOR_DB_BACKEND)
    app.vectordb_client.connect() 

async def shutdown_span():
    app.mongodb_connec.close()  
    app.vectordb_client.disconnect() 

app.on_event("startup")(startup_span)
app.on_event("shutdown")(shutdown_span)

app.include_router(base.base_router)
app.include_router(data.data_router) 