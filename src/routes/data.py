from fastapi import APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
import aiofiles
from models import ResponseSingle
import logging
from .schemes.data import ProcessResponse
from models.ProjectModel import ProjectModel
from models.db_schemes import DataChunk
from models.ChunkModel import ChunkModel

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)


@data_router.post("/upload/{project_id}")
async def upload_data(
    request: Request,
    project_id: str,
    file: UploadFile,
    settings: Settings = Depends(get_settings)
):
    project_model = await ProjectModel.create_instance(db_client=request.app.mongodb)
    project = await project_model.get_project_or_create(project_id=project_id)

    data_controller = DataController()
    is_valid, result_signal = data_controller.validate(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": result_signal}
        )

    project_dir_path = ProjectController().get_project_path(project_id=project_id)

    file_path, file_id = data_controller.generate_filepath(
        org_filename=file.filename,
        project_id=project_id
    )

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chuck := await file.read(settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chuck)
    except Exception as e:
        logger.error(f"error while uploading file: {e}")

    return JSONResponse(
        content={
            "message": ResponseSingle.FILE_UPLOAD_SUCCESS.value,
            "file_id": file_id,
        }
    )


@data_router.post("/process/{project_id}")
async def process_endpoint(
    project_id: str,
    request: Request,
    process_request: ProcessResponse,
):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    project_model = await ProjectModel.create_instance(db_client=request.app.mongodb)
    project = await project_model.get_project_or_create(project_id=project_id)
    

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
            content={"message": ResponseSingle.PROCESSING_FAILED.value}
        )

    file_chunk_records = [
        DataChunk(
            chunk_text=chunk.page_content,
            chuck_metadata=chunk.metadata,
            chunk_order=i + 1,
            chuck_project_id=project.id,
        )
        for i, chunk in enumerate(file_chunks)
    ]

    chunk_model = await ChunkModel.create_instance(db_client=request.app.mongodb)

    if do_reset == 1:
        _= await chunk_model.delete_chunk_by_id(project_id=project.id)

    no_records = await chunk_model.get_many_chunks(chuncks=file_chunk_records)  # ✅ FIXED

    return JSONResponse(
        content={
            "message": ResponseSingle.PROCESSING_SUCCESS.value,
            "inserted_chunks": no_records
        }
    )
