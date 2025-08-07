from ..LLMInterface import LLMInterface 
from openai import OpenAI
import logging 
from ..LLMEnums import OpenAIEnums

class OpenAIProviders(LLMInterface):
    def __init__(self,
                api_key : str,
                api_url : str = None,
                default_input_max_char : int = 1000,
                default_output_max_char : int = 1000,
                default_temperature : float = 0.1):

        self.api_key = api_key
        self.api_url = api_url

        self.default_input_max_char = default_input_max_char
        self.default_output_max_char = default_output_max_char
        self.default_temperature = default_temperature 

        self.gen_model_id = None
        self.emb_model_id = None 
        self.emd_size = None 

        self.client = OpenAI(api_key=self.api_key,
                            api_base=self.api_url
                            ) 
        
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
            self.logger.error("Client for generation from OpenAI is not initialized")
            return None
        
        if self.gen_model_id is None:
            self.logger.error("Generation model is not set")
            return None 
        
        max_output_tokens = max_output_tokens if max_output_tokens  else self.default_output_max_char      
        temperature = temperature if temperature  else self.default_temperature

        char_history.append(self.construct_prompt(prompt=prompt,
                                                  role=OpenAIEnums.USER.value))
        
        response = self.client.chat.completions.create(
                                            model = self.gen_model_id,
                                            messages = char_history,
                                            max_tokens = max_output_tokens,
                                            temperature = temperature
                                        )
        
        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message.content:
            self.logger.error("Generation from OpenAI failed")
            return None 
        
        char_history.append(self.construct_prompt(prompt=response.choices[0].message.content,
                                                  role=OpenAIEnums.ASSISTANT.value))
        
        return response.choices[0].message["content"]
        

    def embed_text(self,
                   text : str,
                   doc_type : str = None):
        if not self.client:
            self.logger.error("Client for embedding from OpenAI is not initialized")
            return None 
        
        if self.emb_model_id is None:
            self.logger.error("Embedding model is not set")
            return None 
        
        response = self.client.embedding.create(
                                                input = text,
                                                model = self.emb_model_id
                                            )
        
        if not response or response.data or len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("Embedding from OpenAI failed")
            return None 
        
        return response.data[0].embedding 
    

    def construct_prompt(self,
                         prompt : str,
                         role : str):
        return {
            "role" : role,
            "content" : self.process_text(prompt)
        }
            
    



        


        

        


