from sqlalchemy import (
    Column, Integer, String, Date, Numeric, ForeignKey, Time,
    DateTime, Sequence
)
from sqlalchemy.orm import relationship
from datetime import datetime
from core.configs import DBBaseModel

class Prospecto(DBBaseModel):
    __tablename__ = "prospecto"
    __table_args__ = {"schema": "vc"}

    prospectoid = Column(Integer, Sequence("vc.prospecto_prospectoid_seq"), primary_key=True)
    produto_interesse = Column(String(100))
    fase_funil = Column(String(50))
    status = Column(String(20))