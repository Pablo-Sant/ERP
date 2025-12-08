from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from models.mm_empresas_model import Empresa


class EmpresaService:
    """Serviço para gerenciar operações de empresas"""

    @staticmethod
    async def criar(dto, db: AsyncSession) -> Empresa:
        """
        Cria uma nova empresa
        
        Args:
            dto: Objeto de transferência de dados (Pydantic model)
            db: Sessão do banco de dados
            
        Returns:
            Empresa: Objeto da empresa criada
            
        Raises:
            ValueError: Se o CNPJ/CPF já estiver cadastrado
        """
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
        """
        Retorna todas as empresas cadastradas
        
        Args:
            db: Sessão do banco de dados
            
        Returns:
            List[Empresa]: Lista de empresas
        """
        result = await db.execute(
            select(Empresa)
            .order_by(Empresa.nome)
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_id(empresa_id: int, db: AsyncSession) -> Optional[Empresa]:
        """
        Busca empresa por ID
        
        Args:
            empresa_id: ID da empresa
            db: Sessão do banco de dados
            
        Returns:
            Optional[Empresa]: Empresa encontrada ou None
        """
        result = await db.execute(
            select(Empresa)
            .filter(Empresa.id == empresa_id)
        )
        return result.scalars().first()

    @staticmethod
    async def buscar_por_cpf_cnpj(cpf_cnpj: str, db: AsyncSession) -> Optional[Empresa]:
        """
        Busca empresa por CPF/CNPJ
        
        Args:
            cpf_cnpj: CPF ou CNPJ da empresa
            db: Sessão do banco de dados
            
        Returns:
            Optional[Empresa]: Empresa encontrada ou None
        """
        if not cpf_cnpj:
            return None
            
        result = await db.execute(
            select(Empresa)
            .filter(Empresa.cpf_cnpj == cpf_cnpj)
        )
        return result.scalars().first()

    @staticmethod
    async def buscar_por_nome(nome: str, db: AsyncSession) -> List[Empresa]:
        """
        Busca empresas por nome (busca parcial)
        
        Args:
            nome: Nome ou parte do nome da empresa
            db: Sessão do banco de dados
            
        Returns:
            List[Empresa]: Lista de empresas encontradas
        """
        result = await db.execute(
            select(Empresa)
            .filter(Empresa.nome.ilike(f"%{nome}%"))
            .order_by(Empresa.nome)
        )
        return result.scalars().all()

    @staticmethod
    async def update(empresa_id: int, dto, db: AsyncSession) -> Optional[Empresa]:
        """
        Atualiza uma empresa existente
        
        Args:
            empresa_id: ID da empresa a ser atualizada
            dto: Objeto de transferência de dados com as alterações
            db: Sessão do banco de dados
            
        Returns:
            Optional[Empresa]: Empresa atualizada ou None se não encontrada
            
        Raises:
            ValueError: Se o CNPJ/CPF já estiver cadastrado em outra empresa
        """
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
        """
        Remove uma empresa
        
        Args:
            empresa_id: ID da empresa a ser removida
            db: Sessão do banco de dados
            
        Returns:
            bool: True se removida, False se não encontrada
            
        Raises:
            ValueError: Se a empresa tiver produtos vinculados
        """
        empresa = await EmpresaService.get_by_id(empresa_id, db)
        
        if not empresa:
            return False

        # TODO: Verificar se empresa tem produtos vinculados
        # Isso requer importar o modelo Produto e verificar relacionamentos
        # from models.mm_produto_model import Produto
        # produtos_count = await db.execute(
        #     select(func.count(Produto.id))
        #     .filter(Produto.empresa_id == empresa_id)
        # )
        # if produtos_count.scalar() > 0:
        #     raise ValueError("Não é possível excluir empresa com produtos vinculados")

        await db.delete(empresa)
        await db.commit()
        return True

    @staticmethod
    async def validar_cpf_cnpj(cpf_cnpj: str) -> None:
        """
        Valida formato do CPF/CNPJ
        
        Args:
            cpf_cnpj: CPF ou CNPJ a ser validado
            
        Raises:
            ValueError: Se o CPF/CNPJ for inválido
        """
        if not cpf_cnpj:
            return
            
        # Remove caracteres não numéricos
        numeros = ''.join(filter(str.isdigit, cpf_cnpj))
        
        # Validação básica de tamanho
        if len(numeros) not in (11, 14):  # CPF tem 11, CNPJ tem 14
            raise ValueError(f"CPF/CNPJ inválido: {cpf_cnpj}")

    @staticmethod
    async def verificar_empresa_ativa(empresa_id: int, db: AsyncSession) -> bool:
        """
        Verifica se uma empresa existe e está ativa
        
        Args:
            empresa_id: ID da empresa
            db: Sessão do banco de dados
            
        Returns:
            bool: True se empresa existe
            
        Raises:
            ValueError: Se empresa não for encontrada
        """
        empresa = await EmpresaService.get_by_id(empresa_id, db)
        
        if not empresa:
            raise ValueError(f"Empresa com ID {empresa_id} não encontrada")
            
        # Se tiver campo ativo/inativo, adicione a verificação:
        # if hasattr(empresa, 'ativo') and not empresa.ativo:
        #     raise ValueError(f"Empresa com ID {empresa_id} está inativa")
            
        return True

    @staticmethod
    async def get_empresas_com_produtos(db: AsyncSession) -> List[Empresa]:
        """
        Retorna empresas que possuem produtos cadastrados
        
        Args:
            db: Sessão do banco de dados
            
        Returns:
            List[Empresa]: Lista de empresas com produtos
        """
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
        """
        Retorna contagem de produtos por empresa
        
        Args:
            db: Sessão do banco de dados
            
        Returns:
            dict: Dicionário com ID da empresa e quantidade de produtos
        """
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