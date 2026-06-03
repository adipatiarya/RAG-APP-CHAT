from typing import Annotated
import uuid

from fastapi import APIRouter, BackgroundTasks, Depends
from app.models.document import DocumentCreate, Document, DocumentUpdate
from app.api.deps import SessionDep, get_embeded_service
from app.repositories.embeded.embed import get_embedding

router = APIRouter(tags=["Documents"], prefix="/documents")


@router.post("")
async def create_doc(sess: SessionDep, doc_in: DocumentCreate):
    embed = get_embedding(doc_in.content)
    user_model = Document.model_validate(doc_in, update={"embedding":embed})

    service = get_embeded_service(sess)
    await service.embed.add(user_model)


@router.get("")
async def list_doc(sess: SessionDep):
    service = get_embeded_service(sess)
    docs = await service.embed.list_all()
    return [
        {
            "id": doc.id,
            "content": doc.content,
            "embedding_len": len(doc.embedding) if doc.embedding is not None else None,
            "embedding_sample": doc.embedding[:5].tolist() if doc.embedding is not None else None
        }
        for doc in docs
    ]
