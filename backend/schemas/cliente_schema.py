from typing import Optional
from pydantic import BaseModel as SCBaseModel

# Validação dos dados recebidos pela api

class ClientesSchema(SCBaseModel):
    id:Optional[int]
    Nome:str

    class Config:
        orm_mode=True