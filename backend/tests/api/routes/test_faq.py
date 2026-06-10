import io

from httpx import AsyncClient
import pytest
import json
from backend.app.core.config import settings


# @pytest.mark.asyncio
# async def test_create_faq(client: AsyncClient, normal_user_token_headers: dict[str, str]) -> None:
#     r = await client.post(f"{settings.API_V1_STR}/faqs", headers=normal_user_token_headers, json={'content':'xxx'})
#     assert 201 == r.status_code
#     data = r.json()
#     assert data
#     print(json.dumps(data, indent=4))

@pytest.mark.asyncio
async def test_upload_faq_csv_stream(client: AsyncClient, normal_user_token_headers: dict[str, str]):
    response = await client.post(
        f"{settings.API_V1_STR}/faqs/upload",
        headers=normal_user_token_headers,
        files={"file": ("test.csv", b"content\nhello\nfoo\n", "text/csv")},
    )
    assert response.status_code == 200

    # baca stream bertahap
    chunks = []
    async for chunk in response.aiter_text():
        chunks.append(chunk)
        print("chunk:", chunk)

    # pastikan ada progres bertahap
    assert any("data:" in c for c in chunks)
