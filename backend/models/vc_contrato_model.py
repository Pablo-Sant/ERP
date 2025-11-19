from sqlalchemy import (
    Column, Integer, String, Date, Numeric, ForeignKey, Time,
    DateTime, Sequence
)
from sqlalchemy.orm import relationship
from datetime import datetime
from core.configs import DBBaseModel
from models.vc_cliente_final_model import ClienteFinal
from models.vc_vendedor_model import Vendedor


class Contrato(DBBaseModel):
    __tablename__ = "contratos"
    __table_args__ = {"schema": "vc"}

    contratoid = Column(Integer, Sequence("vc.contratos_contratoid_seq"), primary_key=True)
    cliente_finalid = Column(Integer, ForeignKey("vc.cliente_final.cliente_finalid"))
    vendedorid = Column(Integer, ForeignKey("vc.vendedor.vendedorid"))
    data_inicio = Column(DateTime, default=datetime.now)
    vencimento = Column(Date)

    
    cliente_final = relationship("ClienteFinal", back_populates="contratos", lazy="joined")
    vendedor = relationship("Vendedor", back_populates="contratos", lazy="joined")