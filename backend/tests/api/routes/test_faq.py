from httpx import AsyncClient
import pytest

from backend.app.core.config import settings


@pytest.mark.asyncio
async def test_create_faq(client: AsyncClient, normal_user_token_headers: dict[str, str]) -> None:
    r = await client.post(f"{settings.API_V1_STR}/faqs", headers=normal_user_token_headers, json={'content':'xxx'})
    assert 201 == r.status_code