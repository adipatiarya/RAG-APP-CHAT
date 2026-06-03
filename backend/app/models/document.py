import enum
import uuid
import numpy as np
from pydantic import BaseModel, field_serializer
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Enum,Text
from pgvector.sqlalchemy import Vector
from typing import Optional


class DocumentBase(SQLModel):
    content: str = Field(sa_column=Column(Text, unique=True)) 
    
class Document(DocumentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    @field_serializer("embedding")
    def serialize_embedding(self, v):
        if isinstance(v, np.ndarray):
            return v.tolist()
        return v
    embedding: Optional[list[float]] = Field(
        default=None,
        sa_column=Column(Vector(384), nullable=True)
    )

# API schemas (BaseModel)
class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(DocumentBase):
    pass

class DocumentPublic(DocumentBase):
    id: uuid.UUID

