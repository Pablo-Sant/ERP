# schemas/auth_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class LoginSchema(BaseModel):
    username: str  # Pode ser email ou nome
    password: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserResponseSchema(BaseModel):
    id: int
    email: str
    nome: str
    tipo_usuario: str

    class Config:
        from_attributes = True

class UserCreateSchema(BaseModel):
    email: EmailStr
    nome: str
    password: str
    tipo_usuario: str

class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = None
    nome: Optional[str] = None
    tipo_usuario: Optional[str] = None
    ativo: Optional[bool] = None