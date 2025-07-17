from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController , ProjectController
import os
import aiofiles
from models import ResponseSingle

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str,
    file: UploadFile,
    settings: Settings = Depends(get_settings)
):
    is_valid, result_signal =  DataController().validate(file=file)

    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={
                                    "message": result_signal
                                    })

    project_dir_path = ProjectController().get_project_path(project_id=project_id)

    file_path = os.path.join(project_dir_path,
                            file.filename)


    async with aiofiles.open(file_path, "wb") as f: 
        while chuck := await file.read(settings.FILE_DEFAULT_CHUNK_SIZE):
            await f.write(chuck)

    return JSONResponse(
                        content={
                            "message": ResponseSingle.FILE_UPLOAD_SUCCESS.value
                            })