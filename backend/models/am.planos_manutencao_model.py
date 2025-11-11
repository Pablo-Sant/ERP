from sqlalchemy import (
    Column, Integer, String, Numeric, Date, Boolean, Text, CheckConstraint, ForeignKey, Computed
)
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel

class PlanosManutencao(DBBaseModel):
    __tablename__ = "planos_manutencao"
    __table_args__ = (
        CheckConstraint("custo_estimado >= 0", name="planos_manutencao_custo_estimado_check"),
        CheckConstraint(
            "tipo_frequencia IN ('diaria','semanal','mensal','trimestral','anual','base_medidor')",
            name="planos_manutencao_tipo_frequencia_check"
        ),
        CheckConstraint(
            "tipo_manutencao IN ('preventiva','corretiva','preditiva','condicional')",
            name="planos_manutencao_tipo_manutencao_check"
        ),
        {"schema": "am"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_organizacao = Column(Integer, ForeignKey("organizacao.id"), nullable=False)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    tipo_manutencao = Column(String(50))
    tipo_frequencia = Column(String(20))
    valor_frequencia = Column(Integer)
    duracao_estimada_minutos = Column(Integer)
    custo_estimado = Column(Numeric(18, 2))
    procedimentos = Column(Text)
    ativo = Column(Boolean, default=True)