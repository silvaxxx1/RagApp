from enum import Enum 


class LLMEnums(Enum):
    OPENAI = "openai" 
    COHERE = "cohere" 
    OPEN_SOURCE_EMBEDDINGS = "open_source_embeddings"  # 👈 new


    
class OpenAIEnums(Enum):
    SYSTEM = "system" 
    USER = "user" 
    ASSISTANT = "assistant" 

class CoHereEnums(Enum):
    SYSTEM = "SYSTEM" 
    USER = "USER" 
    ASSISTANT = "CHATBOT" 

    DOCUMENT = "search_document"
    QUERY = "search_query"

class DocTypeEnums(Enum):
    QUERY = "query" 
    DOCUMENT = "document"