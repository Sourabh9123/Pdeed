from openai import AsyncOpenAI, OpenAIError
import json
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

class LLMService:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = settings.OPENAI_MODEL
            LLMService._initialized = True

    async def analyze_document_text(self, text: str) -> dict:
        if not text.strip():
            raise ValueError("Document text cannot be empty.")

        prompt = f"""
        Analyze the following document text and extract detailed intelligence.
        Respond strictly in JSON format with the following structure:
        - 'document_type' (string): Best guess at the type of document (e.g., Article, Resume, Invoice, Contract, Email, Letter, etc.).
        - 'language' (string): The primary language of the document.
        - 'summary' (string): A concise but comprehensive summary.
        - 'key_themes' (list of strings): 3 to 5 core topics or themes discussed.
        - 'entities' (list of objects): Key entities with 'text' and 'label' (e.g., Person, Organization, Location, Date).
        - 'sentiment' (string): The overall tone of the document (e.g., Positive, Negative, Neutral, Formal, Urgent).
        - 'action_items' (list of strings): Any clear action items, tasks, or follow-ups mentioned (return an empty list if none).

        Document Text:
        {text}
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response received from LLM.")
                
            result = json.loads(content)
                
            return result
            
        except OpenAIError as e:
            logger.error(f"OpenAI API Error: {str(e)}")
            raise RuntimeError(f"OpenAI service encountered an error: {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON from response: {str(e)} Content: {content}")
            raise RuntimeError("Invalid response format received from AI model.")
        except Exception as e:
            logger.exception("Unexpected error in document analysis.")
            raise RuntimeError("An unexpected error occurred during document analysis.")

llm_service = LLMService()
