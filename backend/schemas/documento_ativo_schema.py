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
        orm_mode = True
