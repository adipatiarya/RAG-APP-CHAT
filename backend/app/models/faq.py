# Shared properties
from datetime import datetime
import uuid

from sqlmodel import  Column, Field, SQLModel, Text, DateTime
from sqlmodel import SQLModel, Field
from pgvector.sqlalchemy import Vector
from app.utils import get_datetime_utc

class FaqBase(SQLModel): 
    content: str = Field(sa_column=Column(Text))

    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    deleted_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
class Faq(FaqBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    embedding: list[float] = Field(sa_column=Column(Vector(768)))

class FaqCreate(FaqBase):
    project_name: str | None = Field(default='default')

class FaqPublic(FaqCreate):
    pass