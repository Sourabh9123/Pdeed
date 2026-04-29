from openai import AsyncOpenAI
import json
from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def analyze_document_text(text: str) -> dict:
    prompt = f"""
    Analyze the following document text and provide a brief summary and extract key entities.
    Respond strictly in JSON format with two keys: 'summary' (string) and 'entities' (list of objects with 'text' and 'label' keys).

    Document Text:
    {text}
    """
    
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
        ]
    )
    
    content = response.choices[0].message.content
    return json.loads(content)
