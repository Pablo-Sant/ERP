from pydantic import BaseModel
from datetime import date
from typing import Optional

class ColaboradorBase(BaseModel):
    nome: str
    cpf: str
    email: Optional[str] = None
    funcao_id: Optional[int] = None
    data_contratacao: date
    carga_horaria: int
    data_de_nascimento: Optional[date] = None
    data_de_recrutamento: date
    salario: float


class ColaboradorCreate(ColaboradorBase):
    pass


class ColaboradorResponse(ColaboradorBase):  # Mude de Read para Response
    id: int

    class Config:
        from_attributes = True  # Corrigido: de orm_mode para from_attributes


# ADICIONE ESTA CLASSE
class ColaboradorUpdate(BaseModel):
    """Schema para atualização parcial de colaborador"""
    nome: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[str] = None
    funcao_id: Optional[int] = None
    data_contratacao: Optional[date] = None
    carga_horaria: Optional[int] = None
    data_de_nascimento: Optional[date] = None
    data_de_recrutamento: Optional[date] = None
    salario: Optional[float] = None
    
    class Config:
        from_attributes = True