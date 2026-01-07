from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentoAtivoBase(BaseModel):
    id_ativo: int
    tipo_documento: Optional[str]
    nome_documento: str
    nome_arquivo: Optional[str]
    caminho_arquivo: Optional[str]
    tamanho_arquivo: Optional[int]


class DocumentoAtivoCreate(DocumentoAtivoBase):
    pass


class DocumentoAtivoResponse(DocumentoAtivoBase):
    id: int
    data_envio: datetime

    class Config:
        from_attributes = True  # Corrigido: de orm_mode para from_attributes


class DocumentoAtivoUpdate(BaseModel):
    """Schema para atualização parcial de documento de ativo"""
    id_ativo: Optional[int] = None
    tipo_documento: Optional[str] = None
    nome_documento: Optional[str] = None
    nome_arquivo: Optional[str] = None
    caminho_arquivo: Optional[str] = None
    tamanho_arquivo: Optional[int] = None
    
    class Config:
        from_attributes = True