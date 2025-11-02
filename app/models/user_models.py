from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime



class UserModel(BaseModel):
    username: str
    number: str
    image: str
    role: str
    status: str
    # namaUser: str
    email: EmailStr
    password: str
    created_at: datetime = None
