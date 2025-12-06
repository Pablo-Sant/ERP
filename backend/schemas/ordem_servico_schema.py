from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrdemServicoBase(BaseModel):
    id_organizacao: int
    id_ativo: int
    numero_os: str
    tipo_os: Optional[str] = None
    prioridade: Optional[str] = "medio"
    titulo: str
    descricao: Optional[str] = None
    descricao_problema: Optional[str] = None
    status: Optional[str] = "aberta"


class OrdemServicoCreate(OrdemServicoBase):
    pass


class OrdemServicoResponse(OrdemServicoBase):
    id: int
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        from_attributes = True  # Corrigido: de orm_mode para from_attributes


# ADICIONE ESTA CLASSE
class OrdemServicoUpdate(BaseModel):
    """Schema para atualização parcial de ordem de serviço"""
    id_organizacao: Optional[int] = None
    id_ativo: Optional[int] = None
    numero_os: Optional[str] = None
    tipo_os: Optional[str] = None
    prioridade: Optional[str] = None
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    descricao_problema: Optional[str] = None
    status: Optional[str] = None
    data_atualizacao: Optional[datetime] = None
    
    class Config:
        from_attributes = True