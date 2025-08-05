from fastapi import APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
import aiofiles
from models import ResponseSingle
import logging
from .schemes.data import ProcessResponse
from models.ProjectModel import ProjectModel
from models.db_schemes import DataChunk , Asset
from models.ChunkModel import ChunkModel
from models.AssetModel import AssetModel
from models.enums.AssetTypeEnum import AssetTypeEnum
import os

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
        async with aiofiles.open(file_path, "wb") as f: # aiofiles is asynchronous
            while chuck := await file.read(settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chuck)
    except Exception as e:
        logger.error(f"error while uploading file: {e}")

    # store asset to db
    asset_model = await AssetModel.create_instance(db_client=request.app.mongodb)

    asset_resource = Asset(
        asset_project_id=project.id,
        asset_type=AssetTypeEnum.FILE.value,
        asset_name=file_id,
        asset_size=os.path.getsize(file_path),
    )


    asset_record = await asset_model.create_asset(asset=asset_resource) 

    return JSONResponse(
        content={
            "message": ResponseSingle.FILE_UPLOAD_SUCCESS.value,
            "file_id": file_id, # be careful with this ObjectId to string conversion
        }
    )


@data_router.post("/process/{project_id}")
async def process_endpoint(
    project_id: str,
    request: Request,
    process_request: ProcessResponse,
):
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    project_model = await ProjectModel.create_instance(db_client=request.app.mongodb)
    project = await project_model.get_project_or_create(project_id=project_id)
    

    asset_model = await AssetModel.create_instance(
                          db_client=request.app.mongodb
                                                      ) 
    
    project_files_ids = {}
    if process_request.file_id :
        asset_record = await asset_model.get_asset_record(asset_project_id=project.id,
                                                         asset_name=process_request.file_id)
       
        if asset_record is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": ResponseSingle.FILE_ID_ERROR.value}
            )
       
       
        project_files_ids = {
            asset_record.id: asset_record.asset_name
        }
    else:
        
        
        project_files = await asset_model.get_all_project_asset(
            asset_project_id=project.id,
            asset_type=AssetTypeEnum.FILE.value
        ) 
        project_files_ids = {
            record.id: record.asset_name
            for record in project_files
        }
    
    if len(project_files_ids) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": ResponseSingle.NO_FILE_ERROR.value}
        )


    process_controller = ProcessController(project_id=project_id)

    no_records = 0
    no_files = 0 

    chunk_model = await ChunkModel.create_instance(db_client=request.app.mongodb)
    if do_reset == 1:
            _= await chunk_model.delete_chunk_by_id(project_id=project.id)


    for  asset_id ,file_id in project_files_ids.items():
        file_content = process_controller.get_file_content(file_id=file_id)
            

        if file_content is None:
            return logger.error(f"error while processing file: {file_id}")
            continue

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
                chunk_asset_id=asset_id
            )
            for i, chunk in enumerate(file_chunks)
        ]


        no_records += await chunk_model.get_many_chunks(chuncks=file_chunk_records)  # ✅ FIXED
        no_files += 1 

    return JSONResponse(
        content={
            "message": ResponseSingle.PROCESSING_SUCCESS.value,
            "inserted_chunks": no_records,
            "processed_files": no_files
        }
    )
