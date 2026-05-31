from typing import TYPE_CHECKING, Optional
import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from sqlalchemy import DateTime

from sqlmodel import  Field, Relationship, SQLModel

from app.utils import get_datetime_utc
from app.models.user_role import UserRole
from app.models.role_permision import RolePermission

if TYPE_CHECKING:
    from .user import User
    from .permission import Permission

class Role(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=255)
    description: str | None = Field(default=None, max_length=255)
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
     # relasi ke user melalui tabel penghubung
    users: list["User"] = Relationship(
        back_populates="roles", link_model=UserRole
    )
    # relasi ke permissions melalui tabel penghubung
    permissions: list["Permission"] = Relationship(
        back_populates="roles", link_model=RolePermission
    )
    
# API schemas (BaseModel)
class RoleCreate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=128)
    description: Optional[str] = None
    permission_strs: Optional[list[str]] = Field(default_factory=list)

class RoleUpdate(RoleCreate):
    updated_at: Optional[datetime]  = get_datetime_utc()

class RoleDelete(RoleUpdate):
    deleted_at: Optional[datetime]  = get_datetime_utc()

class  RolePublic(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime
    updated_at: datetime | None = None
    users: list[str] = []
    permissions: list[str] = []
    total_user: int = 0
    total_permission: int = 0

    