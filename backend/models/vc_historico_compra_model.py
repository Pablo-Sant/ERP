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

    historicoid = Column(Integer, Sequence("vc.historico_compra_historicoid_seq"), primary_key=True)  # CORRIGIDO: historico_id -> historicoid
    cliente_finalid = Column(Integer, ForeignKey("vc.cliente_final.cliente_finalid"), nullable=False)  # CORRIGIDO: cliente_final_id -> cliente_finalid
    pedidoid = Column(Integer, ForeignKey("vc.pedidos_de_venda.pedidoid"))  # CORRIGIDO: pedido_id -> pedidoid
    valor_compra = Column(Numeric(10, 2))
    data_compra = Column(Date, default=datetime.now)

    cliente_final = relationship("ClienteFinal", back_populates="historicos_compra", lazy="joined")
    pedido = relationship("PedidoVenda", back_populates="historicos", lazy="joined")