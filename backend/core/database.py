# core/database.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base
from core.configs import settings
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

# Engine do banco
engine: AsyncEngine = create_async_engine(settings.DB_URL)

# Base para os modelos
Base = declarative_base()

# Session local
Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)

# Função para criar tabelas
async def create_tables():
    async with engine.begin() as conn:
        # Importar todos os modelos ANTES de criar as tabelas
        from models.usuario import UsuarioModel
        from models.projeto_model import ProjetoModel
        
        print("📊 Criando tabelas...")
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Tabelas criadas com sucesso!")
        
        # Mostrar tabelas criadas
        tables = list(Base.metadata.tables.keys())
        print(f"📋 Tabelas disponíveis: {tables}")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Alias para get_session para compatibilidade com código existente.
    """
    from core.deps import get_session
    async for session in get_session():
        yield session