# src/stores/llm/providers/OpenSourceEmbeddingsProvider.py

from abc import ABC
from sentence_transformers import SentenceTransformer
from ..LLMInterface import LLMInterface
import torch

class OpenSourceEmbeddingsProvider(LLMInterface, ABC):
    def __init__(self,
                 model_id: str = "intfloat/e5-large-v2",
                 emb_size: int = 1024,
                 default_input_max_char: int = 1000,
                 default_output_max_char: int = 1000,
                 default_temperature: float = 0.1):

        self.model_id = model_id
        self.emb_size = emb_size
        self.default_input_max_char = default_input_max_char
        self.default_output_max_char = default_output_max_char
        self.default_temperature = default_temperature

        self._load_model(model_id)

    def _load_model(self, model_id: str):
        """Load model with automatic GPU fallback."""
        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"[OpenSourceEmbeddingsProvider] Loading model '{model_id}' on {device}...")
            self.model = SentenceTransformer(model_id, device=device)
        except Exception as e:
            print(f"[OpenSourceEmbeddingsProvider] GPU load failed, falling back to CPU. Error: {e}")
            self.model = SentenceTransformer(model_id, device="cpu")

    def set_gen_model(self, model_id: str):
        # No generation model for embeddings-only provider
        pass

    def set_emb_model(self, model_id: str, emb_size: int):
        self.model_id = model_id
        self.emb_size = emb_size
        self._load_model(model_id)

    def generate_text(self, prompt: str, char_history: list = [],
                      max_output_tokens: int = None, temperature: float = None):
        raise NotImplementedError("This provider only supports embeddings.")

    def embed_text(self, text: str, doc_type: str = None):
        if isinstance(text, list):
            return self.model.encode(text, normalize_embeddings=True).tolist()
        return self.model.encode([text], normalize_embeddings=True)[0].tolist()

    def construct_prompt(self, prompt: str, role: str):
        return prompt
