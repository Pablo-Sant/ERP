from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.financeiro_extrato import FinanceiroExtratosBancarios
from models.financeiro_conta import FinanceiroContas
from schemas.financeiro_extratos_bancarios import (
    FinanceiroExtratoCreate,
    FinanceiroExtratoUpdate
)


class FinanceiroExtratoService:
    

    @staticmethod
    async def listar(db: AsyncSession):
        result = await db.execute(select(FinanceiroExtratosBancarios))
        return result.scalars().all()


    @staticmethod
    async def obter_por_id(id_extrato: int, db: AsyncSession):
        result = await db.execute(
            select(FinanceiroExtratosBancarios)
            .filter(FinanceiroExtratosBancarios.id_extrato == id_extrato)
        )
        extrato = result.scalar_one_or_none()

        if not extrato:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Extrato bancário não encontrado."
            )

        return extrato

    
    @staticmethod
    async def _validar_relacionamentos(dto, db: AsyncSession):
        """Validação de conta vinculada."""
        result = await db.execute(
            select(FinanceiroContas).filter(FinanceiroContas.id_conta == dto.id_conta)
        )
        conta = result.scalar_one_or_none()

        if not conta:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A conta vinculada ao extrato não existe."
            )

    
    @staticmethod
    def _validar_dados(dto):
        if dto.valor is not None and dto.valor == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O valor da movimentação não pode ser zero."
            )

        if dto.tipo not in ("credito", "debito"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo inválido. Use: 'credito' ou 'debito'."
            )

        if dto.data_movimento is not None and dto.data_movimento > date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A data de movimento não pode estar no futuro."
            )

    
    @staticmethod
    async def criar(dto: FinanceiroExtratoCreate, db: AsyncSession):
        FinanceiroExtratoService._validar_dados(dto)
        await FinanceiroExtratoService._validar_relacionamentos(dto, db)

        novo = FinanceiroExtratosBancarios(**dto.model_dump())

        db.add(novo)
        await db.commit()
        await db.refresh(novo)

        return novo

    
    @staticmethod
    async def atualizar(id_extrato: int, dto: FinanceiroExtratoUpdate, db: AsyncSession):
        existente = await FinanceiroExtratoService.obter_por_id(id_extrato, db)

        if existente.conciliado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é permitido alterar um extrato já conciliado."
            )

        FinanceiroExtratoService._validar_dados(dto)

        if dto.id_conta is not None:
            await FinanceiroExtratoService._validar_relacionamentos(dto, db)

        data = dto.model_dump(exclude_unset=True)

        for attr, value in data.items():
            setattr(existente, attr, value)

        await db.commit()
        await db.refresh(existente)

        return existente

    
    @staticmethod
    async def deletar(id_extrato: int, db: AsyncSession):
        existente = await FinanceiroExtratoService.obter_por_id(id_extrato, db)

        if existente.conciliado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é permitido excluir um extrato conciliado."
            )

        await db.delete(existente)
        await db.commit()

        return True
