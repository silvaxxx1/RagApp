from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from routes.schemes.nlp import PushRequest, SearchRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from controllers import NLPController
from models import ResponseSingle
import logging
from tqdm.auto import tqdm

logger = logging.getLogger("uvicorn.error")

nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags=["api_v1", "nlp"],
)


@nlp_router.post("/index/push/{project_id}")
async def index_project(
    request: Request,
    project_id: int,
    push_request: PushRequest,
):
    logger.info(f"Starting indexing for project_id: {project_id}")
    logger.info(f"do_reset flag: {push_request.do_reset}")

    # Initialize models
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)

    # Get or create project
    project = await project_model.get_project_or_create(project_id=project_id)
    if not project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": ResponseSingle.PROJECT_ID_ERROR.value},
        )

    # Initialize NLPController
    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        template_parser=request.app.template_parser,
    )

    # Create or reset collection
    collection_name = nlp_controller.create_collection_name(project_id=project_id)
    await request.app.vectordb_client.create_collection(
        collection_name=collection_name,
        embedding_size=request.app.embedding_client.embedding_size,
        do_reset=push_request.do_reset,
    )

    # Get total chunk count as int
    total_chunk_count = await chunk_model.get_total_chunk_count(project_id=project_id)
    logger.info(f"Total chunks to index: {total_chunk_count}")

    # Initialize async-friendly tqdm
    pbar = tqdm(total=total_chunk_count, desc="Indexing...", position=0)

    has_record = True
    page_no = 1
    idx = 0
    total_inserted = 0

    while has_record:
        # Fetch paginated chunks
        page_chunks = await chunk_model.get_project_chunk(
            project_id=project_id, page_no=page_no
        )
        logger.info(f"page_no={page_no}, chunks received: {len(page_chunks)}")

        if not page_chunks:
            break

        page_no += 1

        chunks_ids = [c.chunk_id for c in page_chunks]
        idx += len(page_chunks)

        # Index chunks into vectordb
        is_inserted = await nlp_controller.index_into_vectordb(
            project=project,
            chunks=page_chunks,
            chunks_ids=chunks_ids,
        )

        if not is_inserted:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": ResponseSingle.INSERT_INTO_VECTOR_DB_ERROR.value},
            )

        # Remove await here
        pbar.update(len(page_chunks))
        total_inserted += len(page_chunks)

    # Remove await here too
    pbar.close()



@nlp_router.get("/index/info/{project_id}")
async def get_project_index_info(request: Request, project_id: int):
    # Pass the sessionmaker directly, not a created session
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create(project_id=project_id)

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        template_parser=request.app.template_parser,
    )

    collection_info = await nlp_controller.get_vector_db_collection_info(project=project)
    return JSONResponse(
        content={
            "message": ResponseSingle.VECTORDB_COLLECTION_RETRIEVED.value,
            "collection_info": collection_info,
        }
    )


@nlp_router.post("/index/search/{project_id}")
async def search_index(request: Request, project_id: int, search_request: SearchRequest):
    # Pass the sessionmaker directly, not a created session
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create(project_id=project_id)

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        template_parser=request.app.template_parser,
    )

    results = await nlp_controller.search_vector_db_collection(
        project=project,
        text=search_request.text,
        limit=search_request.limit,
    )

    if not results:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": ResponseSingle.VECTORDB_COLLECTION_RETRIEVAL_ERROR.value
            },
        )

    return JSONResponse(
        content={
            "message": ResponseSingle.VECTORDB_COLLECTION_RETRIEVED.value,
            "results": [result.dict() for result in results],
        }
    )


@nlp_router.post("/index/answer/{project_id}")
async def answer_rag(request: Request, project_id: int, search_request: SearchRequest):
    # Pass the sessionmaker directly, not a created session
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create(project_id=project_id)

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        template_parser=request.app.template_parser,
    )

    answer, full_prompt, chat_history = await nlp_controller.answer_rag_query(
        project=project,
        query=search_request.text,
        limit=search_request.limit,
    )

    if not answer:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": ResponseSingle.RAG_ANSWER_FAILED.value},
        )

    return JSONResponse(
        content={
            "message": ResponseSingle.RAG_ANSWER_SUCCESS.value,
            "answer": answer,
            "full_prompt": full_prompt,
            "chat_history": chat_history,
        }
    )