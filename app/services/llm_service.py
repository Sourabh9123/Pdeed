from openai import AsyncOpenAI, OpenAIError
import json
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def analyze_document_text(text: str) -> dict:
    if not text.strip():
        raise ValueError("Document text cannot be empty.")

    prompt = f"""
    Analyze the following document text and provide a brief summary and extract key entities.
    Respond strictly in JSON format with two keys: 'summary' (string) and 'entities' (list of objects with 'text' and 'label' keys).

    Document Text:
    {text}
    """
    
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response received from LLM.")
            
        return json.loads(content)
        
    except OpenAIError as e:
        logger.error(f"OpenAI API Error: {str(e)}")
        raise RuntimeError(f"OpenAI service encountered an error: {str(e)}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from response: {str(e)} Content: {content}")
        raise RuntimeError("Invalid response format received from AI model.")
    except Exception as e:
        logger.exception("Unexpected error in document analysis.")
        raise RuntimeError("An unexpected error occurred during document analysis.")
