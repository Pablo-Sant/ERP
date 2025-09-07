from typing import Optional
from pydantic import BaseModel as SCBaseModel, EmailStr

# Validação dos dados recebidos pela api

class ClientesSchema(SCBaseModel):
    id:Optional[int]
    Nome:str
    Email:EmailStr


    class Config:
        orm_mode=True