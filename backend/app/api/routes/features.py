
from typing import Dict

from fastapi import APIRouter
from pydantic import BaseModel
from app.utils import all_perms

router = APIRouter(tags=["Features"], prefix="/permissions")

class Resp(BaseModel):
    permissions:Dict[str, Dict[str,bool]] = all_perms()

@router.get("", response_model=Resp)
async def permissions() -> None:
    return Resp (
        permissions=all_perms()
    )