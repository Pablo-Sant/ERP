from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from models.am_planos_manutencao_model import PlanosManutencao
from schemas.planos_manutencao_schema import (
    PlanosManutencaoCreate,
    PlanosManutencaoUpdate
)


class PlanosManutencaoService:


    @staticmethod
    async def listar(db: AsyncSession):
        result = await db.execute(select(PlanosManutencao))
        return result.scalars().all()


    @staticmethod
    async def obter_por_id(id: int, db: AsyncSession):
        result = await db.execute(
            select(PlanosManutencao).filter(PlanosManutencao.id == id)
        )
        plano = result.scalar_one_or_none()

        if not plano:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plano de manutenção não encontrado"
            )

        return plano


    @staticmethod
    async def criar(dto: PlanosManutencaoCreate, db: AsyncSession):
        
        if dto.custo_estimado is not None and dto.custo_estimado < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O custo estimado não pode ser negativo."
            )
        novo = PlanosManutencao(**dto.model_dump())


        db.add(novo)
        await db.commit()
        await db.refresh(novo)

        return novo


    @staticmethod
    async def atualizar(id: int, dto: PlanosManutencaoUpdate, db: AsyncSession):
        existente = await PlanosManutencaoService.obter_por_id(id, db)

        if dto.custo_estimado is not None and dto.custo_estimado < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O custo estimado não pode ser negativo."
            )
        
        data = dto.model_dump(exclude_unset=True)

    
        for attr, value in data.items():
            setattr(existente, attr, value)

        await db.commit()
        await db.refresh(existente)

        return existente


    @staticmethod
    async def deletar(id: int, db: AsyncSession):
        existente = await PlanosManutencaoService.obter_por_id(id, db)

        
        await db.delete(existente)
        await db.commit()

        return True
