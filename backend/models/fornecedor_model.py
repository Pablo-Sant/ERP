from sqlalchemy import (
    Column, Integer, String, Text, Date, Numeric, Boolean,
    ForeignKey, DateTime, JSON, CheckConstraint, text, func, orm
)
from core.configs import DBBaseModel
from typing import List

class Fornecedor(DBBaseModel):
    __tablename__ = "fornecedores"
    __table_args__ = (
        CheckConstraint("email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'"),
        CheckConstraint(
            "tipo_fornecedor IN ('fabricante','fornecedor','prestador_servico','distribuidor')"
        ),
        {"schema": "am"}
    )

    id = Column(Integer, primary_key=True)
    #id_organizacao = Column(Integer, ForeignKey('am.organizacao.id'), nullable=False)
    # = orm.relationship('Organizacao', lazy='joined')
    codigo = Column(String(20), nullable=False)
    nome = Column(String(255), nullable=False)
    tipo_fornecedor = Column(String(50))
    pessoa_contato = Column(String(255))
    telefone = Column(String(20))
    email = Column(String(255))
    endereco = Column(Text)
    cnpj = Column(String(20))
    condicoes_pagamento = Column(String(100))
    ativo = Column(Boolean, server_default=text("true"))
    
    #produtos:List[Produto] = orm.relationship("Produto", back_populates='fornecedor' lazy='dynamic')