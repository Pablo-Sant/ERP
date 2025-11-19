from sqlalchemy import (
    Column, Integer, String, Date, Numeric, ForeignKey, Time,
    DateTime, Sequence
)
from sqlalchemy.orm import relationship
from datetime import datetime
from core.configs import DBBaseModel
from models.vc_cliente_final_model import ClienteFinal
from models.vc_vendedor_model import Vendedor
from models.vc_historico_compra_model import HistoricoCompra

class PedidoVenda(DBBaseModel):
    __tablename__ = "pedidos_de_venda"
    __table_args__ = {"schema": "vc"}

    pedidoid = Column(Integer, Sequence("vc.pedidos_de_venda_pedidoid_seq"), primary_key=True)
    cliente_finalid = Column(Integer, ForeignKey("vc.cliente_final.cliente_finalid"), nullable=False)
    vendedorid = Column(Integer, ForeignKey("vc.vendedor.vendedorid"), nullable=False)
    data_prevista_entrega = Column(Date)
    hora = Column(Time)
    status = Column(String(30))

    
    cliente_final = relationship("ClienteFinal", back_populates="pedidos", lazy="joined")
    vendedor = relationship("Vendedor", back_populates="pedidos", lazy="joined")
    historicos = relationship("HistoricoCompra", back_populates="pedido", lazy="joined")