from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.mm_produto_model import Produto
from models.mm_empresas_model import Empresa
from models.mm_categorias_model import Categoria


class ProdutoService:

    @staticmethod
    async def verificar_empresa_id(empresa_id: int, db: AsyncSession):
        result = await db.execute(
            select(Empresa).filter(Empresa.id == empresa_id)
        )
        empresa = result.scalars().first()

        if not empresa:
            raise ValueError(f"Empresa com ID {empresa_id} não encontrada")

        return empresa
    

    @staticmethod
    async def verificar_categoria_id(categoria_id: int, db: AsyncSession):
        result =  await db.execute(
            select(Categoria).filter(Categoria.id == categoria_id)
        )
        
        categoria = result.scalars().first()
        
        if not categoria:
            raise ValueError(f'Categoria com ID {categoria_id} não encontrada')
        
        return categoria
        
        
    @staticmethod
    async def criar(dto, db: AsyncSession):
        
        await ProdutoService.verificar_empresa_id(dto.empresa_id, db)

        novo = Produto(**dto.model_dump())

        db.add(novo)
        await db.commit()
        await db.refresh(novo)

        return novo
    
    @staticmethod
    async def get_all(db: AsyncSession):

        result = await db.execute(
            select(Produto)
            .order_by(Produto.id)
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_id(id_imposto: int, db: AsyncSession) -> Produto | None:

        result = await db.execute(
            select(Produto)
            .filter(Produto.id == id_imposto)
        )
        return result.scalars().first()

    @staticmethod
    async def update(id_imposto: int, dto, db: AsyncSession):

        registro = await ProdutoService.get_by_id(id_imposto, db)
        await ProdutoService.verificar_empresa_id(dto.empresa_id, db)
        await ProdutoService.verificar_categoria_id(dto.categoria_id, db)

        if not registro:
            return None

        for campo, valor in dto.model_dump().items():
            setattr(registro, campo, valor)

        await db.commit()
        await db.refresh(registro)
        return registro

    @staticmethod
    async def delete(id_imposto: int, db: AsyncSession):

        registro = await ProdutoService.get_by_id(id_imposto, db)

        if not registro:
            return None

        await db.delete(registro)
        await db.commit()
        return True
    

        
