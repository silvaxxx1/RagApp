from fastapi import APIRouter, status, Request 
from fastapi.responses import JSONResponse

import logging 

logger = logging.getLogger("uvicorn.error")

nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags=["api_v1", "nlp"],
) 
