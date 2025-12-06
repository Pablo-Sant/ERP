from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.rh_avaliacao_desempenho_model import AvaliacaoDesempenho
from models.rh_colaboradores_model import Colaborador

class AvaliacaoDesempenhoService:
    
    @staticmethod
    async def validar_colaborador(id_colaborador: int, db: AsyncSession):
        result = await db.execute(
            select(Colaborador).filter(Colaborador.id == id_colaborador)
        )
        
        colaborador = result.scalars().first()
        
        if not colaborador:
            raise ValueError(f'Colaborador com id {id_colaborador} não encontrado')
        
        return colaborador
    
    
    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(
            select(AvaliacaoDesempenho).order_by(AvaliacaoDesempenho.id)
        )
        
        return result.scalars().all()
    
    
    @staticmethod
    async def get_by_id(id: int, db: AsyncSession):
        result = await db.execute(
            select(AvaliacaoDesempenho).filter(AvaliacaoDesempenho.id == id)
        )
        
        avaliacao = result.scalars().first()
        
        if not avaliacao:
            raise ValueError('Avaliacao Desempenho não encontrada')
        
        return avaliacao
    
    @staticmethod
    async def post(dto, db: AsyncSession):
        
        await AvaliacaoDesempenhoService.get_by_id(id, db)
        
     
        novo = AvaliacaoDesempenho(
            **dto.model_dump()
        )

        db.add(novo)
        await db.commit()
        await db.refresh(novo)
        return novo
    
    
    @staticmethod
    async def update(id: int, dto, db: AsyncSession):

        registro = await AvaliacaoDesempenhoService.get_by_id(id, db)

        if not registro:
            return None

        for campo, valor in dto.model_dump().items():
            setattr(registro, campo, valor)

        await db.commit()
        await db.refresh(registro)
        return registro

    @staticmethod
    async def delete(id: int, db: AsyncSession):

        registro = await AvaliacaoDesempenhoService.get_by_id(id, db)

        if not registro:
            return None

        await db.delete(registro)
        await db.commit()
        return True
