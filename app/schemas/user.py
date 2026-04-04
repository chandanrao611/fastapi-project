from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    mobile: Optional[int] = None

class UserCreate(UserBase):
    email: str
    password: str


class UserUpdate(UserBase):
    email: Optional[str] = None
    password: Optional[str] = None


class UserResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    first_name: str
    last_name: Optional[str] = None
    mobile: Optional[int] = None
    email: str
    created_at: datetime
    updated_at: datetime