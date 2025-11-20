from sqlalchemy import (
    Column, Integer, String, Date, Numeric, ForeignKey, Time,
    DateTime, Sequence
)
from sqlalchemy.orm import relationship
from datetime import datetime
from core.configs import DBBaseModel


class HistoricoCompra(DBBaseModel):
    __tablename__ = "historico_compra"
    __table_args__ = {"schema": "vc"}

    historico_id = Column(Integer, Sequence("vc.historico_compra_historicoid_seq"), primary_key=True)
    cliente_final_id = Column(Integer, ForeignKey("vc.cliente_final.cliente_finalid"), nullable=False)
    pedido_id = Column(Integer, ForeignKey("vc.pedidos_de_venda.pedidoid"))
    valor_compra = Column(Numeric(10, 2))
    data_compra = Column(Date, default=datetime.now)

    
    cliente_final = relationship("ClienteFinal", back_populates="historicos_compra", lazy="joined")
    pedido = relationship("PedidoVenda", back_populates="historicos", lazy="joined")