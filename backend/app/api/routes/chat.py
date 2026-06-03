
from fastapi import APIRouter, Query
from pydantic import BaseModel
from app.api.deps import SessionDep, get_embeded_service

router = APIRouter(tags=["Chat"], prefix="/chat")

class Message(BaseModel):
   text:str

@router.post("")
async def chat(sess: SessionDep, message: Message):
   chatr = get_embeded_service(sess)
   result = await chatr.chat(message.text)
   return result

