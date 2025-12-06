from pydantic import BaseModel, Field, EmailStr, validator
from datetime import date, datetime
from typing import Optional

class ColaboradorBase(BaseModel):
    nome: str = Field(..., max_length=100)
    cpf: str = Field(..., min_length=11, max_length=11)
    email: Optional[EmailStr] = Field(None, max_length=100)
    
    funcao_id: Optional[int] = None
    data_contratacao: date
    carga_horaria: int = Field(..., ge=1, le=168)
    
    data_de_nascimento: Optional[date] = None
    data_de_recrutamento: date
    
    salario: float = Field(..., ge=0)
    
    # Campos virtuais para compatibilidade
    ativo: Optional[int] = Field(default=1, ge=0, le=1)
    
    @validator('cpf')
    def validar_cpf(cls, v):
        if len(v) != 11 or not v.isdigit():
            raise ValueError('CPF deve conter 11 dígitos numéricos')
        return v
    
    @validator('data_de_recrutamento')
    def validar_datas(cls, v, values):
        if 'data_contratacao' in values and v > values['data_contratacao']:
            raise ValueError('Data de recrutamento não pode ser posterior à data de contratação')
        return v

class ColaboradorBeneficioCreate(ColaboradorBase):
    pass

class ColaboradorUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = Field(None, max_length=100)
    funcao_id: Optional[int] = None
    carga_horaria: Optional[int] = Field(None, ge=1, le=168)
    data_de_nascimento: Optional[date] = None
    salario: Optional[float] = Field(None, ge=0)
    ativo: Optional[int] = Field(None, ge=0, le=1)

class ColaboradorBeneficioResponse(ColaboradorBase):
    id: int
    # Campos virtuais que não existem no banco mas são retornados
    data_criacao: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None
    
    class Config:
        from_attributes = True