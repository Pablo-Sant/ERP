from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from models.mm_empresas_model import Empresa


class EmpresaService:
    """Serviço para gerenciar operações de empresas"""

    @staticmethod
    async def criar(dto, db: AsyncSession) -> Empresa:

        # Verifica se já existe empresa com mesmo CNPJ/CPF
        if dto.cpf_cnpj:
            empresa_existente = await EmpresaService.buscar_por_cpf_cnpj(
                dto.cpf_cnpj, db
            )
            if empresa_existente:
                raise ValueError(f"CPF/CNPJ {dto.cpf_cnpj} já cadastrado")

        # Validações específicas
        await EmpresaService.validar_cpf_cnpj(dto.cpf_cnpj)

        # Cria nova empresa
        nova_empresa = Empresa(**dto.model_dump())
        
        db.add(nova_empresa)
        await db.commit()
        await db.refresh(nova_empresa)

        return nova_empresa

    @staticmethod
    async def get_all(db: AsyncSession) -> List[Empresa]:

        result = await db.execute(
            select(Empresa)
            .order_by(Empresa.nome)
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_id(empresa_id: int, db: AsyncSession) -> Optional[Empresa]:

        result = await db.execute(
            select(Empresa)
            .filter(Empresa.id == empresa_id)
        )
        return result.scalars().first()

    @staticmethod
    async def buscar_por_cpf_cnpj(cpf_cnpj: str, db: AsyncSession) -> Optional[Empresa]:

        if not cpf_cnpj:
            return None
            
        result = await db.execute(
            select(Empresa)
            .filter(Empresa.cpf_cnpj == cpf_cnpj)
        )
        return result.scalars().first()

    @staticmethod
    async def buscar_por_nome(nome: str, db: AsyncSession) -> List[Empresa]:

        result = await db.execute(
            select(Empresa)
            .filter(Empresa.nome.ilike(f"%{nome}%"))
            .order_by(Empresa.nome)
        )
        return result.scalars().all()

    @staticmethod
    async def update(empresa_id: int, dto, db: AsyncSession) -> Optional[Empresa]:

        empresa = await EmpresaService.get_by_id(empresa_id, db)
        
        if not empresa:
            return None

        # Valida CPF/CNPJ se for alterado
        if dto.cpf_cnpj and dto.cpf_cnpj != empresa.cpf_cnpj:
            await EmpresaService.validar_cpf_cnpj(dto.cpf_cnpj)
            
            # Verifica se novo CPF/CNPJ já existe em outra empresa
            empresa_existente = await EmpresaService.buscar_por_cpf_cnpj(
                dto.cpf_cnpj, db
            )
            if empresa_existente and empresa_existente.id != empresa_id:
                raise ValueError(f"CPF/CNPJ {dto.cpf_cnpj} já cadastrado em outra empresa")

        # Atualiza campos
        for campo, valor in dto.model_dump(exclude_unset=True).items():
            setattr(empresa, campo, valor)

        await db.commit()
        await db.refresh(empresa)
        return empresa

    @staticmethod
    async def delete(empresa_id: int, db: AsyncSession) -> bool:

        empresa = await EmpresaService.get_by_id(empresa_id, db)
        
        if not empresa:
            return False


        await db.delete(empresa)
        await db.commit()
        return True

    @staticmethod
    async def validar_cpf_cnpj(cpf_cnpj: str) -> None:

        if not cpf_cnpj:
            return
            
        numeros = ''.join(filter(str.isdigit, cpf_cnpj))
        
        # Validação básica de tamanho
        if len(numeros) not in (11, 14):  # CPF tem 11, CNPJ tem 14
            raise ValueError(f"CPF/CNPJ inválido: {cpf_cnpj}")

    @staticmethod
    async def verificar_empresa_ativa(empresa_id: int, db: AsyncSession) -> bool:

        empresa = await EmpresaService.get_by_id(empresa_id, db)
        
        if not empresa:
            raise ValueError(f"Empresa com ID {empresa_id} não encontrada")
            
            
        return True

    @staticmethod
    async def get_empresas_com_produtos(db: AsyncSession) -> List[Empresa]:
        from models.mm_produto_model import Produto
        from sqlalchemy import func
        
        result = await db.execute(
            select(Empresa)
            .join(Produto, Empresa.id == Produto.empresa_id)
            .group_by(Empresa.id)
            .having(func.count(Produto.id) > 0)
            .order_by(Empresa.nome)
        )
        return result.scalars().all()

    @staticmethod
    async def get_contagem_produtos_por_empresa(db: AsyncSession) -> dict:

        from models.mm_produto_model import Produto
        from sqlalchemy import func
        
        result = await db.execute(
            select(
                Empresa.id,
                Empresa.nome,
                func.count(Produto.id).label('quantidade_produtos')
            )
            .outerjoin(Produto, Empresa.id == Produto.empresa_id)
            .group_by(Empresa.id, Empresa.nome)
            .order_by(Empresa.nome)
        )
        
        return {
            row[0]: {
                'nome': row[1],
                'quantidade_produtos': row[2]
            }
            for row in result.all()
        }