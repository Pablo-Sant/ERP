# scripts/create_test_user.py - CORRIGIDO
import sys
import os

# Adicionar o diretório raiz ao path para importações
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from security import gerar_hash_senha
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.usuario import UsuarioModel

# Configuração do banco CORRIGIDA - especificar codificação
DATABASE_URL = "postgresql://postgres:14114@localhost:5432/ERP?client_encoding=utf8"

def create_test_user():
    try:
        # Criar engine com configurações de codificação
        engine = create_engine(
            DATABASE_URL,
            echo=True,  # Para debug
            pool_pre_ping=True
        )
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        
        # Verificar se usuário já existe
        existing_user = session.query(UsuarioModel).filter(
            UsuarioModel.email == "admin@bluerp.com"
        ).first()
        
        if not existing_user:
            user = UsuarioModel(
                email="admin@bluerp.com",
                nome="Administrador Sistema",
                senha_hash=gerar_hash_senha("admin123"),
                tipo_usuario="administrador",
                ativo=True
            )
            session.add(user)
            session.commit()
            print("✅ Usuário admin criado com sucesso!")
            print("📧 Email: admin@bluerp.com")
            print("🔑 Senha: admin123")
            print("👤 Tipo: administrador")
        else:
            print("ℹ️  Usuário admin já existe!")
            # Atualizar senha
            existing_user.senha_hash = gerar_hash_senha("admin123")
            session.commit()
            print("🔑 Senha atualizada para: admin123")
            
    except Exception as e:
        print(f"❌ Erro ao criar usuário: {e}")
        import traceback
        traceback.print_exc()
        if 'session' in locals():
            session.rollback()
    finally:
        if 'session' in locals():
            session.close()
        if 'engine' in locals():
            engine.dispose()

if __name__ == "__main__":
    create_test_user()