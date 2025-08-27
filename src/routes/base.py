from fastapi import APIRouter, Depends
from helpers.config import get_settings, Settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

@base_router.get("/")
async def welcome(settings: Settings = Depends(get_settings)):
    
    app_name = settings.APP_NAME 
    app_version = settings.APP_VERSION

    return {
        "app_name": app_name,
        "app_version": app_version,
    }
