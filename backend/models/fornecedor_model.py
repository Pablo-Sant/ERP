from sqlalchemy import (
    Column, Integer, String, Text, Boolean,
    CheckConstraint, text
)
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel

class Fornecedor(DBBaseModel):
    __tablename__ = "fornecedores"
    __table_args__ = (
        CheckConstraint(
            "tipo_fornecedor IN ('fabricante','fornecedor','prestador_servico','distribuidor')"
        ),
        {"schema": "am"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_organizacao = Column(Integer, nullable=False, default=1)
    codigo = Column(String(20), nullable=False, unique=True)
    nome = Column(String(255), nullable=False)
    tipo_fornecedor = Column(String(50))
    pessoa_contato = Column(String(255))
    telefone = Column(String(20))
    email = Column(String(255))
    endereco = Column(Text)
    cnpj = Column(String(20))
    condicoes_pagamento = Column(String(100))
    ativo = Column(Boolean, server_default=text("true"))

    # Relacionamentos
    ativos = relationship("Ativo", back_populates="fornecedor")