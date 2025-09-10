
from ..LLMInterface import LLMInterface
from ..LLMEnums import CoHereEnums, DocTypeEnums
import cohere
import logging
from typing import List, Union

class CoHereProvider(LLMInterface):

    def __init__(self, api_key: str,
                       default_input_max_characters: int=1000,
                       default_generation_max_output_tokens: int=1000,
                       default_generation_temperature: float=0.1):
        
        self.api_key = api_key
        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = cohere.Client(api_key=self.api_key)
        self.logger = logging.getLogger(__name__)

    def set_gen_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_emb_model(self, model_id: str, emb_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = emb_size

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list = [], max_output_tokens: int = None,
                      temperature: float = None):
        if not self.client or not self.generation_model_id:
            self.logger.error("CoHere client or generation model not set")
            return None

        max_output_tokens = max_output_tokens or self.default_generation_max_output_tokens
        temperature = temperature or self.default_generation_temperature

        response = self.client.chat(
            model = self.generation_model_id,
            chat_history = chat_history,
            message = self.process_text(prompt),
            temperature = temperature,
            max_tokens = max_output_tokens
        )

        if not response or not response.text:
            self.logger.error("Error while generating text with CoHere")
            return None

        return response.text

    def embed_text(self, text: Union[str, List[str]], doc_type: str = None):
        if not self.client or not self.embedding_model_id:
            self.logger.error("CoHere client or embedding model not set")
            return None

        if isinstance(text, str):
            text = [text]

        input_type = CoHereEnums.DOCUMENT
        if doc_type == DocTypeEnums.QUERY:
            input_type = CoHereEnums.QUERY

        response = self.client.embed(
            model = self.embedding_model_id,
            texts = [self.process_text(t) for t in text],
            input_type = input_type,
            embedding_types=['float'],
        )

        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("Error while embedding text with CoHere")
            return None

        return [f for f in response.embeddings.float]

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": prompt,
        }
