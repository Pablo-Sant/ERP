from sqlalchemy import (
    Column, Integer, String, Numeric, Date, Boolean, Text, CheckConstraint, ForeignKey, Computed
)
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel
from models.ordens_servicos_model import OrdemServico

class PecasOrdemServico(DBBaseModel):
    __tablename__ = "pecas_ordem_servico"
    __table_args__ = (
        CheckConstraint("custo_unitario >= 0", name="pecas_ordem_servico_custo_unitario_check"),
        {"schema": "am"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_ordem_servico = Column(Integer, ForeignKey("am.ordens_servico.id"), nullable=False)
    numero_peca = Column(String(100), nullable=False)
    nome_peca = Column(String(255), nullable=False)
    quantidade = Column(Numeric(10, 2), nullable=False)
    custo_unitario = Column(Numeric(18, 2))
    custo_total = Column(Numeric(18, 2), Computed("quantidade * custo_unitario", persisted=True))

    ordem_servico = relationship("OrdemServico", back_populates="pecas")