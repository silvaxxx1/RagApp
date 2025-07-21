from fastapi import FastAPI


from routes import base , data

from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings, Settings

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_connec = AsyncIOMotorClient(get_settings().MONGODB_URL)
    app.mongodb = app.mongodb_connec[get_settings().MONGODB_DATABASE]  # database object


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_connec.close() 

app.include_router(base.base_router)
app.include_router(data.data_router) 
