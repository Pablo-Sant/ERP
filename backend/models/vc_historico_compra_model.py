from sqlalchemy import (
    Column, Integer, String, Date, Numeric, ForeignKey, Time,
    DateTime, Sequence
)
from sqlalchemy.orm import relationship
from datetime import datetime
from core.configs import DBBaseModel
from models.vc_cliente_final_model import ClienteFinal
from models.vc_pedido_venda_model import PedidoVenda

class HistoricoCompra(DBBaseModel):
    __tablename__ = "historico_compra"
    __table_args__ = {"schema": "vc"}

    historicoid = Column(Integer, Sequence("vc.historico_compra_historicoid_seq"), primary_key=True)
    cliente_finalid = Column(Integer, ForeignKey("vc.cliente_final.cliente_finalid"), nullable=False)
    pedidoid = Column(Integer, ForeignKey("vc.pedidos_de_venda.pedidoid"))
    valor_compra = Column(Numeric(10, 2))
    data_compra = Column(Date, default=datetime.now)

    
    cliente_final = relationship("ClienteFinal", back_populates="historicos_compra", lazy="joined")
    pedido = relationship("PedidoVenda", back_populates="historicos", lazy="joined")