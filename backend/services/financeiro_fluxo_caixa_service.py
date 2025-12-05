from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.financeiro_fluxo_caixa import FinanceiroFluxoCaixa


class FinanceiroFluxoCaixaService:

    @staticmethod
    async def create(dto, db: AsyncSession) -> FinanceiroFluxoCaixa:

        novo_registro = FinanceiroFluxoCaixa(
            **dto.model_dump()
        )

        db.add(novo_registro)
        await db.commit()
        await db.refresh(novo_registro)
        return novo_registro

    @staticmethod
    async def get_all(db: AsyncSession):

        result = await db.execute(
            select(FinanceiroFluxoCaixa).order_by(FinanceiroFluxoCaixa.data)
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_id(id_fluxo: int, db: AsyncSession):

        result = await db.execute(
            select(FinanceiroFluxoCaixa).filter(FinanceiroFluxoCaixa.id_fluxo == id_fluxo)
        )
        return result.scalars().first()

    @staticmethod
    async def update(id_fluxo: int, dto, db: AsyncSession):

        result = await db.execute(
            select(FinanceiroFluxoCaixa).filter(FinanceiroFluxoCaixa.id_fluxo == id_fluxo)
        )
        registro = result.scalars().first()

        if not registro:
            return None

        for campo, valor in dto.model_dump().items():
            setattr(registro, campo, valor)

        await db.commit()
        await db.refresh(registro)
        return registro

    @staticmethod
    async def delete(id_fluxo: int, db: AsyncSession):
        """
        Exclui um registro pelo ID.
        """
        result = await db.execute(
            select(FinanceiroFluxoCaixa).filter(FinanceiroFluxoCaixa.id_fluxo == id_fluxo)
        )
        registro = result.scalars().first()

        if not registro:
            return None

        await db.delete(registro)
        await db.commit()
        return True
