from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.fiscal_impostos import FiscalImpostos


class FiscalImpostosService:

    @staticmethod
    async def create(dto, db: AsyncSession) -> FiscalImpostos:

        novo = FiscalImpostos(
            **dto.model_dump()
        )

        db.add(novo)
        await db.commit()
        await db.refresh(novo)
        return novo

    @staticmethod
    async def get_all(db: AsyncSession):

        result = await db.execute(
            select(FiscalImpostos)
            .order_by(FiscalImpostos.id_imposto)
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_id(id_imposto: int, db: AsyncSession) -> FiscalImpostos | None:

        result = await db.execute(
            select(FiscalImpostos)
            .filter(FiscalImpostos.id_imposto == id_imposto)
        )
        return result.scalars().first()

    @staticmethod
    async def update(id_imposto: int, dto, db: AsyncSession):

        registro = await FiscalImpostosService.get_by_id(id_imposto, db)

        if not registro:
            return None

        for campo, valor in dto.model_dump().items():
            setattr(registro, campo, valor)

        await db.commit()
        await db.refresh(registro)
        return registro

    @staticmethod
    async def delete(id_imposto: int, db: AsyncSession):

        registro = await FiscalImpostosService.get_by_id(id_imposto, db)

        if not registro:
            return None

        await db.delete(registro)
        await db.commit()
        return True
