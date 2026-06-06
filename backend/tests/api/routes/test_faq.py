from httpx import AsyncClient
import pytest
import json
from backend.app.core.config import settings


@pytest.mark.asyncio
async def test_create_faq(client: AsyncClient, normal_user_token_headers: dict[str, str]) -> None:
    r = await client.post(f"{settings.API_V1_STR}/faqs", headers=normal_user_token_headers, json={'content':'xxx'})
    assert 201 == r.status_code
    data = r.json()
    assert data
    print(json.dumps(data, indent=4))
