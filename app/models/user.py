from pydantic import BaseModel, EmailStr, Field
from typing   import Optional
from datetime import datetime

class UserModel(BaseModel):
    id:         Optional[str]      = Field(default=None, alias="_id")
    name:       str
    email:      EmailStr
    password:   str
    role:       str                = "student"   # "student" or "admin"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        populate_by_name        = True
        arbitrary_types_allowed = True