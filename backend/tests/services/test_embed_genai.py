
from app.core.config import settings
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def embed_flow(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
        dimensions=384,
        embedding_format="float",
    )
    return response.data[0].embedding


def test_embed_genai() -> None:
    result = embed_flow("Hello, my dog is cute")
    print(result)