from sqlalchemy.orm import Session
from typing import List, Optional
from models.ativos_model import Ativo
from models.categoria_ativo_model import CategoriaAtivo
from models.localizacao_model import Localizacao
from models.fornecedor_model import Fornecedor
from schemas.ativo_schema import AtivoCreate, AtivoUpdate

class AtivoService:
    @staticmethod
    def criar_ativo(db: Session, ativo: AtivoCreate) -> Ativo:
        # Verificar se categoria existe
        categoria = db.query(CategoriaAtivo).filter(
            CategoriaAtivo.id == ativo.id_categoria,
            CategoriaAtivo.ativo == True
        ).first()
        if not categoria:
            raise ValueError(f"Categoria com ID {ativo.id_categoria} não encontrada ou inativa")
        
        # Verificar se localização existe
        localizacao = db.query(Localizacao).filter(
            Localizacao.id == ativo.id_localizacao,
            Localizacao.ativo == True
        ).first()
        if not localizacao:
            raise ValueError(f"Localização com ID {ativo.id_localizacao} não encontrada ou inativa")
        
        # Verificar se fornecedor existe (se fornecido)
        if ativo.id_fornecedor:
            fornecedor = db.query(Fornecedor).filter(
                Fornecedor.id == ativo.id_fornecedor,
                Fornecedor.ativo == True
            ).first()
            if not fornecedor:
                raise ValueError(f"Fornecedor com ID {ativo.id_fornecedor} não encontrado ou inativo")
        
        # Verificar se número tag já existe
        tag_existente = db.query(Ativo).filter(
            Ativo.numero_tag == ativo.numero_tag
        ).first()
        if tag_existente:
            raise ValueError(f"Número tag {ativo.numero_tag} já existe")
        
        # Criar ativo
        db_ativo = Ativo(**ativo.dict())
        db.add(db_ativo)
        db.commit()
        db.refresh(db_ativo)
        return db_ativo
    
    @staticmethod
    def obter_ativo(db: Session, ativo_id: int) -> Optional[Ativo]:
        return db.query(Ativo).filter(Ativo.id == ativo_id).first()
    
    @staticmethod
    def listar_ativos(db: Session, skip: int = 0, limit: int = 100) -> List[Ativo]:
        return db.query(Ativo).offset(skip).limit(limit).all()
    
    @staticmethod
    def atualizar_ativo(db: Session, ativo_id: int, ativo_update: AtivoUpdate) -> Optional[Ativo]:
        db_ativo = db.query(Ativo).filter(Ativo.id == ativo_id).first()
        if not db_ativo:
            return None
        
        update_data = ativo_update.dict(exclude_unset=True)
        
        # Verificar se nova localização existe
        if 'id_localizacao' in update_data:
            localizacao = db.query(Localizacao).filter(
                Localizacao.id == update_data['id_localizacao'],
                Localizacao.ativo == True
            ).first()
            if not localizacao:
                raise ValueError(f"Localização com ID {update_data['id_localizacao']} não encontrada ou inativa")
        
        for field, value in update_data.items():
            setattr(db_ativo, field, value)
        
        db.commit()
        db.refresh(db_ativo)
        return db_ativo
    
    @staticmethod
    def excluir_ativo(db: Session, ativo_id: int) -> bool:
        db_ativo = db.query(Ativo).filter(Ativo.id == ativo_id).first()
        if not db_ativo:
            return False
        
        # Verificar se há ordens de serviço ativas
        if db_ativo.ordens_servico:
            ordens_ativas = [os for os in db_ativo.ordens_servico if os.status not in ['concluida', 'cancelada']]
            if ordens_ativas:
                raise ValueError("Não é possível excluir ativo com ordens de serviço ativas")
        
        db.delete(db_ativo)
        db.commit()
        return True
    
    @staticmethod
    def buscar_ativos(db: Session, 
                     id_categoria: Optional[int] = None,
                     id_localizacao: Optional[int] = None,
                     status: Optional[str] = None,
                     criticidade: Optional[str] = None) -> List[Ativo]:
        query = db.query(Ativo)
        
        if id_categoria:
            query = query.filter(Ativo.id_categoria == id_categoria)
        if id_localizacao:
            query = query.filter(Ativo.id_localizacao == id_localizacao)
        if status:
            query = query.filter(Ativo.status_ativo == status)
        if criticidade:
            query = query.filter(Ativo.criticidade == criticidade)
        
        return query.all()