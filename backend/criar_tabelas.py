from core.configs import DBBaseModel
from core.database import engine
from sqlalchemy import text

async def drop_all_cascade(conn, metadata):
    for table in metadata.sorted_tables:
        await conn.execute(text(f"DROP TABLE IF EXISTS {table.schema}.{table.name} CASCADE"))


async def create_tables() -> None:
    import models.__all_models
    # criando as tabelas no banco 

    async with engine.begin() as conn:
        await drop_all_cascade(conn, DBBaseModel.metadata)
        #await conn.run_sync(DBBaseModel.metadata.drop_all)
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS am"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS bi"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS grc"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS mm"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS vc"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS fi"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS pp"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS ps"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS qm"))
        await conn.run_sync(DBBaseModel.metadata.create_all)
    print("Tabelas criadas com sucesso")

if __name__ == "__main__":
    import asyncio

    asyncio.run(create_tables())


