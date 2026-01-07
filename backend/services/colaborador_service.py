from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from models.rh.colaboradores_model import Colaborador
from models.rh.funcoes_model import Funcao
from schemas.rh.colaborador_schema import ColaboradorCreate, ColaboradorUpdate

class ColaboradorService:
    @staticmethod
    def criar_colaborador(db: Session, colaborador: ColaboradorCreate) -> Colaborador:
        # Verificar se CPF já existe
        cpf_existente = db.query(Colaborador).filter(
            Colaborador.cpf == colaborador.cpf
        ).first()
        if cpf_existente:
            raise ValueError(f"CPF {colaborador.cpf} já cadastrado")
        
        # Verificar se função existe
        if colaborador.funcao_id:
            funcao = db.query(Funcao).filter(
                Funcao.id == colaborador.funcao_id
            ).first()
            if not funcao:
                raise ValueError(f"Função com ID {colaborador.funcao_id} não encontrada")
        
        # Verificar datas
        if colaborador.data_de_recrutamento > colaborador.data_contratacao:
            raise ValueError("Data de recrutamento não pode ser posterior à data de contratação")
        
        # Criar colaborador
        db_colaborador = Colaborador(**colaborador.dict())
        db.add(db_colaborador)
        db.commit()
        db.refresh(db_colaborador)
        return db_colaborador
    
    @staticmethod
    def obter_colaborador(db: Session, colaborador_id: int) -> Optional[Colaborador]:
        return db.query(Colaborador).filter(Colaborador.id == colaborador_id).first()
    
    @staticmethod
    def listar_colaboradores(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        ativo: Optional[bool] = None,
        funcao_id: Optional[int] = None
    ) -> List[Colaborador]:
        query = db.query(Colaborador)
        
        if ativo is not None:
        
            query = query.filter(Colaborador.ativo == (1 if ativo else 0))
        
        if funcao_id:
            query = query.filter(Colaborador.funcao_id == funcao_id)
        
        return query.order_by(Colaborador.nome).offset(skip).limit(limit).all()
    
    @staticmethod
    def atualizar_colaborador(
        db: Session, 
        colaborador_id: int, 
        colaborador_update: ColaboradorUpdate
    ) -> Optional[Colaborador]:
        db_colaborador = db.query(Colaborador).filter(Colaborador.id == colaborador_id).first()
        if not db_colaborador:
            return None
        
        update_data = colaborador_update.dict(exclude_unset=True)
        
        # Verificar se nova função existe
        if 'funcao_id' in update_data and update_data['funcao_id']:
            funcao = db.query(Funcao).filter(
                Funcao.id == update_data['funcao_id']
            ).first()
            if not funcao:
                raise ValueError(f"Função com ID {update_data['funcao_id']} não encontrada")
        
        # Não permitir atualizar CPF
        if 'cpf' in update_data:
            raise ValueError("CPF não pode ser alterado")
        
        for field, value in update_data.items():
            setattr(db_colaborador, field, value)
        
        db.commit()
        db.refresh(db_colaborador)
        return db_colaborador
    
    @staticmethod
    def excluir_colaborador(db: Session, colaborador_id: int) -> bool:
        db_colaborador = db.query(Colaborador).filter(Colaborador.id == colaborador_id).first()
        if not db_colaborador:
            return False
        
        # Verificar se há registros relacionados antes de excluir
        if db_colaborador.beneficios:
            raise ValueError("Não é possível excluir colaborador com benefícios ativos")
        
        if db_colaborador.folhas_pagamento:
            raise ValueError("Não é possível excluir colaborador com registros de folha de pagamento")
        
        db.delete(db_colaborador)
        db.commit()
        return True
    
    @staticmethod
    def buscar_por_cpf(db: Session, cpf: str) -> Optional[Colaborador]:
        return db.query(Colaborador).filter(Colaborador.cpf == cpf).first()
    
    @staticmethod
    def calcular_idade(colaborador: Colaborador) -> Optional[int]:
        if not colaborador.data_de_nascimento:
            return None
        
        hoje = date.today()
        nascimento = colaborador.data_de_nascimento
        idade = hoje.year - nascimento.year
        
        if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
            idade -= 1
        
        return idade
    
    @staticmethod
    def calcular_tempo_empresa(colaborador: Colaborador) -> int:
        hoje = date.today()
        contratacao = colaborador.data_contratacao
        tempo = hoje.year - contratacao.year
        
        if (hoje.month, hoje.day) < (contratacao.month, contratacao.day):
            tempo -= 1
        
        return tempo