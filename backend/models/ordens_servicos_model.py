from sqlalchemy.dialects.postgresql import UUID, JSONB
from core.configs import DBBaseModel
from sqlalchemy import (
    Column, Integer, String, Text, Date, Numeric, Boolean,
    ForeignKey, DateTime, JSON, CheckConstraint, text, func, orm
)
from typing import List
from models.am_planos_manutencao_model import PlanosManutencao
from models.ativos_model import Ativo

class OrdemServico(DBBaseModel):
    __tablename__ = "ordens_servico"
    __table_args__ = (
        CheckConstraint("custo_material_real >= 0"),
        CheckConstraint("custo_mao_obra_real >= 0"),
        CheckConstraint(
            "prioridade IN ('baixa','medio','alta','critico')"
        ),
        CheckConstraint(
            "status IN ('aberta','atribuida','em_andamento','em_espera','concluida','cancelada')"
        ),
        CheckConstraint(
            "tipo_os IN ('preventiva','corretiva','emergencia','preditiva','calibracao')"
        ),
        {"schema": "am"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    #id_organizacao = Column(Integer, ForeignKey('Organizacao.id'), nullable=False)
    #organizacao = orm.relationship('Organizacao', lazy='joined')
    id_ativo = Column(Integer, ForeignKey("am.ativos.id"), nullable=False)
    ativo = orm.relationship('Ativo', lazy='joined')
    id_plano_manutencao = Column(Integer, ForeignKey('am.planos_manutencao.id'))
    plano_manutencao = orm.relationship('PlanosManutencao', lazy='joined')
    numero_os = Column(String(100), nullable=False)
    tipo_os = Column(String(50))
    prioridade = Column(String(20), server_default=text("'medio'"))
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text)
    descricao_problema = Column(Text)
    data_agendada = Column(DateTime(timezone=True))
    data_vencimento = Column(DateTime(timezone=True))
    data_inicio_real = Column(DateTime(timezone=True))
    data_fim_real = Column(DateTime(timezone=True))
    atribuido_para = Column(Integer)
    status = Column(String(50), server_default=text("'aberta'"))
    horas_trabalho_reais = Column(Numeric(5, 2))
    custo_material_real = Column(Numeric(18, 2))
    custo_mao_obra_real = Column(Numeric(18, 2))
    custo_total = Column(Numeric(18, 2))
    trabalho_realizado = Column(Text)
    causa_raiz = Column(Text)
    recomendacoes = Column(Text)
    criado_por = Column(Integer)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), server_default=func.now())