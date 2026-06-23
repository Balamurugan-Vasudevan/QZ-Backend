from pydantic import BaseModel, EmailStr
from typing   import Optional

class RegisterSchema(BaseModel):
    name:     str
    email:    EmailStr
    password: str
    role:     str = "student"    # "student" or "admin"

class LoginSchema(BaseModel):
    email:    EmailStr
    password: str

class UserResponse(BaseModel):
    id:    str
    name:  str
    email: str
    role:  str
    token: str

class UserOut(BaseModel):
    id:    str
    name:  str
    email: str
    role:  str