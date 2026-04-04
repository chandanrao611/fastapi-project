from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    first_name: str
    last_name: str = None
    mobile: int = None
    email: str
    password: str

class UserResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    first_name: str
    last_name: str = None
    mobile: int = None
    email: str
    created_at: datetime
    updated_at: datetime