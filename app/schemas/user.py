from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: str
    is_active: bool

    model_config = {"from_attributes": True}
