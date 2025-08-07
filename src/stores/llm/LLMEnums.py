from enum import Enum 


class LLMEnums(Enum):
    OPENAI = "openai" 
    COHERE = "cohere" 

    
class OpenAIEnums(Enum):
    SYSTEM = "system" 
    USER = "user" 
    ASSISTANT = "assistant" 

class CohereEnums(Enum):
    SYSTEM = "SYSTEM" 
    USER = "USER" 
    ASSISTANT = "CHATBOT" 

    DOCUMENT = "search_document"
    QUERY = "search_query"

class DocTypeEnums(Enum):
    QUERY = "query" 
    DOCUMENT = "document"