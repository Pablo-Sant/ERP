# models/vc_contrato_model.py
from sqlalchemy import (
    Column, Integer, String, Date, Numeric, ForeignKey, Time,
    DateTime, Sequence
)
from sqlalchemy.orm import relationship
from datetime import datetime
from core.configs import DBBaseModel

class Contrato(DBBaseModel):
    __tablename__ = "contratos"
    __table_args__ = {"schema": "vc"}

    contratoid = Column(Integer, Sequence("vc.contratos_contratoid_seq"), primary_key=True)
    cliente_finalid = Column(Integer, ForeignKey("vc.cliente_final.cliente_finalid"))
    vendedorid = Column(Integer, ForeignKey("vc.vendedor.vendedorid"))
    data_inicio = Column(DateTime, default=datetime.now)
    vencimento = Column(Date)

    
    cliente_final = relationship("ClienteFinal", lazy="select")
    vendedor = relationship("Vendedor", lazy="select")