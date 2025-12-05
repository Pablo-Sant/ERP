from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from models.am_pecas_ordem_servico import PecasOrdemServico
from schemas.peca_ordem_servico_schema import PecasOrdemServicoCreate


class PecasOrdemServicoService:

    @staticmethod
    async def listar(db: AsyncSession):
        result = await db.execute(select(PecasOrdemServico))
        return result.scalars().all()


    @staticmethod
    async def obter_por_id(id: int, db: AsyncSession):
        result = await db.execute(
            select(PecasOrdemServico).filter(PecasOrdemServico.id == id)
        )
        peca = result.scalar_one_or_none()

        if not peca:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Peça de ordem de serviço não encontrada"
            )

        return peca


    @staticmethod
    async def criar(dto: PecasOrdemServicoCreate, db: AsyncSession):
        nova = PecasOrdemServico(
            id_ordem_servico=dto.id_ordem_servico,
            numero_peca=dto.numero_peca,
            nome_peca=dto.nome_peca,
            quantidade=dto.quantidade,
            custo_unitario=dto.custo_unitario
            # custo_total não é necessário, pois é calculado pelo banco
        )

        db.add(nova)
        await db.commit()
        await db.refresh(nova)

        return nova


    @staticmethod
    async def atualizar(id: int, dto: PecasOrdemServicoCreate, db: AsyncSession):
        existente = await PecasOrdemServicoService.obter_por_id(id, db)

        existente.id_ordem_servico = dto.id_ordem_servico
        existente.numero_peca = dto.numero_peca
        existente.nome_peca = dto.nome_peca
        existente.quantidade = dto.quantidade
        existente.custo_unitario = dto.custo_unitario

        await db.commit()
        await db.refresh(existente)

        return existente


    @staticmethod
    async def deletar(id: int, db: AsyncSession):
        existente = await PecasOrdemServicoService.obter_por_id(id, db)

        await db.delete(existente)
        await db.commit()

        return True
