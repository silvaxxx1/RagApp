from .LLMEnums import LLMEnums
from .providers import( 
         OpenAIProvider,
        OpenSourceEmbeddingsProvider ,
        CoHereProvider ) # 👈 add

class LLMProviderFactory:
    def __init__(self, config: dict):
        self.config = config

    def create(self, provider: str):
        if provider == LLMEnums.OPENAI.value:
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_API_URL,
                default_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens=self.config.GENERATION_DAFAULT_MAX_TOKENS,
                default_generation_temperature=self.config.GENERATION_DAFAULT_TEMPERATURE
            )

        if provider == LLMEnums.COHERE.value:
            return CoHereProvider(
                api_key=self.config.COHERE_API_KEY,
                default_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens=self.config.GENERATION_DAFAULT_MAX_TOKENS,
                default_generation_temperature=self.config.GENERATION_DAFAULT_TEMPERATURE
            )

        if provider == LLMEnums.OPEN_SOURCE_EMBEDDINGS.value:  # 👈 new
            return OpenSourceEmbeddingsProvider(
                model_id=self.config.EMBEDDING_MODEL_ID,
                emb_size=self.config.EMBEDDING_MODEL_SIZE,
                default_input_max_char=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                default_output_max_char=self.config.GENERATION_DAFAULT_MAX_TOKENS,
                default_temperature=self.config.GENERATION_DAFAULT_TEMPERATURE
            )

        return None
