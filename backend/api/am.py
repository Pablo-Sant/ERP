from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import List, Optional, Dict, Any, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, func, and_, or_
from datetime import datetime, date
from decimal import Decimal
import json
import os
from pathlib import Path

from core.database import get_db
from pydantic import BaseModel, Field, validator, ConfigDict, field_validator, model_validator
from typing import Optional

# ========== SCHEMAS ==========
class CategoriaResponse(BaseModel):
    id: int
    codigo: str
    nome: str
    descricao: Optional[str] = None
    metodo_depreciacao: Optional[str] = "linha_reta"
    vida_util_padrao_anos: Optional[int] = 5
    taxa_residual_padrao: Optional[float] = 0
    
    model_config = ConfigDict(from_attributes=True)

class LocalizacaoResponse(BaseModel):
    id: int
    codigo: str
    nome: str
    tipo_local: Optional[str] = None
    endereco: Optional[str] = None
    ativo: bool = True
    
    model_config = ConfigDict(from_attributes=True)

class FornecedorResponse(BaseModel):
    id: int
    codigo: str
    nome: str
    tipo_fornecedor: Optional[str] = None
    pessoa_contato: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    cnpj: Optional[str] = None
    ativo: bool = True
    
    model_config = ConfigDict(from_attributes=True)

# Schema para criação que aceita tanto os nomes novos quanto antigos
class AtivoCreate(BaseModel):
    # Campos do banco
    numero_tag: Optional[str] = Field(None, min_length=1, max_length=100)
    nome: Optional[str] = Field(None, min_length=1, max_length=255)
    id_categoria: Optional[int] = None
    id_localizacao: Optional[int] = None
    id_organizacao: int = 1
    
    # Campos antigos para compatibilidade
    tag: Optional[str] = Field(None, min_length=1, max_length=100)
    categoria_nome: Optional[str] = None
    localizacao_nome: Optional[str] = None
    data_aquisicao: Optional[date] = None
    valor: Optional[Union[Decimal, float, str]] = None
    status: Optional[str] = "ativo"
    criticidade: Optional[str] = "medio"
    
    # Outros campos do banco
    id_ativo_pai: Optional[int] = None
    id_fornecedor: Optional[int] = None
    numero_serie: Optional[str] = None
    modelo: Optional[str] = None
    fabricante: Optional[str] = None
    descricao: Optional[str] = None
    status_ativo: Optional[str] = "ativo"
    custo_aquisicao: Optional[Union[Decimal, float]] = 0
    numero_ordem_compra: Optional[str] = None
    data_vencimento_garantia: Optional[date] = None
    vida_util_anos: Optional[int] = None
    valor_residual: Optional[Union[Decimal, float]] = 0
    valor_atual: Optional[Union[Decimal, float]] = None
    especificacoes: Optional[Dict[str, Any]] = None
    parametros_tecnicos: Optional[Dict[str, Any]] = None
    observacoes: Optional[str] = None

    @field_validator('status', 'status_ativo', mode='before')
    @classmethod
    def validate_status(cls, v):
        if v is None:
            return v
        valid_status = ['planejado', 'ativo', 'inativo', 'em_manutencao', 'baixado', 'descartado', 'perdido']
        if v not in valid_status:
            raise ValueError(f'Status deve ser um dos: {", ".join(valid_status)}')
        return v

    @field_validator('criticidade', mode='before')
    @classmethod
    def validate_criticidade(cls, v):
        if v is None:
            return v
        valid_criticidades = ['baixa', 'medio', 'alta', 'critico']
        if v not in valid_criticidades:
            raise ValueError(f'Criticidade deve ser um dos: {", ".join(valid_criticidades)}')
        return v

    @field_validator('valor', mode='before')
    @classmethod
    def parse_valor(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            # Remover R$ e converter
            v = v.replace('R$', '').replace('.', '').replace(',', '.').strip()
        try:
            return Decimal(v)
        except:
            return Decimal(0)

    @model_validator(mode='after')
    def normalize_fields(self):
        """Normaliza os campos para o formato do banco"""
        data = self.model_dump(exclude_unset=True)
        
        # Mapear campos antigos para novos
        if 'tag' in data and 'numero_tag' not in data:
            self.numero_tag = data['tag']
        if 'categoria_nome' in data and 'id_categoria' not in data:
            # Aqui precisaríamos buscar o ID da categoria pelo nome
            # Por enquanto, vamos usar um valor padrão
            self.id_categoria = 1
        if 'localizacao_nome' in data and 'id_localizacao' not in data:
            self.id_localizacao = 1
        if 'status' in data and 'status_ativo' not in data:
            self.status_ativo = data['status']
        if 'valor' in data:
            if 'custo_aquisicao' not in data:
                self.custo_aquisicao = data['valor']
            if 'valor_atual' not in data:
                self.valor_atual = data['valor']
        
        return self

class AtivoUpdate(BaseModel):
    numero_tag: Optional[str] = Field(None, min_length=1, max_length=100)
    nome: Optional[str] = Field(None, min_length=1, max_length=255)
    id_categoria: Optional[int] = None
    id_localizacao: Optional[int] = None
    id_ativo_pai: Optional[int] = None
    id_fornecedor: Optional[int] = None
    numero_serie: Optional[str] = None
    modelo: Optional[str] = None
    fabricante: Optional[str] = None
    descricao: Optional[str] = None
    status_ativo: Optional[str] = None
    criticidade: Optional[str] = None
    data_aquisicao: Optional[date] = None
    custo_aquisicao: Optional[Union[Decimal, float]] = None
    numero_ordem_compra: Optional[str] = None
    data_vencimento_garantia: Optional[date] = None
    vida_util_anos: Optional[int] = None
    valor_residual: Optional[Union[Decimal, float]] = None
    valor_atual: Optional[Union[Decimal, float]] = None
    especificacoes: Optional[Dict[str, Any]] = None
    parametros_tecnicos: Optional[Dict[str, Any]] = None
    observacoes: Optional[str] = None

class AtivoResponse(BaseModel):
    id: int
    uuid: Optional[str] = None
    numero_tag: str
    nome: str
    id_categoria: int
    id_localizacao: int
    id_organizacao: int
    id_ativo_pai: Optional[int] = None
    id_fornecedor: Optional[int] = None
    numero_serie: Optional[str] = None
    modelo: Optional[str] = None
    fabricante: Optional[str] = None
    descricao: Optional[str] = None
    status_ativo: str
    criticidade: str
    data_aquisicao: Optional[date] = None
    custo_aquisicao: Optional[Decimal] = None
    numero_ordem_compra: Optional[str] = None
    data_vencimento_garantia: Optional[date] = None
    vida_util_anos: Optional[int] = None
    valor_residual: Optional[Decimal] = None
    valor_atual: Optional[Decimal] = None
    depreciacao_acumulada: Optional[Decimal] = None
    especificacoes: Optional[Dict[str, Any]] = None
    parametros_tecnicos: Optional[Dict[str, Any]] = None
    data_ativacao: Optional[date] = None
    data_desativacao: Optional[date] = None
    observacoes: Optional[str] = None
    data_criacao: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None
    
    # Campos derivados (vindos de joins)
    categoria_nome: Optional[str] = None
    localizacao_nome: Optional[str] = None
    fornecedor_nome: Optional[str] = None
    
    # Campos de compatibilidade
    tag: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    purchaseDate: Optional[str] = None
    value: Optional[str] = None
    
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            Decimal: lambda v: float(v) if v is not None else None,
            date: lambda v: v.isoformat() if v else None,
            datetime: lambda v: v.isoformat() if v else None
        }
    )
    
    @field_validator('tag', mode='after')
    @classmethod
    def set_tag(cls, v, info):
        if info.data.get('numero_tag'):
            return info.data['numero_tag']
        return v
    
    @field_validator('category', mode='after')
    @classmethod
    def set_category(cls, v, info):
        if info.data.get('categoria_nome'):
            return info.data['categoria_nome']
        return v
    
    @field_validator('location', mode='after')
    @classmethod
    def set_location(cls, v, info):
        if info.data.get('localizacao_nome'):
            return info.data['localizacao_nome']
        return v
    
    @field_validator('purchaseDate', mode='after')
    @classmethod
    def set_purchase_date(cls, v, info):
        if info.data.get('data_aquisicao'):
            return info.data['data_aquisicao'].isoformat()
        return v
    
    @field_validator('value', mode='after')
    @classmethod
    def set_value(cls, v, info):
        valor = info.data.get('valor_atual') or info.data.get('custo_aquisicao')
        if valor:
            return f"R$ {float(valor):,.2f}"
        return v

class DashboardResponse(BaseModel):
    total_ativos: int
    valor_total: float
    total_categorias: int
    ativos_por_status: List[Dict[str, Any]]
    ativos_por_categoria: List[Dict[str, Any]]
    ativos_por_criticidade: List[Dict[str, Any]]
    data_atualizacao: str

router = APIRouter()

# ========== CRUD ATIVOS ==========
@router.post("/", response_model=AtivoResponse, status_code=201)
async def criar_ativo(ativo: AtivoCreate, db: AsyncSession = Depends(get_db)):
    """Cria um novo ativo"""
    try:
        # Normalizar campos (suporte a campos antigos)
        data = ativo.model_dump(exclude_unset=True)
        
        # Validar campos obrigatórios
        if not data.get('numero_tag'):
            raise HTTPException(status_code=400, detail="Campo 'numero_tag' é obrigatório")
        if not data.get('nome'):
            raise HTTPException(status_code=400, detail="Campo 'nome' é obrigatório")
        if not data.get('id_categoria'):
            raise HTTPException(status_code=400, detail="Campo 'id_categoria' é obrigatório")
        if not data.get('id_localizacao'):
            raise HTTPException(status_code=400, detail="Campo 'id_localizacao' é obrigatório")
        
        # Verificar se tag já existe
        query_check = """
        SELECT COUNT(*) FROM am.ativos 
        WHERE numero_tag = :numero_tag AND id_organizacao = :id_organizacao
        """
        result = await db.execute(
            text(query_check), 
            {"numero_tag": data['numero_tag'], "id_organizacao": data.get('id_organizacao', 1)}
        )
        count = result.scalar()
        
        if count > 0:
            raise HTTPException(
                status_code=400, 
                detail=f"Tag {data['numero_tag']} já existe para esta organização"
            )
        
        # Inserir ativo - CORRIGIDO: usar valores padrão para parâmetros não fornecidos
        query_insert = """
        INSERT INTO am.ativos (
            id_organizacao, id_categoria, id_localizacao, id_ativo_pai, id_fornecedor,
            numero_tag, numero_serie, modelo, fabricante, nome, descricao,
            status_ativo, criticidade, data_aquisicao, custo_aquisicao,
            numero_ordem_compra, data_vencimento_garantia, vida_util_anos,
            valor_residual, valor_atual, especificacoes, parametros_tecnicos, observacoes,
            criado_por, data_ativacao
        ) VALUES (
            COALESCE(:id_organizacao, 1), 
            :id_categoria, 
            :id_localizacao, 
            :id_ativo_pai, 
            :id_fornecedor,
            :numero_tag, 
            :numero_serie, 
            :modelo, 
            :fabricante, 
            :nome, 
            :descricao,
            COALESCE(:status_ativo, 'ativo'), 
            COALESCE(:criticidade, 'medio'), 
            :data_aquisicao, 
            COALESCE(:custo_aquisicao, 0),
            :numero_ordem_compra, 
            :data_vencimento_garantia, 
            :vida_util_anos,
            COALESCE(:valor_residual, 0), 
            COALESCE(:valor_atual, COALESCE(:custo_aquisicao, 0)), 
            :especificacoes, 
            :parametros_tecnicos, 
            :observacoes,
            COALESCE(:criado_por, 1), 
            CASE WHEN COALESCE(:status_ativo, 'ativo') = 'ativo' THEN CURRENT_DATE ELSE NULL END
        ) RETURNING *
        """
        
        # Preparar parâmetros com valores padrão
        params = {
            'id_organizacao': data.get('id_organizacao', 1),
            'id_categoria': data.get('id_categoria'),
            'id_localizacao': data.get('id_localizacao'),
            'id_ativo_pai': data.get('id_ativo_pai'),
            'id_fornecedor': data.get('id_fornecedor'),
            'numero_tag': data.get('numero_tag'),
            'numero_serie': data.get('numero_serie'),
            'modelo': data.get('modelo'),
            'fabricante': data.get('fabricante'),
            'nome': data.get('nome'),
            'descricao': data.get('descricao'),
            'status_ativo': data.get('status_ativo', 'ativo'),
            'criticidade': data.get('criticidade', 'medio'),
            'data_aquisicao': data.get('data_aquisicao'),
            'custo_aquisicao': data.get('custo_aquisicao', 0),
            'numero_ordem_compra': data.get('numero_ordem_compra'),
            'data_vencimento_garantia': data.get('data_vencimento_garantia'),
            'vida_util_anos': data.get('vida_util_anos'),
            'valor_residual': data.get('valor_residual', 0),
            'valor_atual': data.get('valor_atual', data.get('custo_aquisicao', 0)),
            'especificacoes': None,
            'parametros_tecnicos': None,
            'observacoes': data.get('observacoes'),
            'criado_por': 1
        }
        
        # Converter valores para Decimal
        decimal_fields = ['custo_aquisicao', 'valor_atual', 'valor_residual']
        for field in decimal_fields:
            if params[field] is not None:
                if isinstance(params[field], str):
                    params[field] = Decimal(params[field].replace('R$', '').replace('.', '').replace(',', '.').strip())
                elif isinstance(params[field], float):
                    params[field] = Decimal(str(params[field]))
        
        # Converter dicionários para JSON
        if data.get('especificacoes'):
            params['especificacoes'] = json.dumps(data['especificacoes'])
        if data.get('parametros_tecnicos'):
            params['parametros_tecnicos'] = json.dumps(data['parametros_tecnicos'])
        
        # Remover None values para não causar problemas com COALESCE
        for key in list(params.keys()):
            if params[key] is None and key not in ['especificacoes', 'parametros_tecnicos']:
                params[key] = None  # Mantém como None, COALESCE tratará
        
        print(f"DEBUG: Parâmetros para INSERT: {params}")  # Debug
        
        result = await db.execute(text(query_insert), params)
        row = result.fetchone()
        
        # Buscar ativo completo com joins
        ativo_completo = await _get_ativo_completo(db, row.id)
        
        await db.commit()
        return ativo_completo
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        print(f"Erro detalhado ao criar ativo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar ativo: {str(e)}")
    
@router.get("/", response_model=List[AtivoResponse])
async def listar_ativos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Lista todos os ativos com paginação"""
    try:
        query = """
        SELECT 
            a.*,
            ca.nome as categoria_nome,
            l.nome as localizacao_nome,
            f.nome as fornecedor_nome
        FROM am.ativos a
        LEFT JOIN am.categorias_ativos ca ON a.id_categoria = ca.id
        LEFT JOIN am.localizacoes l ON a.id_localizacao = l.id
        LEFT JOIN am.fornecedores f ON a.id_fornecedor = f.id
        WHERE a.id_organizacao = 1
        ORDER BY a.data_criacao DESC
        LIMIT :limit OFFSET :skip
        """
        
        result = await db.execute(text(query), {"skip": skip, "limit": limit})
        rows = result.fetchall()
        
        ativos = []
        for row in rows:
            ativo = _process_ativo_row(dict(row._mapping))
            ativos.append(ativo)
        
        return ativos
        
    except Exception as e:
        print(f"Erro ao listar ativos: {str(e)}")  # Debug
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

async def _get_ativo_completo(db: AsyncSession, ativo_id: int) -> Dict[str, Any]:
    """Busca um ativo completo com joins"""
    query = """
    SELECT 
        a.*,
        ca.nome as categoria_nome,
        l.nome as localizacao_nome,
        f.nome as fornecedor_nome
    FROM am.ativos a
    LEFT JOIN am.categorias_ativos ca ON a.id_categoria = ca.id
    LEFT JOIN am.localizacoes l ON a.id_localizacao = l.id
    LEFT JOIN am.fornecedores f ON a.id_fornecedor = f.id
    WHERE a.id = :ativo_id
    """
    
    result = await db.execute(text(query), {"ativo_id": ativo_id})
    row = result.fetchone()
    
    if not row:
        return None
    
    ativo = dict(row._mapping)
    return _process_ativo_row(ativo)

def _process_ativo_row(ativo: Dict[str, Any]) -> Dict[str, Any]:
    """Processa uma linha de ativo do banco de forma segura"""
    try:
        result = {}
        
        # Copiar todos os campos básicos
        for key, value in ativo.items():
            if value is None:
                result[key] = None
            elif isinstance(value, (str, int, float, bool)):
                result[key] = value
            elif isinstance(value, Decimal):
                result[key] = float(value)
            elif hasattr(value, 'isoformat'):  # Para datetime/date
                if hasattr(value, 'date') and not hasattr(value, 'hour'):  # É date
                    result[key] = value.isoformat()
                else:  # É datetime
                    result[key] = value.isoformat()
            else:
                result[key] = str(value)
        
        # Processar campos JSONB
        if 'especificacoes' in result and result['especificacoes']:
            try:
                if isinstance(result['especificacoes'], str):
                    result['especificacoes'] = json.loads(result['especificacoes'])
            except:
                result['especificacoes'] = None
        
        if 'parametros_tecnicos' in result and result['parametros_tecnicos']:
            try:
                if isinstance(result['parametros_tecnicos'], str):
                    result['parametros_tecnicos'] = json.loads(result['parametros_tecnicos'])
            except:
                result['parametros_tecnicos'] = None
        
        # Garantir campos obrigatórios
        result.setdefault('status_ativo', 'ativo')
        result.setdefault('criticidade', 'medio')
        result.setdefault('id_organizacao', 1)
        
        # Campos de compatibilidade
        result['tag'] = result.get('numero_tag', '')
        result['category'] = result.get('categoria_nome', '')
        result['location'] = result.get('localizacao_nome', '')
        
        if result.get('data_aquisicao'):
            result['purchaseDate'] = result['data_aquisicao']
        
        valor = result.get('valor_atual') or result.get('custo_aquisicao')
        if valor:
            result['value'] = f"R$ {float(valor):,.2f}"
        else:
            result['value'] = "R$ 0,00"
        
        return result
    except Exception as e:
        print(f"Erro ao processar linha de ativo: {str(e)}")
        print(f"Dados originais: {ativo}")
        # Retornar dados mínimos
        return {
            'id': ativo.get('id', 0),
            'numero_tag': ativo.get('numero_tag', ''),
            'nome': ativo.get('nome', ''),
            'id_categoria': ativo.get('id_categoria', 0),
            'id_localizacao': ativo.get('id_localizacao', 0),
            'status_ativo': ativo.get('status_ativo', 'ativo'),
            'criticidade': ativo.get('criticidade', 'medio'),
            'categoria_nome': ativo.get('categoria_nome', ''),
            'localizacao_nome': ativo.get('localizacao_nome', ''),
            'tag': ativo.get('numero_tag', ''),
            'category': ativo.get('categoria_nome', ''),
            'location': ativo.get('localizacao_nome', ''),
            'value': 'R$ 0,00'
        }

@router.get("/buscar", response_model=List[AtivoResponse])
async def buscar_ativos(
    categoria: Optional[str] = None,
    localizacao: Optional[str] = None,
    status: Optional[str] = None,
    criticidade: Optional[str] = None,
    nome: Optional[str] = None,
    tag: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Busca ativos com filtros"""
    try:
        query = """
        SELECT 
            a.*,
            ca.nome as categoria_nome,
            l.nome as localizacao_nome,
            f.nome as fornecedor_nome
        FROM am.ativos a
        LEFT JOIN am.categorias_ativos ca ON a.id_categoria = ca.id
        LEFT JOIN am.localizacoes l ON a.id_localizacao = l.id
        LEFT JOIN am.fornecedores f ON a.id_fornecedor = f.id
        WHERE a.id_organizacao = 1
        """
        
        params = {}
        conditions = []
        
        if categoria:
            conditions.append("ca.nome ILIKE :categoria")
            params["categoria"] = f"%{categoria}%"
        
        if localizacao:
            conditions.append("l.nome ILIKE :localizacao")
            params["localizacao"] = f"%{localizacao}%"
        
        if status:
            conditions.append("a.status_ativo = :status")
            params["status"] = status
        
        if criticidade:
            conditions.append("a.criticidade = :criticidade")
            params["criticidade"] = criticidade
        
        if nome:
            conditions.append("a.nome ILIKE :nome")
            params["nome"] = f"%{nome}%"
        
        if tag:
            conditions.append("a.numero_tag ILIKE :tag")
            params["tag"] = f"%{tag}%"
        
        if conditions:
            query += " AND " + " AND ".join(conditions)
        
        query += " ORDER BY a.data_criacao DESC"
        
        result = await db.execute(text(query), params)
        rows = result.fetchall()
        
        ativos = []
        for row in rows:
            ativo = dict(row._mapping)
            ativos.append(_process_ativo_row(ativo))
        
        return ativos
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/{ativo_id}", response_model=AtivoResponse)
async def obter_ativo(ativo_id: int, db: AsyncSession = Depends(get_db)):
    """Obtém um ativo específico pelo ID"""
    try:
        ativo = await _get_ativo_completo(db, ativo_id)
        
        if not ativo:
            raise HTTPException(status_code=404, detail="Ativo não encontrado")
        
        return ativo
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao obter ativo {ativo_id}: {str(e)}")  # Debug
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.put("/{ativo_id}", response_model=AtivoResponse)
async def atualizar_ativo(
    ativo_id: int,
    ativo_update: AtivoUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Atualiza um ativo existente"""
    try:
        # Verificar se ativo existe
        ativo_existente = await _get_ativo_completo(db, ativo_id)
        if not ativo_existente:
            raise HTTPException(status_code=404, detail="Ativo não encontrado")
        
        # Preparar campos para atualização
        update_data = ativo_update.model_dump(exclude_unset=True)
        
        if not update_data:
            return ativo_existente
        
        # Construir query dinâmica
        set_clauses = []
        params = {"ativo_id": ativo_id}
        
        for field, value in update_data.items():
            if field == 'especificacoes' and value is not None:
                set_clauses.append("especificacoes = :especificacoes")
                params["especificacoes"] = json.dumps(value)
            elif field == 'parametros_tecnicos' and value is not None:
                set_clauses.append("parametros_tecnicos = :parametros_tecnicos")
                params["parametros_tecnicos"] = json.dumps(value)
            elif value is not None:
                set_clauses.append(f"{field} = :{field}")
                params[field] = value
        
        # Adicionar data_atualizacao
        set_clauses.append("data_atualizacao = CURRENT_TIMESTAMP")
        
        # Atualizar data_ativacao se status mudar para 'ativo'
        if 'status_ativo' in update_data and update_data['status_ativo'] == 'ativo':
            set_clauses.append("data_ativacao = COALESCE(data_ativacao, CURRENT_DATE)")
        
        # Atualizar data_desativacao se status mudar para inativo/baixado
        if 'status_ativo' in update_data and update_data['status_ativo'] in ['inativo', 'baixado', 'descartado']:
            set_clauses.append("data_desativacao = CURRENT_DATE")
        
        query = f"""
        UPDATE am.ativos
        SET {', '.join(set_clauses)}
        WHERE id = :ativo_id
        """
        
        await db.execute(text(query), params)
        
        # Buscar ativo atualizado
        ativo_atualizado = await _get_ativo_completo(db, ativo_id)
        
        await db.commit()
        return ativo_atualizado
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/{ativo_id}", status_code=204)
async def excluir_ativo(ativo_id: int, db: AsyncSession = Depends(get_db)):
    """Exclui um ativo"""
    try:
        # Verificar se ativo existe
        query_check = "SELECT id FROM am.ativos WHERE id = :ativo_id"
        result = await db.execute(text(query_check), {"ativo_id": ativo_id})
        if not result.fetchone():
            raise HTTPException(status_code=404, detail="Ativo não encontrado")
        
        # Excluir ativo
        query_delete = "DELETE FROM am.ativos WHERE id = :ativo_id"
        await db.execute(text(query_delete), {"ativo_id": ativo_id})
        
        await db.commit()
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# ========== DASHBOARD ==========
@router.get("/dashboard/resumo", response_model=DashboardResponse)
async def dashboard_resumo(db: AsyncSession = Depends(get_db)):
    """Retorna resumo para dashboard de ativos"""
    try:
        # Total de ativos
        query_total = """
        SELECT COUNT(*) as total, 
               COALESCE(SUM(COALESCE(valor_atual, custo_aquisicao, 0)), 0) as valor_total
        FROM am.ativos 
        WHERE id_organizacao = 1
        """
        result = await db.execute(text(query_total))
        row = result.fetchone()
        total_ativos = row.total or 0
        valor_total = float(row.valor_total or 0)
        
        # Total de categorias distintas
        query_categorias = """
        SELECT COUNT(DISTINCT id_categoria) as total
        FROM am.ativos 
        WHERE id_organizacao = 1
        """
        result = await db.execute(text(query_categorias))
        total_categorias = result.scalar() or 0
        
        # Ativos por status
        query_status = """
        SELECT 
            COALESCE(status_ativo, 'ativo') as status,
            COUNT(*) as quantidade,
            COALESCE(SUM(COALESCE(valor_atual, custo_aquisicao, 0)), 0) as valor_total
        FROM am.ativos 
        WHERE id_organizacao = 1
        GROUP BY status_ativo
        ORDER BY quantidade DESC
        """
        result = await db.execute(text(query_status))
        rows = result.fetchall()
        
        ativos_por_status = []
        for row in rows:
            ativos_por_status.append({
                "status": row.status,
                "quantidade": row.quantidade,
                "valor_total": float(row.valor_total or 0)
            })
        
        # Ativos por categoria
        query_categoria = """
        SELECT 
            COALESCE(ca.nome, 'Sem categoria') as categoria,
            COUNT(a.id) as quantidade,
            COALESCE(SUM(COALESCE(a.valor_atual, a.custo_aquisicao, 0)), 0) as valor_total
        FROM am.ativos a
        LEFT JOIN am.categorias_ativos ca ON a.id_categoria = ca.id
        WHERE a.id_organizacao = 1
        GROUP BY ca.nome
        ORDER BY valor_total DESC
        LIMIT 10
        """
        result = await db.execute(text(query_categoria))
        rows = result.fetchall()
        
        ativos_por_categoria = []
        for row in rows:
            ativos_por_categoria.append({
                "categoria": row.categoria,
                "quantidade": row.quantidade,
                "valor_total": float(row.valor_total or 0)
            })
        
        # Ativos por criticidade
        query_criticidade = """
        SELECT 
            COALESCE(criticidade, 'medio') as criticidade,
            COUNT(*) as quantidade,
            COALESCE(SUM(COALESCE(valor_atual, custo_aquisicao, 0)), 0) as valor_total
        FROM am.ativos 
        WHERE id_organizacao = 1
        GROUP BY criticidade
        ORDER BY 
            CASE COALESCE(criticidade, 'medio')
                WHEN 'critico' THEN 1
                WHEN 'alta' THEN 2
                WHEN 'medio' THEN 3
                WHEN 'baixa' THEN 4
                ELSE 5
            END
        """
        result = await db.execute(text(query_criticidade))
        rows = result.fetchall()
        
        ativos_por_criticidade = []
        for row in rows:
            ativos_por_criticidade.append({
                "criticidade": row.criticidade,
                "quantidade": row.quantidade,
                "valor_total": float(row.valor_total or 0)
            })
        
        return {
            "total_ativos": total_ativos,
            "valor_total": valor_total,
            "total_categorias": total_categorias,
            "ativos_por_status": ativos_por_status,
            "ativos_por_categoria": ativos_por_categoria,
            "ativos_por_criticidade": ativos_por_criticidade,
            "data_atualizacao": datetime.now().isoformat()
        }
        
    except Exception as e:
        # Fallback para dados mockados se o banco falhar
        print(f"Aviso: Erro ao consultar dashboard, usando dados mockados: {str(e)}")
        return {
            "total_ativos": 0,
            "valor_total": 0.0,
            "total_categorias": 0,
            "ativos_por_status": [],
            "ativos_por_categoria": [],
            "ativos_por_criticidade": [],
            "data_atualizacao": datetime.now().isoformat()
        }

# ========== ENDPOINTS AUXILIARES ==========
@router.get("/categorias/listar", response_model=List[CategoriaResponse])
async def listar_categorias(db: AsyncSession = Depends(get_db)):
    """Lista todas as categorias"""
    try:
        query = """
        SELECT id, codigo, nome, descricao, 
               metodo_depreciacao, vida_util_padrao_anos, taxa_residual_padrao
        FROM am.categorias_ativos 
        WHERE id_organizacao = 1
        ORDER BY nome
        """
        result = await db.execute(text(query))
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]
    except Exception as e:
        # Mock data se a tabela não existir
        print(f"Aviso: Erro ao buscar categorias, retornando dados mockados: {str(e)}")
        return [
            {"id": 1, "codigo": "TI", "nome": "TI", "descricao": "Equipamentos de TI"},
            {"id": 2, "codigo": "FROTA", "nome": "Frota", "descricao": "Veículos"},
            {"id": 3, "codigo": "MOB", "nome": "Mobília", "descricao": "Móveis e utensílios"}
        ]

@router.get("/localizacoes/listar", response_model=List[LocalizacaoResponse])
async def listar_localizacoes(db: AsyncSession = Depends(get_db)):
    """Lista todas as localizações"""
    try:
        query = """
        SELECT id, codigo, nome, tipo_local, endereco, ativo
        FROM am.localizacoes 
        WHERE id_organizacao = 1
        ORDER BY nome
        """
        result = await db.execute(text(query))
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]
    except Exception as e:
        # Mock data se a tabela não existir
        print(f"Aviso: Erro ao buscar localizações, retornando dados mockados: {str(e)}")
        return [
            {"id": 1, "codigo": "SERV", "nome": "Sala Servidores", "tipo_local": "sala_tec", "ativo": True},
            {"id": 2, "codigo": "GAR", "nome": "Garagem", "tipo_local": "garagem", "ativo": True},
            {"id": 3, "codigo": "DIR", "nome": "Sala Diretoria", "tipo_local": "escritorio", "ativo": True}
        ]

@router.get("/fornecedores/listar", response_model=List[FornecedorResponse])
async def listar_fornecedores(db: AsyncSession = Depends(get_db)):
    """Lista todos os fornecedores"""
    try:
        query = """
        SELECT id, codigo, nome, tipo_fornecedor, 
               pessoa_contato, telefone, email, cnpj, ativo
        FROM am.fornecedores 
        WHERE id_organizacao = 1 AND ativo = true
        ORDER BY nome
        """
        result = await db.execute(text(query))
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]
    except Exception as e:
        # Mock data se a tabela não existir
        print(f"Aviso: Erro ao buscar fornecedores, retornando dados mockados: {str(e)}")
        return []

# ========== HEALTH CHECK ==========
@router.get("/teste/banco")
async def teste_conexao_banco(db: AsyncSession = Depends(get_db)):
    """Testa a conexão com o banco de dados"""
    try:
        # Testar conexão com tabelas principais
        tabelas = {
            'ativos': "SELECT COUNT(*) FROM am.ativos WHERE id_organizacao = 1",
            'categorias_ativos': "SELECT COUNT(*) FROM am.categorias_ativos WHERE id_organizacao = 1",
            'localizacoes': "SELECT COUNT(*) FROM am.localizacoes WHERE id_organizacao = 1",
            'fornecedores': "SELECT COUNT(*) FROM am.fornecedores WHERE id_organizacao = 1"
        }
        
        estatisticas = {}
        for nome, query in tabelas.items():
            try:
                result = await db.execute(text(query))
                estatisticas[nome] = result.scalar() or 0
            except Exception as e:
                estatisticas[nome] = f'erro: {str(e)[:50]}'
        
        return {
            "status": "conexao_ok",
            "mensagem": "Conexão com banco de dados estabelecida",
            "timestamp": datetime.now().isoformat(),
            "estatisticas": estatisticas
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro na conexão com banco de dados: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Health check simples"""
    return {
        "status": "healthy",
        "module": "asset_management",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# ========== RELATÓRIOS ==========
@router.get("/relatorios/ativos-vencimento-garantia")
async def relatorio_ativos_vencimento_garantia(
    dias: int = Query(90, ge=1, le=365),
    db: AsyncSession = Depends(get_db)
):
    """Relatório de ativos com vencimento de garantia próximo"""
    try:
        query = """
        SELECT 
            a.id,
            a.numero_tag,
            a.nome,
            a.data_vencimento_garantia,
            a.id_fornecedor,
            f.nome as fornecedor_nome,
            ca.nome as categoria_nome,
            EXTRACT(DAY FROM (a.data_vencimento_garantia - CURRENT_DATE)) as dias_para_vencer
        FROM am.ativos a
        LEFT JOIN am.fornecedores f ON a.id_fornecedor = f.id
        LEFT JOIN am.categorias_ativos ca ON a.id_categoria = ca.id
        WHERE a.id_organizacao = 1
          AND a.data_vencimento_garantia IS NOT NULL
          AND a.data_vencimento_garantia >= CURRENT_DATE
          AND a.data_vencimento_garantia <= CURRENT_DATE + INTERVAL ':dias days'
        ORDER BY a.data_vencimento_garantia
        """
        
        result = await db.execute(text(query), {"dias": dias})
        rows = result.fetchall()
        
        ativos = []
        for row in rows:
            ativo = dict(row._mapping)
            if ativo.get('data_vencimento_garantia'):
                ativo['data_vencimento_garantia'] = ativo['data_vencimento_garantia'].date().isoformat() if hasattr(ativo['data_vencimento_garantia'], 'date') else str(ativo['data_vencimento_garantia'])
            ativos.append(ativo)
        
        return {
            "dias_para_vencimento": dias,
            "total_ativos": len(ativos),
            "ativos": ativos,
            "data_geracao": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")