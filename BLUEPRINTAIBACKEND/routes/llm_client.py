import json
from openai import OpenAI

from config import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_structured_json(system_prompt: str, user_prompt: str) -> dict:
    if not settings.OPENAI_API_KEY:
        return {}

    response = client.responses.create(
        model=settings.OPENAI_MODEL,
        instructions=system_prompt,
        input=user_prompt,
    )

    text = response.output_text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw_text": text}
