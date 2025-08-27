from abc import ABC, abstractmethod 


class LLMInterface(ABC):
    @abstractmethod
    def set_gen_model(self,
                      model_id : str):
        pass 

    @abstractmethod
    def set_emb_model(self,
                      model_id : str,
                      emb_size : int):
        pass 
    
    @abstractmethod
    def generate_text(self,
                      prompt : str,
                      char_history: list=[],
                      max_output_tokens : int = None,
                      temperature : float = None):
        pass 

    @abstractmethod
    def embed_text(self,
                   text : str,
                   doc_type : str = None):
        pass 

    @abstractmethod
    def construct_prompt(self,
                      prompt : str,
                      role : str):
        pass 

