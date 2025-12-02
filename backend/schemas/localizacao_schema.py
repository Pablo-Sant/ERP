from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class LocalizacaoBase(BaseModel):
    id_organizacao: Optional[int] = Field(default=1)
    id_local_pai: Optional[int] = None
    codigo: str = Field(..., max_length=20)
    nome: str = Field(..., max_length=255)
    tipo_local: Optional[str] = Field(
        None,
        pattern="^(matriz|filial|armazem|fabrica|escritorio|campo|virtual)$"
    )
    endereco: Optional[str] = None
    latitude: Optional[Decimal] = Field(None, ge=-90, le=90)
    longitude: Optional[Decimal] = Field(None, ge=-180, le=180)
    pessoa_contato: Optional[str] = Field(None, max_length=255)
    telefone_contato: Optional[str] = Field(None, max_length=20)
    ativo: Optional[bool] = True

class LocalizacaoCreate(LocalizacaoBase):
    pass

class LocalizacaoUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=255)
    tipo_local: Optional[str] = Field(
        None,
        pattern="^(matriz|filial|armazem|fabrica|escritorio|campo|virtual)$"
    )
    endereco: Optional[str] = None
    pessoa_contato: Optional[str] = Field(None, max_length=255)
    telefone_contato: Optional[str] = Field(None, max_length=20)
    ativo: Optional[bool] = None

class LocalizacaoResponse(LocalizacaoBase):
    id: int
    nivel_hierarquia: int
    caminho_string: Optional[str]

    class Config:
        from_attributes = True