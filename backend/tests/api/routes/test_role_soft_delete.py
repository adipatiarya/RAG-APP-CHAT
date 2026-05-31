import json

from faker import Faker
import pytest
from httpx import AsyncClient
import pytest_asyncio
from app.core.config import settings

from app.api.deps import get_role_service, get_user_service
from app.models.role import RoleCreate
from app.models.user import UserCreate
from tests.helpers.util import random_lower_string
from app.utils import logger



@pytest_asyncio.fixture(scope="function")
async def role_id_to_deleted(client: AsyncClient, normal_user_token_headers: dict[str, str]) -> None:
    role_name  = random_lower_string()
    payload = {
        "name": role_name,
        "description": "string",
        "permission": {
            "user": {
                "can_create_user": False,
                "can_delete_user": True,
                "can_update_user": False,
                "can_view_user": False
            },
            "role": {
                "can_create_role": False,
                "can_delete_role": False,
                "can_update_role": False,
                "can_view_role": False
            }
        }
    }

    r = await client.post(f"{settings.API_V1_STR}/roles", headers=normal_user_token_headers, json=payload)
    assert 201 == r.status_code
    resp = r.json()
    return resp['id']

@pytest.mark.asyncio
async def test_delete_role_soft_hard(client: AsyncClient, normal_user_token_headers: dict[str, str], role_id_to_deleted) -> None:
    
    id = role_id_to_deleted
    
    #periksa
    r = await client.get(f"{settings.API_V1_STR}/roles/{id}", headers=normal_user_token_headers)
    assert 200 == r.status_code
    data = r.json()
    #assert "deleted_at" in data
    assert data["deleted_at"] is None


    #aksi
    r = await client.delete(f"{settings.API_V1_STR}/roles/{id}?hard=no", headers=normal_user_token_headers)
    assert 204 == r.status_code

    #cek soft
    r = await client.get(f"{settings.API_V1_STR}/roles/{id}", headers=normal_user_token_headers)
    assert 200 == r.status_code
    data = r.json()
    assert data
    assert "deleted_at" in data
    assert data["deleted_at"] is not None


    #aksi
    r = await client.delete(f"{settings.API_V1_STR}/roles/{id}", headers=normal_user_token_headers)
    assert 204 == r.status_code

    #cek hard
    r = await client.get(f"{settings.API_V1_STR}/roles/{id}", headers=normal_user_token_headers)
    assert 404 == r.status_code
   

