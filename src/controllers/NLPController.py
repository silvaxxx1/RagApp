from .BaseController import BaseController 
from models.db_schemes import Project, DataChunk 
from stores.llm.LLMEnums import DocTypeEnums
from typing import List

class NLPController(BaseController): 

    def __init__(self,
                 vectordb_client,
                 generation_client,
                 embedding_client):
         
        super().__init__() 

        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client 

    def create_collection_name(self, project_id: str):
        return f"_collection_{project_id}".strip()
    
    def reset_vectordb_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)


    def get_vectordb_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.get_collection_info(collection_name=collection_name) 
    
    def index_into_vectordb(self, project: Project,
                            chunks: list[DataChunk],
                            chunks_ids: List[int],
                            do_reset: bool = False):
        
        collection_name = self.create_collection_name(project_id=project.project_id)

        texts = [c.chunk_text for c in chunks]  # Fixed typo here
        metadatas = [c.chunk_metadata for c in chunks]  # Fixed typo here

        vectors = [
            self.embedding_client.embed_text(text=text,
                                            doc_type=DocTypeEnums.DOCUMENT.value) 
            for text in texts
        ] 

        _ = self.vectordb_client.create_collection(
            collection_name=collection_name,
            do_reset=do_reset,
            embedding_size=self.embedding_client.emb_size
        )

        _ = self.vectordb_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            vectors=vectors,
            metadata=metadatas,
            record_ids=chunks_ids,
        )

        return True
