import asyncio
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.configs import settings, DBBaseModel
from main import app
from fastapi.testclient import TestClient



@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()



TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:"
    f"{settings.DB_PASS}@{settings.DB_HOST}:"
    f"{settings.DB_PORT}/{settings.DB_NAME}_test"
)


engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)

AsyncSessionLocal = sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)



@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    """
    Cria todas as tabelas no início da sessão de testes
    e remove todas no final.
    """
    async with engine_test.begin() as conn:
        await conn.run_sync(DBBaseModel.metadata.create_all)

    yield

    async with engine_test.begin() as conn:
        await conn.run_sync(DBBaseModel.metadata.drop_all)



@pytest.fixture
async def db_session():
    """
    Abre uma sessão por teste e faz rollback ao final,
    garantindo isolamento entre testes.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()



@pytest.fixture
def client(db_session, monkeypatch):
    """
    Substitui a dependência get_db da API para usar o banco de testes.
    """

    async def override_get_db():
        yield db_session

    from core.deps import get_db  # ajuste para o seu projeto

    monkeypatch.setattr("api.deps.get_db", override_get_db)

    with TestClient(app) as c:
        yield c
