
from fastapi import APIRouter, Query
from pydantic import BaseModel
from app.api.deps import SessionDep

router = APIRouter(tags=["Chat"], prefix="/chat")

class Message(BaseModel):
   text:str

@router.post("")
async def chat(sess: SessionDep, message: Message):
   return message

