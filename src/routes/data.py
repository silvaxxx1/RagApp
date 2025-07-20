from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController , ProjectController, ProcessController
import aiofiles
from models import ResponseSingle
import logging 
from .schemes.data import ProcessResponse

logger = logging.getLogger("uvicorn.error")

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
    data_controller = DataController()
    is_valid, result_signal =  data_controller.validate(file=file)

    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={
                                    "message": result_signal
                                    })

    project_dir_path = ProjectController().get_project_path(project_id=project_id)

    file_path , file_id = data_controller.generate_filepath(
        org_filename=file.filename,
        project_id=project_id
    )

    try:
        async with aiofiles.open(file_path, "wb") as f: 
            while chuck := await file.read(settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chuck)

    except Exception as e:
        logger.error(f"errror while uploading file :{e}")

    return JSONResponse(
                        content={
                            "message": ResponseSingle.FILE_UPLOAD_SUCCESS.value,
                            "file_id": file_id
                            })  


@data_router.post("/process/{project_id}")
async def process_endpoint(
    project_id: str,
    process_request: ProcessResponse,
                        ):
    file_id = process_request.file_id 
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size

    process_controller = ProcessController(project_id=project_id)
    file_content = process_controller.get_file_content(file_id=file_id)
    
    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": ResponseSingle.PROCESSING_FAILED.value,
                }
        ) 
    
    return file_chunks