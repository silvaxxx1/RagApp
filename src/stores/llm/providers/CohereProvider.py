from ..LLMInterface import LLMInterface 
import logging 
from ..LLMEnums import CohereEnums , DocTypeEnums
import cohere 

class CohereProviders(LLMInterface):
    def __init__(self,
                api_key : str,
                default_input_max_char : int = 1000,
                default_output_max_char : int = 1000,
                default_temperature : float = 0.1):

        self.api_key = api_key

        self.default_input_max_char = default_input_max_char
        self.default_output_max_char = default_output_max_char
        self.default_temperature = default_temperature 

        self.gen_model_id = None
        self.emb_model_id = None 
        self.emd_size = None 

        self.client = cohere.Client(api_key=self.api_key)
        
        self.logger = logging.getLogger(__name__) 

    def set_gen_model(self,model_id : str):
        self.gen_model_id = model_id

    def set_emb_model(self,model_id : str, emb_size : int):
        self.emb_model_id = model_id
        self.emd_size = emb_size

    def process_text(self,
                     text : str):
        return text[:self.default_input_max_char].strip()
    
    def generate_text(self,
                      prompt : str,
                      char_history: list=[],
                      max_output_tokens : int = None,
                      temperature : float = None):
        
        if not self.client:
            self.logger.error("Client for generation from Cohere is not initialized")
            return None
        
        if self.gen_model_id is None:
            self.logger.error("Generation model from Cohere is not set")
            return None 
        

        max_output_tokens = max_output_tokens if max_output_tokens  else self.default_output_max_char      
        temperature = temperature if temperature  else self.default_temperature
        
        response = self.client.chat(
                                    model = self.gen_model_id,
                                    chat_history = char_history,
                                    massage = self.process_text(prompt),
                                    temperature = temperature,
                                    max_tokens = max_output_tokens
                                    )
        
        
        if not response or not response.text :
            self.logger.error("Generation from Cohere failed")
            return None 
        
        return response.text[0].text 
    

    def embed_text(self,
                   text : str,
                   doc_type : str = None):
        if not self.client:
            self.logger.error("Client for embedding from OpenAI is not initialized")
            return None 
        
        if self.emb_model_id is None:
            self.logger.error("Embedding model is not set")
            return None 
        
        input_type = CohereEnums.DOCUMENT 
        if doc_type == DocTypeEnums.QUERY:
            input_type = CohereEnums.QUERY 

        response = self.client.embed(
            model=self.emb_model_id,
            texts=[self.process_text(text)],
            input_type=input_type,
            embedding_types=['float'],    
        )

        if not response or response.embeddings   or not response.embeddings.float:
            self.logger.error("Embedding from Cohere failed")
            return None
        
        return response.embeddings.float[0]
    
    def construct_prompt(self,
                         prompt : str,
                         role : str):
        return {
            "role" : role,
            "text" : self.process_text(prompt)
        }
            