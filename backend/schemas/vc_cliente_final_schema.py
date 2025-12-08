# schemas/cliente_final_schema.py
from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from typing import Optional, Annotated
from decimal import Decimal
from pydantic.functional_validators import AfterValidator

def validar_cpf_cnpj(v: Optional[str]) -> Optional[str]:
    
    if v is None or v == "":
        return v
        
    
    numeros = ''.join(filter(str.isdigit, v))
    
   
    if len(numeros) not in (11, 14):
        raise ValueError('CPF deve ter 11 dígitos ou CNPJ 14 dígitos')
        
    return v


CPFCNPJType = Annotated[Optional[str], AfterValidator(validar_cpf_cnpj)]

class ClienteFinalBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100, description="Nome do cliente")
    cpf_cnpj: CPFCNPJType = Field(None, min_length=11, max_length=20, description="CPF ou CNPJ")
    email: Optional[str] = Field(None, max_length=100, description="E-mail do cliente")
    telefone: Optional[str] = Field(None, max_length=20, description="Telefone do cliente")
    endereco: Optional[str] = Field(None, max_length=200, description="Endereço completo")
    cidade: Optional[str] = Field(None, max_length=100, description="Cidade")
    data_ultima_compra: Optional[date] = Field(None, description="Data da última compra")
    valor_compra: Optional[Decimal] = Field(None, ge=0, description="Valor da última compra")

class ClienteFinalCreate(ClienteFinalBase):
    pass

class ClienteFinalUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    cpf_cnpj: CPFCNPJType = Field(None, min_length=11, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    telefone: Optional[str] = Field(None, max_length=20)
    endereco: Optional[str] = Field(None, max_length=200)
    cidade: Optional[str] = Field(None, max_length=100)
    data_ultima_compra: Optional[date] = Field(None)
    valor_compra: Optional[Decimal] = Field(None, ge=0)

class ClienteFinalResponse(ClienteFinalBase):
    cliente_finalid: int = Field(..., description="ID do cliente")
    
    class Config:
        from_attributes = True