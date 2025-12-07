# models/vc_vendedor_model.py
from sqlalchemy import (
    Column, Integer, String, Date, Numeric, ForeignKey, Time,
    DateTime, Sequence
)
from sqlalchemy.orm import relationship
from datetime import datetime
from core.configs import DBBaseModel

class Vendedor(DBBaseModel):
    __tablename__ = "vendedor"
    __table_args__ = {"schema": "vc"}

    vendedorid = Column(Integer, Sequence("vc.vendedor_vendedorid_seq"), primary_key=True)
    nome = Column(String(100), nullable=False)
    cpf_cnpj = Column(String(20), nullable=False)
    inscricao_estadual = Column(String(30))
    email = Column(String(100))
    telefone = Column(String(20))
    endereco = Column(String(200))
    cidade = Column(String(100))
    estado = Column(String(50))
    site = Column(String(100))
    status = Column(String(20))
    data_cadastro = Column(Date, default=datetime.now)
    
    
    contratos = relationship("Contrato", back_populates="vendedor")
    pedidos = relationship("PedidoVenda", back_populates="vendedor", lazy="joined")