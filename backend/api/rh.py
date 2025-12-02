"""
API Completa de Recursos Humanos (RH)
Integra todos os módulos do sistema de RH
"""

from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from datetime import date
import uvicorn

# Importando models e schemas (simulando a importação)
# Como estamos em um único arquivo, vamos usar as classes diretamente
from typing import Any

# ============================================================================
# CONFIGURAÇÃO DO APLICATIVO
# ============================================================================

app = FastAPI(
    title="API de Recursos Humanos",
    description="API completa para gestão de Recursos Humanos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# SIMULAÇÃO DO BANCO DE DADOS (para exemplo)
# ============================================================================

# Em um cenário real, você teria a configuração do banco aqui
# from core.database import get_db, engine
# DBBaseModel.metadata.create_all(bind=engine)

# ============================================================================
# SCHEMAS (baseados nos arquivos fornecidos)
# ============================================================================

from pydantic import BaseModel, Field, EmailStr, validator
from datetime import date, datetime
from typing import Optional

# ----------------------------------------------------------------------------
# Schemas de Colaborador
# ----------------------------------------------------------------------------

class ColaboradorBase(BaseModel):
    nome: str = Field(..., max_length=100)
    cpf: str = Field(..., min_length=11, max_length=11)
    email: Optional[EmailStr] = Field(None, max_length=100)
    funcao_id: Optional[int] = None
    data_contratacao: date
    carga_horaria: int = Field(..., ge=1, le=168)
    data_de_nascimento: Optional[date] = None
    data_de_recrutamento: date
    salario: float = Field(..., ge=0)
    ativo: Optional[int] = Field(default=1, ge=0, le=1)
    
    @validator('cpf')
    def validar_cpf(cls, v):
        if len(v) != 11 or not v.isdigit():
            raise ValueError('CPF deve conter 11 dígitos numéricos')
        return v
    
    @validator('data_de_recrutamento')
    def validar_datas(cls, v, values):
        if 'data_contratacao' in values and v > values['data_contratacao']:
            raise ValueError('Data de recrutamento não pode ser posterior à data de contratação')
        return v

class ColaboradorCreate(ColaboradorBase):
    pass

class ColaboradorUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = Field(None, max_length=100)
    funcao_id: Optional[int] = None
    carga_horaria: Optional[int] = Field(None, ge=1, le=168)
    data_de_nascimento: Optional[date] = None
    salario: Optional[float] = Field(None, ge=0)
    ativo: Optional[int] = Field(None, ge=0, le=1)

class ColaboradorResponse(ColaboradorBase):
    id: int
    data_criacao: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ----------------------------------------------------------------------------
# Schemas de Função
# ----------------------------------------------------------------------------

class FuncaoBase(BaseModel):
    nome: str = Field(..., max_length=50)
    descricao: Optional[str] = Field(None, max_length=200)

class FuncaoCreate(FuncaoBase):
    pass

class FuncaoUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=50)
    descricao: Optional[str] = Field(None, max_length=200)

class FuncaoResponse(FuncaoBase):
    id: int
    
    class Config:
        from_attributes = True

# ----------------------------------------------------------------------------
# Schemas de Folha de Pagamento
# ----------------------------------------------------------------------------

class FolhaPagamentoBase(BaseModel):
    colaborador_id: int
    mes: int = Field(..., ge=1, le=12)
    ano: int = Field(..., ge=2000, le=2100)
    salario_base: float = Field(..., ge=0)
    descontos: Optional[float] = Field(None, ge=0)
    salario_liquido: float = Field(..., ge=0)

class FolhaPagamentoCreate(FolhaPagamentoBase):
    pass

class FolhaPagamentoUpdate(BaseModel):
    descontos: Optional[float] = Field(None, ge=0)
    salario_liquido: Optional[float] = Field(None, ge=0)

class FolhaPagamentoResponse(FolhaPagamentoBase):
    id: int
    
    class Config:
        from_attributes = True

# ----------------------------------------------------------------------------
# Schemas de Recrutamento
# ----------------------------------------------------------------------------

class RecrutamentoBase(BaseModel):
    colaborador_id: int
    data_recrutamento: date
    status: str = Field(..., max_length=50)
    observacoes: Optional[str] = Field(None, max_length=200)

class RecrutamentoCreate(RecrutamentoBase):
    pass

class RecrutamentoUpdate(BaseModel):
    status: Optional[str] = Field(None, max_length=50)
    observacoes: Optional[str] = Field(None, max_length=200)

class RecrutamentoResponse(RecrutamentoBase):
    id: int
    
    class Config:
        from_attributes = True

# ----------------------------------------------------------------------------
# Schemas de Avaliação de Desempenho
# ----------------------------------------------------------------------------

class AvaliacaoDesempenhoBase(BaseModel):
    colaborador_id: int
    data_avaliacao: date
    nota: int = Field(..., ge=0, le=10)
    comentarios: Optional[str] = Field(None, max_length=200)

class AvaliacaoDesempenhoCreate(AvaliacaoDesempenhoBase):
    pass

class AvaliacaoDesempenhoUpdate(BaseModel):
    nota: Optional[int] = Field(None, ge=0, le=10)
    comentarios: Optional[str] = Field(None, max_length=200)

class AvaliacaoDesempenhoResponse(AvaliacaoDesempenhoBase):
    id: int
    
    class Config:
        from_attributes = True

# ----------------------------------------------------------------------------
# Schemas de Benefício
# ----------------------------------------------------------------------------

class BeneficioBase(BaseModel):
    nome: str = Field(..., max_length=50)
    descricao: Optional[str] = Field(None, max_length=200)
    valor: Optional[float] = Field(None, ge=0)

class BeneficioCreate(BeneficioBase):
    pass

class BeneficioUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=50)
    descricao: Optional[str] = Field(None, max_length=200)
    valor: Optional[float] = Field(None, ge=0)

class BeneficioResponse(BeneficioBase):
    id: int
    
    class Config:
        from_attributes = True

# ----------------------------------------------------------------------------
# Schemas de ColaboradorBeneficio (Associação)
# ----------------------------------------------------------------------------

class ColaboradorBeneficioBase(BaseModel):
    colaborador_id: int
    beneficio_id: int

class ColaboradorBeneficioCreate(ColaboradorBeneficioBase):
    pass

class ColaboradorBeneficioResponse(ColaboradorBeneficioBase):
    id: int
    
    class Config:
        from_attributes = True

# ============================================================================
# ENDPOINTS DE COLABORADORES
# ============================================================================

@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "API de Recursos Humanos",
        "version": "1.0.0",
        "documentation": "/docs"
    }

@app.get("/colaboradores", response_model=List[ColaboradorResponse])
async def listar_colaboradores(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    ativo: Optional[int] = Query(None, ge=0, le=1)
):
    """
    Lista todos os colaboradores com paginação.
    
    - **skip**: Número de registros a pular
    - **limit**: Limite de registros por página
    - **ativo**: Filtrar por status ativo (1) ou inativo (0)
    """
    # Em um cenário real, você faria a consulta ao banco:
    # db.query(Colaborador).filter(...).offset(skip).limit(limit).all()
    
    return []  # Placeholder para a resposta real

@app.post("/colaboradores", response_model=ColaboradorResponse, status_code=status.HTTP_201_CREATED)
async def criar_colaborador(colaborador: ColaboradorCreate):
    """
    Cria um novo colaborador.
    
    - Valida CPF (11 dígitos)
    - Valida datas (recrutamento <= contratação)
    - Valida carga horária (1-168 horas)
    """
    try:
        # Em um cenário real:
        # db_colaborador = Colaborador(**colaborador.dict())
        # db.add(db_colaborador)
        # db.commit()
        # db.refresh(db_colaborador)
        
        # Simulação de resposta
        response_data = colaborador.dict()
        response_data["id"] = 1  # ID simulado
        response_data["data_criacao"] = datetime.now()
        response_data["data_atualizacao"] = datetime.now()
        
        return response_data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado ou dados inválidos"
        )

@app.get("/colaboradores/{colaborador_id}", response_model=ColaboradorResponse)
async def obter_colaborador(colaborador_id: int):
    """
    Obtém um colaborador específico pelo ID.
    """
    # Em um cenário real:
    # colaborador = db.query(Colaborador).filter(Colaborador.id == colaborador_id).first()
    
    if colaborador_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colaborador não encontrado"
        )
    
    # Simulação de resposta
    return {
        "id": colaborador_id,
        "nome": "João Silva",
        "cpf": "12345678901",
        "email": "joao@empresa.com",
        "funcao_id": 1,
        "data_contratacao": date(2023, 1, 15),
        "carga_horaria": 40,
        "data_de_nascimento": date(1990, 5, 20),
        "data_de_recrutamento": date(2023, 1, 10),
        "salario": 5000.00,
        "ativo": 1,
        "data_criacao": datetime.now(),
        "data_atualizacao": datetime.now()
    }

@app.put("/colaboradores/{colaborador_id}", response_model=ColaboradorResponse)
async def atualizar_colaborador(colaborador_id: int, colaborador_update: ColaboradorUpdate):
    """
    Atualiza um colaborador existente.
    
    - Apenas campos fornecidos são atualizados
    """
    # Em um cenário real:
    # db_colaborador = db.query(Colaborador).filter(Colaborador.id == colaborador_id).first()
    # if not db_colaborador:
    #     raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    
    if colaborador_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colaborador não encontrado"
        )
    
    # Simulação de atualização
    update_data = colaborador_update.dict(exclude_unset=True)
    
    return {
        "id": colaborador_id,
        "nome": "João Silva Atualizado",
        "cpf": "12345678901",
        "email": "joao.atualizado@empresa.com",
        "funcao_id": 2,
        "data_contratacao": date(2023, 1, 15),
        "carga_horaria": 44,
        "data_de_nascimento": date(1990, 5, 20),
        "data_de_recrutamento": date(2023, 1, 10),
        "salario": 5500.00,
        "ativo": 1,
        "data_criacao": datetime.now(),
        "data_atualizacao": datetime.now()
    }

@app.delete("/colaboradores/{colaborador_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_colaborador(colaborador_id: int):
    """
    Remove um colaborador (soft delete).
    
    - Na verdade, marca como inativo (ativo=0)
    """
    # Em um cenário real:
    # db_colaborador = db.query(Colaborador).filter(Colaborador.id == colaborador_id).first()
    # if not db_colaborador:
    #     raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    
    # db_colaborador.ativo = 0
    # db.commit()
    
    if colaborador_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colaborador não encontrado"
        )
    
    return

# ============================================================================
# ENDPOINTS DE FUNÇÕES
# ============================================================================

@app.get("/funcoes", response_model=List[FuncaoResponse])
async def listar_funcoes():
    """Lista todas as funções cadastradas"""
    return []  # Placeholder

@app.post("/funcoes", response_model=FuncaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_funcao(funcao: FuncaoCreate):
    """Cria uma nova função"""
    try:
        # Simulação de criação
        response_data = funcao.dict()
        response_data["id"] = 1
        return response_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar função: {str(e)}"
        )

@app.get("/funcoes/{funcao_id}", response_model=FuncaoResponse)
async def obter_funcao(funcao_id: int):
    """Obtém uma função específica pelo ID"""
    if funcao_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Função não encontrada"
        )
    
    return {
        "id": funcao_id,
        "nome": "Desenvolvedor",
        "descricao": "Desenvolvimento de software"
    }

@app.put("/funcoes/{funcao_id}", response_model=FuncaoResponse)
async def atualizar_funcao(funcao_id: int, funcao_update: FuncaoUpdate):
    """Atualiza uma função existente"""
    if funcao_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Função não encontrada"
        )
    
    return {
        "id": funcao_id,
        "nome": "Desenvolvedor Atualizado",
        "descricao": "Desenvolvimento de software atualizado"
    }

# ============================================================================
# ENDPOINTS DE FOLHA DE PAGAMENTO
# ============================================================================

@app.get("/folha-pagamento", response_model=List[FolhaPagamentoResponse])
async def listar_folhas_pagamento(
    colaborador_id: Optional[int] = None,
    mes: Optional[int] = Query(None, ge=1, le=12),
    ano: Optional[int] = Query(None, ge=2000, le=2100),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    Lista folhas de pagamento com filtros.
    
    - Filtrar por colaborador, mês e/ou ano
    """
    return []  # Placeholder

@app.post("/folha-pagamento", response_model=FolhaPagamentoResponse, status_code=status.HTTP_201_CREATED)
async def criar_folha_pagamento(folha: FolhaPagamentoCreate):
    """Cria uma nova folha de pagamento"""
    try:
        # Validação adicional
        if folha.salario_liquido > folha.salario_base:
            raise ValueError("Salário líquido não pode ser maior que o salário base")
        
        if folha.descontos and folha.descontos > folha.salario_base:
            raise ValueError("Descontos não podem ser maiores que o salário base")
        
        # Simulação de criação
        response_data = folha.dict()
        response_data["id"] = 1
        return response_data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@app.get("/folha-pagamento/{folha_id}", response_model=FolhaPagamentoResponse)
async def obter_folha_pagamento(folha_id: int):
    """Obtém uma folha de pagamento específica pelo ID"""
    if folha_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folha de pagamento não encontrada"
        )
    
    return {
        "id": folha_id,
        "colaborador_id": 1,
        "mes": 12,
        "ano": 2024,
        "salario_base": 5000.00,
        "descontos": 1000.00,
        "salario_liquido": 4000.00
    }

# ============================================================================
# ENDPOINTS DE RECRUTAMENTO
# ============================================================================

@app.get("/recrutamentos", response_model=List[RecrutamentoResponse])
async def listar_recrutamentos(
    status: Optional[str] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None
):
    """Lista recrutamentos com filtros"""
    return []  # Placeholder

@app.post("/recrutamentos", response_model=RecrutamentoResponse, status_code=status.HTTP_201_CREATED)
async def criar_recrutamento(recrutamento: RecrutamentoCreate):
    """Cria um novo registro de recrutamento"""
    try:
        # Simulação de criação
        response_data = recrutamento.dict()
        response_data["id"] = 1
        return response_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar recrutamento: {str(e)}"
        )

# ============================================================================
# ENDPOINTS DE AVALIAÇÃO DE DESEMPENHO
# ============================================================================

@app.get("/avaliacoes", response_model=List[AvaliacaoDesempenhoResponse])
async def listar_avaliacoes(
    colaborador_id: Optional[int] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    nota_minima: Optional[int] = Query(None, ge=0, le=10)
):
    """Lista avaliações de desempenho com filtros"""
    return []  # Placeholder

@app.post("/avaliacoes", response_model=AvaliacaoDesempenhoResponse, status_code=status.HTTP_201_CREATED)
async def criar_avaliacao(avaliacao: AvaliacaoDesempenhoCreate):
    """Cria uma nova avaliação de desempenho"""
    try:
        # Simulação de criação
        response_data = avaliacao.dict()
        response_data["id"] = 1
        return response_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar avaliação: {str(e)}"
        )

# ============================================================================
# ENDPOINTS DE BENEFÍCIOS
# ============================================================================

@app.get("/beneficios", response_model=List[BeneficioResponse])
async def listar_beneficios():
    """Lista todos os benefícios disponíveis"""
    return []  # Placeholder

@app.post("/beneficios", response_model=BeneficioResponse, status_code=status.HTTP_201_CREATED)
async def criar_beneficio(beneficio: BeneficioCreate):
    """Cria um novo benefício"""
    try:
        # Simulação de criação
        response_data = beneficio.dict()
        response_data["id"] = 1
        return response_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar benefício: {str(e)}"
        )

# ============================================================================
# ENDPOINTS DE ASSOCIAÇÃO COLABORADOR-BENEFÍCIO
# ============================================================================

@app.post("/colaboradores/{colaborador_id}/beneficios", response_model=ColaboradorBeneficioResponse, status_code=status.HTTP_201_CREATED)
async def adicionar_beneficio_colaborador(
    colaborador_id: int,
    beneficio_colaborador: ColaboradorBeneficioCreate
):
    """Associa um benefício a um colaborador"""
    if beneficio_colaborador.colaborador_id != colaborador_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID do colaborador na URL não corresponde ao ID no corpo da requisição"
        )
    
    try:
        # Simulação de criação
        response_data = beneficio_colaborador.dict()
        response_data["id"] = 1
        return response_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao associar benefício: {str(e)}"
        )

@app.get("/colaboradores/{colaborador_id}/beneficios", response_model=List[BeneficioResponse])
async def listar_beneficios_colaborador(colaborador_id: int):
    """Lista todos os benefícios de um colaborador"""
    if colaborador_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colaborador não encontrado"
        )
    
    return [
        {
            "id": 1,
            "nome": "Vale Alimentação",
            "descricao": "Benefício para alimentação",
            "valor": 500.00
        }
    ]

# ============================================================================
# ENDPOINTS DE RELATÓRIOS E ESTATÍSTICAS
# ============================================================================

@app.get("/relatorios/colaboradores-por-funcao")
async def relatorio_colaboradores_por_funcao():
    """
    Relatório: Quantidade de colaboradores por função.
    """
    # Em um cenário real, você faria uma query GROUP BY
    return [
        {"funcao": "Desenvolvedor", "quantidade": 10},
        {"funcao": "Analista", "quantidade": 5},
        {"funcao": "Gerente", "quantidade": 3}
    ]

@app.get("/relatorios/folha-pagamento/{ano}/{mes}")
async def relatorio_folha_pagamento_mensal(ano: int, mes: int):
    """
    Relatório consolidado da folha de pagamento de um mês específico.
    """
    return {
        "ano": ano,
        "mes": mes,
        "total_funcionarios": 50,
        "total_salario_bruto": 250000.00,
        "total_descontos": 50000.00,
        "total_salario_liquido": 200000.00,
        "media_salario": 5000.00
    }

@app.get("/relatorios/avaliacoes-media")
async def relatorio_media_avaliacoes():
    """
    Relatório: Média de avaliações por colaborador.
    """
    return {
        "total_colaboradores_avaliados": 30,
        "media_geral": 8.5,
        "melhor_media": 9.8,
        "pior_media": 6.2
    }

# ============================================================================
# ENDPOINTS DE DASHBOARD
# ============================================================================

@app.get("/dashboard/resumo")
async def dashboard_resumo():
    """
    Retorna um resumo para o dashboard do RH.
    """
    return {
        "total_colaboradores": 150,
        "colaboradores_ativos": 140,
        "colaboradores_inativos": 10,
        "total_funcoes": 20,
        "folha_pagamento_mensal": 750000.00,
        "media_avaliacao": 8.2,
        "recrutamentos_ativos": 5,
        "novos_contratados_mes": 3
    }

# ============================================================================
# CONFIGURAÇÃO DE ERROS GLOBAIS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handler personalizado para exceções HTTP"""
    return {
        "detail": exc.detail,
        "status_code": exc.status_code
    }

# ============================================================================
# INICIALIZAÇÃO DO SERVIDOR
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )