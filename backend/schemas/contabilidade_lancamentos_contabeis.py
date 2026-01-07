from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, Annotated
from pydantic import BaseModel, StringConstraints, Field

class ContabilidadeLancamentosBase(BaseModel):
    data: date
    historico: Optional[str] = None
    valor: Decimal
    debito_conta_id: int
    credito_conta_id: int
    origem_modulo: Optional[str] = None
    origem_id: Optional[int] = None


class ContabilidadeLancamentosCreate(ContabilidadeLancamentosBase):
    pass


class ContabilidadeLancamentosResponse(ContabilidadeLancamentosBase):
    id_lancamento: int

    class Config:
        from_attributes = True



class ContabilidadeLancamentosUpdate(BaseModel):
    """Schema para atualização parcial de lançamentos contábeis"""
    data: Optional[date] = None
    historico: Optional[str] = None
    valor: Optional[Decimal] = None
    debito_conta_id: Optional[int] = None
    credito_conta_id: Optional[int] = None
    origem_modulo: Optional[str] = None
    origem_id: Optional[int] = None
    
    class Config:
        from_attributes = True