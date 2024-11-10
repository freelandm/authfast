from typing import Optional

from pydantic import BaseModel, EmailStr
from app.models.base import BaseSQLModel
from sqlmodel import Field
from datetime import datetime
from uuid import uuid4, UUID

class UserBase(BaseSQLModel):
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    full_name: str
    is_active: bool = Field(default=True)

class User(UserBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    verified_email: bool = Field(default=False)

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: Optional[UUID]
    created_at: datetime

class UserRegistrationParameters(BaseModel):
    username: str
    password: str
    full_name: str = None
    email: EmailStr

class EmailVerificationParameters(BaseModel):
    username: str