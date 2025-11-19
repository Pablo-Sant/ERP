from sqlalchemy import (
    Column, Integer, String, Date, Numeric, ForeignKey, Time,
    DateTime, Sequence
)
from sqlalchemy.orm import relationship
from datetime import datetime
from core.configs import DBBaseModel
from models.vc_contrato_model import Contrato
from models.vc_historico_compra_model import HistoricoCompra
from models.vc_pedido_venda_model import PedidoVenda

class ClienteFinal(DBBaseModel):
    __tablename__ = "cliente_final"
    __table_args__ = {"schema": "vc"}

    cliente_finalid = Column(Integer, Sequence("vc.cliente_final_cliente_finalid_seq"), primary_key=True)
    nome = Column(String(100), nullable=False)
    cpf_cnpj = Column(String(20))
    email = Column(String(100))
    telefone = Column(String(20))
    endereco = Column(String(200))
    cidade = Column(String(100))
    data_ultima_compra = Column(Date)
    valor_compra = Column(Numeric(10, 2))

    
    contratos = relationship("Contrato", back_populates="cliente_final", lazy="joined")
    historicos_compra = relationship("HistoricoCompra", back_populates="cliente_final", lazy="joined")
    pedidos = relationship("PedidoVenda", back_populates="cliente_final", lazy="joined")