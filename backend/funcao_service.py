from sqlalchemy.orm import Session
from typing import List, Optional
from models.rh.funcoes_model import Funcao
from schemas.rh.funcao_schema import FuncaoCreate, FuncaoUpdate

class FuncaoService:
    @staticmethod
    def criar_funcao(db: Session, funcao: FuncaoCreate) -> Funcao:
        # Verificar se nome já existe
        nome_existente = db.query(Funcao).filter(
            Funcao.nome.ilike(funcao.nome)
        ).first()
        if nome_existente:
            raise ValueError(f"Função com nome '{funcao.nome}' já existe")
        
        db_funcao = Funcao(**funcao.dict())
        db.add(db_funcao)
        db.commit()
        db.refresh(db_funcao)
        return db_funcao
    
    @staticmethod
    def obter_funcao(db: Session, funcao_id: int) -> Optional[Funcao]:
        return db.query(Funcao).filter(Funcao.id == funcao_id).first()
    
    @staticmethod
    def listar_funcoes(db: Session, skip: int = 0, limit: int = 100) -> List[Funcao]:
        return db.query(Funcao).order_by(Funcao.nome).offset(skip).limit(limit).all()
    
    @staticmethod
    def atualizar_funcao(db: Session, funcao_id: int, funcao_update: FuncaoUpdate) -> Optional[Funcao]:
        db_funcao = db.query(Funcao).filter(Funcao.id == funcao_id).first()
        if not db_funcao:
            return None
        
        update_data = funcao_update.dict(exclude_unset=True)
        
        # Verificar se novo nome já existe (excluindo a própria função)
        if 'nome' in update_data:
            nome_existente = db.query(Funcao).filter(
                Funcao.nome.ilike(update_data['nome']),
                Funcao.id != funcao_id
            ).first()
            if nome_existente:
                raise ValueError(f"Função com nome '{update_data['nome']}' já existe")
        
        for field, value in update_data.items():
            setattr(db_funcao, field, value)
        
        db.commit()
        db.refresh(db_funcao)
        return db_funcao
    
    @staticmethod
    def excluir_funcao(db: Session, funcao_id: int) -> bool:
        db_funcao = db.query(Funcao).filter(Funcao.id == funcao_id).first()
        if not db_funcao:
            return False
        
        # Verificar se há colaboradores usando esta função
        if db_funcao.colaboradores:
            raise ValueError("Não é possível excluir função que está sendo usada por colaboradores")
        
        db.delete(db_funcao)
        db.commit()
        return True
    
    @staticmethod
    def buscar_por_nome(db: Session, nome: str) -> List[Funcao]:
        return db.query(Funcao).filter(Funcao.nome.ilike(f"%{nome}%")).all()