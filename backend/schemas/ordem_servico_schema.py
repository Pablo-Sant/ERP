from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrdemServicoBase(BaseModel):
    id_organizacao: int
    id_ativo: int
    numero_os: str
    tipo_os: Optional[str]
    prioridade: Optional[str] = "medio"
    titulo: str
    descricao: Optional[str]
    descricao_problema: Optional[str]
    status: Optional[str] = "aberta"

class OrdemServicoCreate(OrdemServicoBase):
    pass

class OrdemServicoResponse(OrdemServicoBase):
    id: int
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        orm_mode = True
