from fastapi import APIRouter, status, Request 
from fastapi.responses import JSONResponse
from routes.schemes.nlp import PushRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from controllers import NLPController
from models import ResponseSingle
import logging 

logger = logging.getLogger("uvicorn.error")

nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags=["api_v1", "nlp"],
) 


@nlp_router.post("/index/push/{project_id}")
async def index_project(request: Request,
                         project_id: str,
                         push_request: PushRequest): 
    
    logger.info(f"Starting indexing for project_id: {project_id}")
    logger.info(f"do_reset flag: {push_request.do_reset}")

    project_model = await ProjectModel.create_instance(
        db_client=request.app.mongodb
    )
    chunk_model = await ChunkModel.create_instance(db_client=request.app.mongodb)
    
    project = await project_model.get_project_or_create(project_id=project_id) 

    # Log project.id type and value for debugging
    logger.info(f"Project ID type: {type(project.id)}")
    logger.info(f"Project ID value: {project.id}")

    if not project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": ResponseSingle.PROJECT_ID_ERROR.value}
        )

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client
    ) 

    has_record = True
    page_no = 1
    idx = 0
    total_inserted = 0

    while has_record:
        page_chunks = await chunk_model.get_project_chunk(
            project_id=project.id,
            page_no=page_no
        )
        
        logger.info(f"page_no={page_no}, chunks received: {len(page_chunks)}")

        if page_chunks:
            page_no += 1
        else:
            has_record = False
            break 

        chunks_ids = list(range(idx, idx + len(page_chunks)))
        idx += len(page_chunks)

        is_inserted =  nlp_controller.index_into_vectordb(
            project=project,
            chunks=page_chunks,
            do_reset=push_request.do_reset,
            chunks_ids=chunks_ids
        ) 

        if not is_inserted:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": ResponseSingle.INSERT_INTO_VECTOR_DB_ERROR.value}
            )
        
        total_inserted += len(page_chunks)

    return JSONResponse(
        content={
            "message": ResponseSingle.INSERT_INTO_VECTOR_DB_SUCCESS.value,
            "inserted_items_count": total_inserted
        }
    )
