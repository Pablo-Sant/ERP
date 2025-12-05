from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.financeiro_conta import FinanceiroContas
from schemas.financeiro_contas_financeiras import FinanceiroContaCreate, FinanceiroContaUpdate


class FinanceiroContaService:

    
    @staticmethod
    async def listar(db: AsyncSession):
        result = await db.execute(select(FinanceiroContas))
        return result.scalars().all()

    
    @staticmethod
    async def obter_por_id(id_conta: int, db: AsyncSession):
        result = await db.execute(
            select(FinanceiroContas).filter(FinanceiroContas.id_conta == id_conta)
        )
        conta = result.scalar_one_or_none()

        if not conta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conta financeira não encontrada."
            )

        return conta

    
    @staticmethod
    def _validar_dados(dto):
        if dto.saldo_inicial is not None and dto.saldo_inicial < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O saldo inicial não pode ser negativo."
            )

        if dto.data_abertura is not None and dto.data_abertura > date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A data de abertura não pode estar no futuro."
            )

        if dto.tipo not in ("caixa", "banco", "cartao"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de conta inválido. Use: 'caixa', 'banco' ou 'cartao'."
            )

    
    @staticmethod
    async def criar(dto: FinanceiroContaCreate, db: AsyncSession):
        FinanceiroContaService._validar_dados(dto)

        nova = FinanceiroContas(**dto.model_dump())

        db.add(nova)
        await db.commit()
        await db.refresh(nova)

        return nova

    
    @staticmethod
    async def atualizar(id_conta: int, dto: FinanceiroContaUpdate, db: AsyncSession):
        existente = await FinanceiroContaService.obter_por_id(id_conta, db)

        FinanceiroContaService._validar_dados(dto)

        data = dto.model_dump(exclude_unset=True)

        for attr, value in data.items():
            setattr(existente, attr, value)

        await db.commit()
        await db.refresh(existente)

        return existente

   
    @staticmethod
    async def deletar(id_conta: int, db: AsyncSession):
        existente = await FinanceiroContaService.obter_por_id(id_conta, db)

        # Regra de negócio comum
        if existente.lancamentos and len(existente.lancamentos) > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível excluir uma conta que possui lançamentos financeiros."
            )

        await db.delete(existente)
        await db.commit()

        return True
