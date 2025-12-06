from datetime import date
from decimal import Decimal
from typing import Annotated, Optional, List
from pydantic import BaseModel, StringConstraints, Field

class PecasOrdemServicoBase(BaseModel):
    id_ordem_servico: int
    numero_peca: Annotated[str, StringConstraints(max_length=100)]
    nome_peca: Annotated[str, StringConstraints(max_length=255)]
    quantidade: Decimal
    custo_unitario: Optional[Decimal] = None
    custo_total: Optional[Decimal] = None


class PecasOrdemServicoCreate(PecasOrdemServicoBase):
    pass


class PecasOrdemServicoResponse(PecasOrdemServicoBase):
    id: int

    class Config:
        from_attributes = True


# ADICIONE ESTA CLASSE
class PecasOrdemServicoUpdate(BaseModel):
    """Schema para atualização parcial de peças de ordem de serviço"""
    id_ordem_servico: Optional[int] = None
    numero_peca: Optional[Annotated[str, StringConstraints(max_length=100)]] = None
    nome_peca: Optional[Annotated[str, StringConstraints(max_length=255)]] = None
    quantidade: Optional[Decimal] = None
    custo_unitario: Optional[Decimal] = None
    custo_total: Optional[Decimal] = None
    
    class Config:
        from_attributes = True