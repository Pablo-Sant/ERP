from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.financeiro_orcamento import FinanceiroOrcamentos


class FinanceiroOrcamentosService:

    @staticmethod
    async def create(dto, db: AsyncSession) -> FinanceiroOrcamentos:

        novo = FinanceiroOrcamentos(**dto.model_dump())
        db.add(novo)

        await db.commit()
        await db.refresh(novo)
        return novo

    @staticmethod
    async def get_all(db: AsyncSession):

        result = await db.execute(
            select(FinanceiroOrcamentos)
            .order_by(FinanceiroOrcamentos.ano, FinanceiroOrcamentos.mes)
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_id(id_orcamento: int, db: AsyncSession) -> FinanceiroOrcamentos | None:

        result = await db.execute(
            select(FinanceiroOrcamentos)
            .filter(FinanceiroOrcamentos.id_orcamento == id_orcamento)
        )
        return result.scalars().first()

    @staticmethod
    async def update(id_orcamento: int, dto, db: AsyncSession):

        registro = await FinanceiroOrcamentosService.get_by_id(id_orcamento, db)

        if not registro:
            return None

        for campo, valor in dto.model_dump().items():
            setattr(registro, campo, valor)

        await db.commit()
        await db.refresh(registro)
        return registro

    @staticmethod
    async def delete(id_orcamento: int, db: AsyncSession):

        registro = await FinanceiroOrcamentosService.get_by_id(id_orcamento, db)

        if not registro:
            return None

        await db.delete(registro)
        await db.commit()
        return True
