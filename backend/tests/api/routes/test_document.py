import pytest
from httpx import AsyncClient
from unittest.mock import patch
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from app.utils import generate_password_reset_token
from app.core.config import settings
from app.api.deps import get_user_service
from app.models.user import UserCreate

from tests.helpers.util import random_email, random_lower_string
import json
@pytest.mark.asyncio
async def test_crud_documents(client: AsyncClient) -> None:
     # kirim dokumen
    await client.post(f"{settings.API_V1_STR}/documents", json={"content": "hello sayangkuass"})


    #test
    r = await client.get(f"{settings.API_V1_STR}/documents")

    js = r.json()
    print(json.dumps(js, indent=4))

