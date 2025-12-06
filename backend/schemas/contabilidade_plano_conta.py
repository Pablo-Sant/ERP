from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, Annotated
from pydantic import BaseModel, StringConstraints, Field

class ContabilidadePlanoContasBase(BaseModel):
    codigo: Annotated[str, StringConstraints(max_length=20)]
    nome: Annotated[str, StringConstraints(max_length=100)]
    tipo: Annotated[str, StringConstraints(max_length=20)]
    nivel: int


class ContabilidadePlanoContasCreate(ContabilidadePlanoContasBase):
    pass


class ContabilidadePlanoContasResponse(ContabilidadePlanoContasBase):
    id_conta: int

    class Config:
        from_attributes = True


# ADICIONE ESTA CLASSE
class ContabilidadePlanoContasUpdate(BaseModel):
    """Schema para atualização parcial de plano de contas"""
    codigo: Optional[Annotated[str, StringConstraints(max_length=20)]] = None
    nome: Optional[Annotated[str, StringConstraints(max_length=100)]] = None
    tipo: Optional[Annotated[str, StringConstraints(max_length=20)]] = None
    nivel: Optional[int] = None
    
    class Config:
        from_attributes = True