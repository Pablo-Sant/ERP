from sqlalchemy import (
    Column, Integer, String, Date, Numeric, ForeignKey, Time,
    DateTime, Sequence
)
from sqlalchemy.orm import relationship
from datetime import datetime
from core.configs import DBBaseModel
from models.vc_contrato_model import Contrato
from models.vc_pedido_venda_model import PedidoVenda

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
    #contrato_id = Column(Integer, ForeignKey("contratos.id")) Errado, pois é uma relação de 1 -> N
    #pedido_id = Column(Integer, ForeignKey("pedidos_de_venda.id"))
    
    # Em relações 1 -> N a chave estrangeira sempre vai na tabela N
    # Mas o relacionamento vai nas duas
    
    contratos = relationship("Contrato", back_populates="vendedor", lazy="joined")
    pedidos = relationship("PedidoVenda", back_populates="vendedor", lazy="joined")