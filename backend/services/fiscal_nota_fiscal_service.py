from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.fiscal_notas_fiscais import FiscalNotasFiscais


class FiscalNotasFiscaisService:

    @staticmethod
    async def create(dto, db: AsyncSession) -> FiscalNotasFiscais:

        novo = FiscalNotasFiscais(
            **dto.model_dump()
        )

        db.add(novo)
        await db.commit()
        await db.refresh(novo)
        return novo

    @staticmethod
    async def get_all(db: AsyncSession):

        result = await db.execute(
            select(FiscalNotasFiscais)
            .order_by(FiscalNotasFiscais.id_nota)
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_id(id: int, db: AsyncSession) -> FiscalNotasFiscais | None:

        result = await db.execute(
            select(FiscalNotasFiscais)
            .filter(FiscalNotasFiscais.id_nota == id)
        )
        return result.scalars().first()

    @staticmethod
    async def update(id: int, dto, db: AsyncSession):

        registro = await FiscalNotasFiscaisService.get_by_id(id, db)

        if not registro:
            return None

        for campo, valor in dto.model_dump().items():
            setattr(registro, campo, valor)

        await db.commit()
        await db.refresh(registro)
        return registro

    @staticmethod
    async def delete(id: int, db: AsyncSession):

        registro = await FiscalNotasFiscaisService.get_by_id(id, db)

        if not registro:
            return None

        await db.delete(registro)
        await db.commit()
        return True
