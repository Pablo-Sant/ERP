# models/ativos_model.py - CORRIGIDO
from sqlalchemy import (
    Column, Integer, String, Text, Date, Numeric, Boolean,
    ForeignKey, DateTime, CheckConstraint, text, func
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel

class Ativo(DBBaseModel):
    __tablename__ = "ativos"
    __table_args__ = (
        CheckConstraint(
            "criticidade IN ('baixa','medio','alta','critico')"
        ),
        CheckConstraint(
            "status_ativo IN ('planejado','ativo','inativo','em_manutencao','baixado','descartado','perdido')"
        ),
        CheckConstraint("custo_aquisicao >= 0"),
        CheckConstraint("valor_atual >= 0"),
        CheckConstraint("valor_residual >= 0"),
        CheckConstraint("depreciacao_acumulada >= 0"),
        {"schema": "am"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    #id_organizacao = Column(Integer, nullable=False, default=1)
    #id_categoria = Column(Integer, ForeignKey("categorias_ativos.id"), nullable=False)
    #id_localizacao = Column(Integer, ForeignKey("localizacoes.id"), nullable=False)
    #id_fornecedor = Column(Integer, ForeignKey("fornecedores.id"))
    
    numero_tag = Column(String(100), nullable=False, unique=True)
    numero_serie = Column(String(100))
    modelo = Column(String(255))
    fabricante = Column(String(255))
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    status_ativo = Column(String(50), server_default=text("'ativo'"))
    criticidade = Column(String(20), server_default=text("'medio'"))
    data_aquisicao = Column(Date)
    custo_aquisicao = Column(Numeric(18, 2))
    numero_ordem_compra = Column(String(100))
    data_vencimento_garantia = Column(Date)
    vida_util_anos = Column(Integer)
    valor_residual = Column(Numeric(18, 2), server_default=text("0"))
    valor_atual = Column(Numeric(18, 2))
    depreciacao_acumulada = Column(Numeric(18, 2), server_default=text("0"))
    especificacoes = Column(JSONB)
    parametros_tecnicos = Column(JSONB)
    data_ativacao = Column(Date)
    data_desativacao = Column(Date)
    observacoes = Column(Text)
    criado_por = Column(Integer)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), server_default=func.now())

  
    #categoria = relationship("CategoriaAtivo", back_populates="ativos")
    #localizacao = relationship("Localizacao", back_populates="ativos")
    #fornecedor = relationship("Fornecedor", back_populates="ativos")
    
    # String literal com o nome da classe
    """registros_depreciacao = relationship(
        "RegistrosDepreciacao",  # ← String literal, não import
        back_populates="ativo",
        cascade="all, delete-orphan",
        lazy='select'
    )
    
    # Se outras classes também causam problemas, use string literals:
    registros_calibracao = relationship(
        "RegistrosCalibracao",  # ← String literal
        back_populates="ativo"
    )
    
    ordens_servico = relationship(
        "OrdemServico",  # ← String literal
        back_populates="ativo"
    )
    
    documentos = relationship(
        "DocumentoAtivo",  # ← String literal
        back_populates="ativo"
    )
    
    movimentacoes = relationship(
        "MovimentacaoAtivo",  # ← String literal
        back_populates="ativo"
    )"""