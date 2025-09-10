# src/stores/llm/providers/OpenSourceEmbeddingsProvider.py

from abc import ABC
from sentence_transformers import SentenceTransformer
from ..LLMInterface import LLMInterface
import torch
import logging
from typing import List, Union
import math

class OpenSourceEmbeddingsProvider(LLMInterface, ABC):
    def __init__(self,
                 model_id: str = "intfloat/e5-large-v2",
                 emb_size: int = 1024,
                 default_input_max_char: int = 1000,
                 default_output_max_char: int = 1000,
                 default_temperature: float = 0.1,
                 batch_size: int = 64):
        """
        Open-source embedding provider using SentenceTransformers.
        """
        self.model_id = model_id
        self.embedding_size = emb_size
        self.default_input_max_char = default_input_max_char
        self.default_output_max_char = default_output_max_char
        self.default_temperature = default_temperature
        self.batch_size = batch_size

        self.logger = logging.getLogger(__name__)
        self._load_model(model_id)

    def _load_model(self, model_id: str):
        """Load model with automatic GPU fallback."""
        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.logger.info(f"[OpenSourceEmbeddingsProvider] Loading model '{model_id}' on {device}...")
            self.model = SentenceTransformer(model_id, device=device)
        except Exception as e:
            self.logger.warning(f"[OpenSourceEmbeddingsProvider] GPU load failed, falling back to CPU. Error: {e}")
            self.model = SentenceTransformer(model_id, device="cpu")

    def set_gen_model(self, model_id: str):
        """No generation model for embeddings-only provider"""
        pass

    def set_emb_model(self, model_id: str, emb_size: int):
        self.model_id = model_id
        self.emb_size = emb_size
        self._load_model(model_id)

    def generate_text(self, prompt: str, chat_history: list = [],
                      max_output_tokens: int = None, temperature: float = None):
        raise NotImplementedError("This provider only supports embeddings.")

    def _chunk_text(self, text: str, max_len: int = None) -> List[str]:
        """
        Split text into chunks if longer than max_len.
        """
        max_len = max_len or self.default_input_max_char
        if len(text) <= max_len:
            return [text]
        return [text[i:i + max_len] for i in range(0, len(text), max_len)]

    def embed_text(self, text: Union[str, List[str]], doc_type: str = None, batch_size: int = None) -> Union[List[float], List[List[float]]]:
        """
        Embed single text or list of texts in batch-safe way.
        """
        batch_size = batch_size or self.batch_size

        # Normalize input to list
        if isinstance(text, str):
            texts = self._chunk_text(text)
        else:
            # Chunk each text if too long
            texts = []
            for t in text:
                texts.extend(self._chunk_text(t))

        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_emb = self.model.encode(batch, normalize_embeddings=True, device=self.model.device)
            embeddings.extend(batch_emb.tolist())

        # Return single embedding if original input was string
        if isinstance(text, str):
            # Average embeddings if multiple chunks
            if len(embeddings) == 1:
                return embeddings[0]
            avg_emb = [sum(x) / len(embeddings) for x in zip(*embeddings)]
            return avg_emb

        return embeddings

    def construct_prompt(self, prompt: str, role: str):
        return prompt
