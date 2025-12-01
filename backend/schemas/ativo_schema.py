from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from uuid import UUID

class AtivoBase(BaseModel):
    id_organizacao: Optional[int]
    id_categoria: Optional[int]
    id_localizacao: Optional[int]
    id_fornecedor: Optional[int]
    numero_tag: Optional[str]
    numero_serie: Optional[str]
    nome: Optional[str]
    modelo: Optional[str]
    fabricante: Optional[str]
    status_ativo: Optional[str] = "ativo"
    criticidade: Optional[str] = "medio"
    data_aquisicao: Optional[date] = datetime.now
    numero_ordem_compra: Optional[int]
    custo_aquisicao: Optional[float]
    data_vencimento_garantia: Optional[date]
    valor_atual: Optional[float]
    valor_residual: Optional[float]
    especificacoes: Optional[dict]
    parametros_tecnicos: Optional[dict]
    vida_util_anos: Optional[int]   

class AtivoCreate(AtivoBase):
    pass

class AtivoResponse(AtivoBase):
    id: int
    uuid: UUID
    data_criacao: datetime

    class Config:
        orm_mode = True
