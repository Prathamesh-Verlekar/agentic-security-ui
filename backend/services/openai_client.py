"""
Thin wrapper around the OpenAI SDK.
"""

from openai import AsyncOpenAI

from backend.config import OPENAI_API_KEY, OPENAI_MODEL_NAME


def get_openai_client() -> AsyncOpenAI:
    """Return a configured async OpenAI client."""
    return AsyncOpenAI(api_key=OPENAI_API_KEY)


async def chat_completion(
    prompt: str, system: str = "", max_tokens: int = 2048
) -> str:
    """
    Send a single chat-completion request and return the assistant message.
    """
    client = get_openai_client()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model=OPENAI_MODEL_NAME,
        messages=messages,
        temperature=0.7,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content or ""
