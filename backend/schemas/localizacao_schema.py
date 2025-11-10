from pydantic import BaseModel
from typing import Optional

class LocalizacaoBase(BaseModel):
    id_organizacao: int
    codigo: str
    nome: str
    tipo_local: Optional[str]
    endereco: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    pessoa_contato: Optional[str]
    telefone_contato: Optional[str]
    ativo: Optional[bool] = True

class LocalizacaoCreate(LocalizacaoBase):
    pass

class LocalizacaoResponse(LocalizacaoBase):
    id: int

    class Config:
        orm_mode = True
