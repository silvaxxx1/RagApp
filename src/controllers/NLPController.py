from .BaseController import BaseController 
from models.db_schemes import Project, DataChunk 
from stores.llm.LLMEnums import DocTypeEnums
from typing import List
import json 

class NLPController(BaseController): 

    def __init__(self,
                 vectordb_client,
                 generation_client,
                 embedding_client,
                 template_parser):
         
        super().__init__() 

        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client 
        self.template_parser = template_parser

    def create_collection_name(self, project_id: str):
        return f"_collection_{project_id}".strip()
    
    def reset_vectordb_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)


    def get_vectordb_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name=collection_name)
        
        return json.dumps(collection_info,
                          default=lambda x: x.__dict__) 
    
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


    def search_vector_db_collection(self, project: Project, text: str, limit: int = 10):
        
        # get collection name 
        collection_name = self.create_collection_name(project_id=project.project_id)



        # get text embedding vector 
        vector = self.embedding_client.embed_text(text=text,
                                                doc_type=DocTypeEnums.QUERY.value)
        
        if not vector or len(vector) == 0:
            return False
        # do semantic search in vector db 
        results = self.vectordb_client.search_by_vector(collection_name=collection_name,
                                                        vector=vector,
                                                        limit=limit)
        if not results :
            return False
        
        return results 
    
    def answer_rag_query(self, project: Project, query: str, limit: int = 10):
        
        answer, full_prompt, chat_history = None, None, None
        # do semantic search in vector db 
        retrived_docs = self.search_vector_db_collection(project=project,
                                                        text=query,
                  
                                                        limit=limit)
        
        if not retrived_docs or len(retrived_docs) == 0:
            return answer, full_prompt, chat_history  
        

        system_prompt = self.template_parser.get("rag", "system_prompt")
        document_prompt = "\n".join([

            self.template_parser.get("rag", "document_prompt", {
                "doc_num": idx + 1,
                "chunk_text": self.generation_client.process_text(doc.text),
                })
            for idx, doc in enumerate(retrived_docs)
        ])
         
        # This is the line that needs to be changed.
        # Pass the 'query' variable to the template parser here.
        footer_prompt = self.template_parser.get("rag", "footer_prompt", {"query": query})


        chat_history = [
            self.generation_client.construct_prompt(
                prompt=system_prompt,
                role=self.generation_client.enums.SYSTEM.value,
            )
        ]

        full_prompt = "\n\n".join([
            document_prompt,
            footer_prompt
        ])
        
        answer = self.generation_client.generate_text(
            prompt=full_prompt,
            char_history=chat_history,
        ) 

        return answer, full_prompt, chat_history 