from fastapi import APIRouter, Depends ,  UploadFile
from helpers.config import get_settings, Settings
from controllers import DataController
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(prjoect_id: str,
                    file: UploadFile,
                    settings: Settings = Depends(get_settings)
                    ):

    is_valid = DataController().validate(file = file)
    return is_valid