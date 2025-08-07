from fastapi import FastAPI
from routes import base , data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings 
from stores.llm.LLMProviderFactory import LLMProviderFactory

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongodb_connec = AsyncIOMotorClient(get_settings().MONGODB_URL)
    app.mongodb = app.mongodb_connec[get_settings().MONGODB_DATABASE]  # database object
    llm_provider = LLMProviderFactory(settings)

    # generation_client 
    app_generation_client = llm_provider.create(provider=settings.GENERATION_BACKEND)
    app_generation_client.set_gen_model(model_id = settings.GENERATION_MODEL_ID)
    # embedding_client
    app.embedding_client = llm_provider.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_emb_model(model_id = settings.EMBEDDING_MODEL_ID, emb_size = settings.EMBEDDING_MODEL_SIZE)
@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_connec.close() 

app.include_router(base.base_router)
app.include_router(data.data_router) 