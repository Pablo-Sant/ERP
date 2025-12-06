# bi_api.py
from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json
import hashlib

from core.database import get_db
from models.bi_dashboard_model import Dashboard
from models.bi_metrica_kpi_model import MetricaKPI
from models.bi_cache_dados_model import CacheDadosBI

from schemas.bi_dashboard_schema import (
    DashboardBase, DashboardCreate, DashboardRead
)
from schemas.bi_metrica_kpi_schema import (
    MetricaKPIBase, MetricaKPICreate, MetricaKPIRead
)
from schemas.bi_cache_dados_schema import (
    CacheDadosBIBase, CacheDadosBICreate, CacheDadosBIRead
)
from schemas.bi_relatorio import (
    RelatorioBase, RelatorioCreate, RelatorioRead
)

router = APIRouter(prefix="/bi", tags=["Business Intelligence"])

# ========== DASHBOARDS ==========
@router.post("/dashboards/", response_model=DashboardRead, status_code=status.HTTP_201_CREATED)
def criar_dashboard(dashboard: DashboardCreate, db: Session = Depends(get_db)):
    """Cria um novo dashboard"""
    db_dashboard = Dashboard(
        nome=dashboard.nome,
        descricao=dashboard.descricao,
        config_json=dashboard.config_json,
        data_atualizacao=datetime.utcnow()
    )
    db.add(db_dashboard)
    db.commit()
    db.refresh(db_dashboard)
    return db_dashboard

@router.get("/dashboards/", response_model=List[DashboardRead])
def listar_dashboards(
    skip: int = 0,
    limit: int = 100,
    nome: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lista todos os dashboards"""
    query = db.query(Dashboard)
    
    if nome:
        query = query.filter(Dashboard.nome.ilike(f"%{nome}%"))
    
    dashboards = query.order_by(Dashboard.data_atualizacao.desc()).offset(skip).limit(limit).all()
    return dashboards

@router.get("/dashboards/{dashboard_id}", response_model=DashboardRead)
def obter_dashboard(dashboard_id: int, db: Session = Depends(get_db)):
    """Obtém um dashboard pelo ID"""
    dashboard = db.query(Dashboard).filter(Dashboard.id_dashboard == dashboard_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard não encontrado")
    return dashboard

@router.put("/dashboards/{dashboard_id}", response_model=DashboardRead)
def atualizar_dashboard(
    dashboard_id: int,
    dashboard_data: DashboardBase,
    db: Session = Depends(get_db)
):
    """Atualiza um dashboard"""
    dashboard = db.query(Dashboard).filter(Dashboard.id_dashboard == dashboard_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard não encontrado")
    
    for key, value in dashboard_data.dict(exclude_unset=True).items():
        if key == "config_json" and value is not None:
            # Atualizar data_atualizacao quando config_json é alterado
            dashboard.data_atualizacao = datetime.utcnow()
        setattr(dashboard, key, value)
    
    db.commit()
    db.refresh(dashboard)
    return dashboard

@router.delete("/dashboards/{dashboard_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_dashboard(dashboard_id: int, db: Session = Depends(get_db)):
    """Deleta um dashboard"""
    dashboard = db.query(Dashboard).filter(Dashboard.id_dashboard == dashboard_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard não encontrado")
    
    db.delete(dashboard)
    db.commit()
    return None

@router.get("/dashboards/{dashboard_id}/dados")
def obter_dados_dashboard(
    dashboard_id: int,
    atualizar_cache: bool = False,
    db: Session = Depends(get_db)
):
    """Obtém os dados de um dashboard (com cache)"""
    dashboard = db.query(Dashboard).filter(Dashboard.id_dashboard == dashboard_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard não encontrado")
    
    # Gerar chave de cache para este dashboard
    chave_cache = f"dashboard_{dashboard_id}_{dashboard.data_atualizacao.timestamp()}"
    
    if not atualizar_cache:
        # Tentar obter do cache primeiro
        cache = db.query(CacheDadosBI).filter(
            CacheDadosBI.chave_cache == chave_cache,
            CacheDadosBI.data_expiracao > datetime.now()
        ).first()
        
        if cache:
            return {
                "dashboard": dashboard,
                "dados": cache.dados_json,
                "fonte": "cache",
                "data_geracao": cache.data_geracao
            }
    
    # Se não tem cache ou atualizar_cache=True, gerar dados
    dados = gerar_dados_dashboard(dashboard, db)
    
    # Salvar no cache
    cache_novo = CacheDadosBI(
        chave_cache=chave_cache,
        dados_json=dados,
        data_geracao=datetime.now(),
        data_expiracao=datetime.now() + timedelta(hours=1)  # Expira em 1 hora
    )
    db.add(cache_novo)
    db.commit()
    
    return {
        "dashboard": dashboard,
        "dados": dados,
        "fonte": "banco_dados",
        "data_geracao": datetime.now()
    }

# ========== MÉTRICAS/KPIs ==========
@router.post("/metricas/", response_model=MetricaKPIRead, status_code=status.HTTP_201_CREATED)
def criar_metrica(metrica: MetricaKPICreate, db: Session = Depends(get_db)):
    """Cria uma nova métrica/KPI"""
    db_metrica = MetricaKPI(**metrica.dict())
    db.add(db_metrica)
    db.commit()
    db.refresh(db_metrica)
    return db_metrica

@router.get("/metricas/", response_model=List[MetricaKPIRead])
def listar_metricas(
    skip: int = 0,
    limit: int = 100,
    categoria: Optional[str] = None,
    nome: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lista todas as métricas/KPIs"""
    query = db.query(MetricaKPI)
    
    if categoria:
        query = query.filter(MetricaKPI.categoria == categoria)
    if nome:
        query = query.filter(MetricaKPI.nome.ilike(f"%{nome}%"))
    
    metricas = query.order_by(MetricaKPI.nome).offset(skip).limit(limit).all()
    return metricas

@router.get("/metricas/{metrica_id}", response_model=MetricaKPIRead)
def obter_metrica(metrica_id: int, db: Session = Depends(get_db)):
    """Obtém uma métrica/KPI pelo ID"""
    metrica = db.query(MetricaKPI).filter(MetricaKPI.id_metrica == metrica_id).first()
    if not metrica:
        raise HTTPException(status_code=404, detail="Métrica não encontrada")
    return metrica

@router.put("/metricas/{metrica_id}", response_model=MetricaKPIRead)
def atualizar_metrica(
    metrica_id: int,
    metrica_data: MetricaKPIBase,
    db: Session = Depends(get_db)
):
    """Atualiza uma métrica/KPI"""
    metrica = db.query(MetricaKPI).filter(MetricaKPI.id_metrica == metrica_id).first()
    if not metrica:
        raise HTTPException(status_code=404, detail="Métrica não encontrada")
    
    for key, value in metrica_data.dict(exclude_unset=True).items():
        setattr(metrica, key, value)
    
    db.commit()
    db.refresh(metrica)
    return metrica

@router.delete("/metricas/{metrica_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_metrica(metrica_id: int, db: Session = Depends(get_db)):
    """Deleta uma métrica/KPI"""
    metrica = db.query(MetricaKPI).filter(MetricaKPI.id_metrica == metrica_id).first()
    if not metrica:
        raise HTTPException(status_code=404, detail="Métrica não encontrada")
    
    db.delete(metrica)
    db.commit()
    return None

@router.get("/metricas/{metrica_id}/calcular")
def calcular_metrica(
    metrica_id: int,
    parametros: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Calcula o valor de uma métrica/KPI"""
    metrica = db.query(MetricaKPI).filter(MetricaKPI.id_metrica == metrica_id).first()
    if not metrica:
        raise HTTPException(status_code=404, detail="Métrica não encontrada")
    
    # Analisar parâmetros se fornecidos
    params_dict = {}
    if parametros:
        try:
            params_dict = json.loads(parametros)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Parâmetros inválidos")
    
    # Calcular métrica baseada no tipo
    resultado = calcular_valor_metrica(metrica, params_dict, db)
    
    return {
        "metrica": metrica,
        "valor": resultado,
        "parametros": params_dict,
        "data_calculo": datetime.now(),
        "unidade_medida": metrica.unidade_medida
    }

# ========== CACHE DE DADOS ==========
@router.post("/cache/", response_model=CacheDadosBIRead, status_code=status.HTTP_201_CREATED)
def criar_cache(cache: CacheDadosBICreate, db: Session = Depends(get_db)):
    """Cria um novo cache de dados"""
    db_cache = CacheDadosBI(
        chave_cache=cache.chave_cache,
        dados_json=cache.dados_json,
        data_geracao=datetime.now(),
        data_expiracao=cache.data_expiracao or (datetime.now() + timedelta(hours=1))
    )
    db.add(db_cache)
    db.commit()
    db.refresh(db_cache)
    return db_cache

@router.get("/cache/", response_model=List[CacheDadosBIRead])
def listar_cache(
    skip: int = 0,
    limit: int = 100,
    apenas_validos: bool = True,
    chave: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lista caches de dados"""
    query = db.query(CacheDadosBI)
    
    if apenas_validos:
        query = query.filter(CacheDadosBI.data_expiracao > datetime.now())
    
    if chave:
        query = query.filter(CacheDadosBI.chave_cache.ilike(f"%{chave}%"))
    
    caches = query.order_by(CacheDadosBI.data_geracao.desc()).offset(skip).limit(limit).all()
    return caches

@router.get("/cache/{chave}")
def obter_cache_por_chave(chave: str, db: Session = Depends(get_db)):
    """Obtém cache por chave"""
    cache = db.query(CacheDadosBI).filter(
        CacheDadosBI.chave_cache == chave,
        CacheDadosBI.data_expiracao > datetime.now()
    ).first()
    
    if not cache:
        raise HTTPException(status_code=404, detail="Cache não encontrado ou expirado")
    
    return cache

@router.delete("/cache/{cache_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_cache(cache_id: int, db: Session = Depends(get_db)):
    """Deleta um cache"""
    cache = db.query(CacheDadosBI).filter(CacheDadosBI.id_cache == cache_id).first()
    if not cache:
        raise HTTPException(status_code=404, detail="Cache não encontrado")
    
    db.delete(cache)
    db.commit()
    return None

@router.post("/cache/limpar")
def limpar_cache(
    expirados: bool = True,
    prefixo: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Limpa o cache de dados"""
    query = db.query(CacheDadosBI)
    
    if expirados:
        query = query.filter(CacheDadosBI.data_expiracao <= datetime.now())
    
    if prefixo:
        query = query.filter(CacheDadosBI.chave_cache.startswith(prefixo))
    
    caches = query.all()
    count = 0
    
    for cache in caches:
        db.delete(cache)
        count += 1
    
    db.commit()
    
    return {
        "mensagem": f"{count} caches removidos",
        "timestamp": datetime.now()
    }

# ========== RELATÓRIOS ==========
@router.post("/relatorios/", response_model=RelatorioRead)
def criar_relatorio(relatorio: RelatorioCreate, db: Session = Depends(get_db)):
    """Cria um novo relatório"""
    # Aqui você criaria o relatório no banco de dados
    # Como não temos o modelo, vou simular a criação
    relatorio_criado = {
        "id_relatorio": 1,  # Simulado
        **relatorio.dict(),
        "data_criacao": datetime.now()
    }
    return relatorio_criado

@router.get("/relatorios/executar")
def executar_relatorio(
    sql_query: str,
    parametros: Optional[str] = None,
    usar_cache: bool = True,
    tempo_expiracao_cache: int = 300,  # 5 minutos em segundos
    db: Session = Depends(get_db)
):
    """Executa uma consulta SQL e retorna os resultados"""
    # Validar query SQL (básico)
    if not sql_query.strip().upper().startswith(("SELECT", "WITH")):
        raise HTTPException(status_code=400, detail="Apenas consultas SELECT são permitidas")
    
    # Gerar chave de cache baseada na query e parâmetros
    cache_key = gerar_chave_cache(sql_query, parametros)
    
    if usar_cache:
        # Verificar cache
        cache = db.query(CacheDadosBI).filter(
            CacheDadosBI.chave_cache == cache_key,
            CacheDadosBI.data_expiracao > datetime.now()
        ).first()
        
        if cache:
            return {
                "dados": cache.dados_json,
                "fonte": "cache",
                "data_geracao": cache.data_geracao,
                "total_registros": len(cache.dados_json) if isinstance(cache.dados_json, list) else 1
            }
    
    # Executar query
    try:
        # Analisar parâmetros se fornecidos
        params_dict = {}
        if parametros:
            try:
                params_dict = json.loads(parametros)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Parâmetros inválidos")
        
        # Executar consulta SQL
        if params_dict:
            result = db.execute(text(sql_query), params_dict)
        else:
            result = db.execute(text(sql_query))
        
        # Converter resultados para dicionário
        colunas = result.keys()
        dados = [dict(zip(colunas, row)) for row in result.fetchall()]
        
        # Salvar no cache se usar_cache=True
        if usar_cache:
            cache_novo = CacheDadosBI(
                chave_cache=cache_key,
                dados_json=dados,
                data_geracao=datetime.now(),
                data_expiracao=datetime.now() + timedelta(seconds=tempo_expiracao_cache)
            )
            db.add(cache_novo)
            db.commit()
        
        return {
            "dados": dados,
            "fonte": "banco_dados",
            "data_geracao": datetime.now(),
            "total_registros": len(dados)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar query: {str(e)}")

@router.get("/relatorios/predefinidos")
def listar_relatorios_predefinidos():
    """Lista relatórios predefinidos do sistema"""
    return {
        "vendas": [
            {
                "nome": "Vendas por Vendedor",
                "descricao": "Total de vendas agrupadas por vendedor",
                "endpoint": "/api/bi/relatorios/vendas-por-vendedor"
            },
            {
                "nome": "Vendas Mensais",
                "descricao": "Vendas totais por mês",
                "endpoint": "/api/bi/relatorios/vendas-mensais"
            }
        ],
        "clientes": [
            {
                "nome": "Clientes Mais Ativos",
                "descricao": "Top 10 clientes com mais compras",
                "endpoint": "/api/bi/relatorios/clientes-ativos"
            }
        ],
        "atendimento": [
            {
                "nome": "Tickets por Tipo",
                "descricao": "Distribuição de tickets por tipo de atendimento",
                "endpoint": "/api/bi/relatorios/tickets-por-tipo"
            }
        ]
    }

# ========== RELATÓRIOS PREDEFINIDOS ==========
@router.get("/relatorios/vendas-por-vendedor")
def relatorio_vendas_por_vendedor(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    usar_cache: bool = True,
    db: Session = Depends(get_db)
):
    """Relatório de vendas agrupadas por vendedor"""
    query = """
    SELECT 
        v.vendedorid,
        v.nome as vendedor,
        COUNT(p.pedidoid) as total_pedidos,
        SUM(h.valor_compra) as valor_total_vendas,
        AVG(h.valor_compra) as valor_medio_venda
    FROM vc.vendedor v
    LEFT JOIN vc.pedidos_de_venda p ON v.vendedorid = p.vendedorid
    LEFT JOIN vc.historico_compra h ON p.pedidoid = h.pedido_id
    WHERE 1=1
    """
    
    params = {}
    if data_inicio:
        query += " AND p.data_prevista_entrega >= :data_inicio"
        params["data_inicio"] = data_inicio
    if data_fim:
        query += " AND p.data_prevista_entrega <= :data_fim"
        params["data_fim"] = data_fim
    
    query += " GROUP BY v.vendedorid, v.nome ORDER BY valor_total_vendas DESC NULLS LAST"
    
    # Executar usando a função de relatório genérica
    from datetime import date as date_type
    from .bi import executar_relatorio
    
    params_str = json.dumps(params) if params else None
    return executar_relatorio.__wrapped__(
        sql_query=query,
        parametros=params_str,
        usar_cache=usar_cache,
        tempo_expiracao_cache=300,  # 5 minutos
        db=db
    )

@router.get("/relatorios/vendas-mensais")
def relatorio_vendas_mensais(
    ano: Optional[int] = None,
    meses: int = 12,
    db: Session = Depends(get_db)
):
    """Relatório de vendas mensais"""
    query = """
    SELECT 
        DATE_TRUNC('month', p.data_prevista_entrega) as mes,
        EXTRACT(YEAR FROM p.data_prevista_entrega) as ano,
        EXTRACT(MONTH FROM p.data_prevista_entrega) as mes_numero,
        COUNT(p.pedidoid) as total_pedidos,
        SUM(h.valor_compra) as valor_total_vendas,
        COUNT(DISTINCT p.cliente_finalid) as clientes_ativos
    FROM vc.pedidos_de_venda p
    LEFT JOIN vc.historico_compra h ON p.pedidoid = h.pedido_id
    WHERE p.data_prevista_entrega IS NOT NULL
    """
    
    params = {}
    if ano:
        query += " AND EXTRACT(YEAR FROM p.data_prevista_entrega) = :ano"
        params["ano"] = ano
    else:
        # Últimos N meses por padrão
        query += " AND p.data_prevista_entrega >= CURRENT_DATE - INTERVAL ':meses months'"
        params["meses"] = meses
    
    query += """
    GROUP BY 
        DATE_TRUNC('month', p.data_prevista_entrega),
        EXTRACT(YEAR FROM p.data_prevista_entrega),
        EXTRACT(MONTH FROM p.data_prevista_entrega)
    ORDER BY mes DESC
    """
    
    params_str = json.dumps(params) if params else None
    return executar_relatorio.__wrapped__(
        sql_query=query,
        parametros=params_str,
        usar_cache=True,
        tempo_expiracao_cache=3600,  # 1 hora
        db=db
    )

@router.get("/relatorios/clientes-ativos")
def relatorio_clientes_ativos(
    top_n: int = 10,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Relatório dos clientes mais ativos"""
    query = """
    SELECT 
        c.cliente_finalid,
        c.nome as cliente,
        COUNT(p.pedidoid) as total_compras,
        SUM(h.valor_compra) as valor_total_gasto,
        MAX(p.data_prevista_entrega) as ultima_compra,
        COUNT(DISTINCT EXTRACT(MONTH FROM p.data_prevista_entrega)) as meses_ativos
    FROM vc.cliente_final c
    LEFT JOIN vc.pedidos_de_venda p ON c.cliente_finalid = p.cliente_finalid
    LEFT JOIN vc.historico_compra h ON p.pedidoid = h.pedido_id
    WHERE 1=1
    """
    
    params = {"top_n": top_n}
    if data_inicio:
        query += " AND p.data_prevista_entrega >= :data_inicio"
        params["data_inicio"] = data_inicio
    if data_fim:
        query += " AND p.data_prevista_entrega <= :data_fim"
        params["data_fim"] = data_fim
    
    query += """
    GROUP BY c.cliente_finalid, c.nome
    HAVING COUNT(p.pedidoid) > 0
    ORDER BY valor_total_gasto DESC NULLS LAST
    LIMIT :top_n
    """
    
    params_str = json.dumps(params) if params else None
    return executar_relatorio.__wrapped__(
        sql_query=query,
        parametros=params_str,
        usar_cache=True,
        tempo_expiracao_cache=300,
        db=db
    )

@router.get("/relatorios/tickets-por-tipo")
def relatorio_tickets_por_tipo(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Relatório de tickets agrupados por tipo"""
    query = """
    SELECT 
        t.tipo,
        COUNT(t.id_ticket) as total_tickets,
        COUNT(CASE WHEN t.status = 'RESOLVIDO' THEN 1 END) as tickets_resolvidos,
        AVG(EXTRACT(EPOCH FROM (t.data_resolucao - t.data_abertura))/3600) as tempo_medio_resolucao_horas,
        COUNT(CASE WHEN t.prioridade = 'URGENTE' THEN 1 END) as tickets_urgentes
    FROM sm.ticket_atendimento t
    WHERE 1=1
    """
    
    params = {}
    if data_inicio:
        query += " AND t.data_abertura >= :data_inicio"
        params["data_inicio"] = data_inicio
    if data_fim:
        query += " AND t.data_abertura <= :data_fim"
        params["data_fim"] = data_fim
    
    query += " GROUP BY t.tipo ORDER BY total_tickets DESC"
    
    params_str = json.dumps(params) if params else None
    return executar_relatorio.__wrapped__(
        sql_query=query,
        parametros=params_str,
        usar_cache=True,
        tempo_expiracao_cache=300,
        db=db
    )

# ========== KPI CALCULATION ==========
@router.get("/kpis/calculados")
def calcular_kpis_principais(db: Session = Depends(get_db)):
    """Calcula os principais KPIs do sistema"""
    kpis = {}
    
    # 1. Total de Vendas
    query_vendas = "SELECT SUM(valor_compra) FROM vc.historico_compra"
    result = db.execute(text(query_vendas)).fetchone()
    kpis["total_vendas"] = float(result[0] or 0)
    
    # 2. Total de Clientes
    query_clientes = "SELECT COUNT(*) FROM vc.cliente_final"
    result = db.execute(text(query_clientes)).fetchone()
    kpis["total_clientes"] = result[0]
    
    # 3. Ticket Médio
    query_ticket_medio = """
    SELECT AVG(valor_compra) 
    FROM vc.historico_compra 
    WHERE valor_compra IS NOT NULL
    """
    result = db.execute(text(query_ticket_medio)).fetchone()
    kpis["ticket_medio"] = float(result[0] or 0)
    
    # 4. Total de Tickets Abertos
    query_tickets_abertos = """
    SELECT COUNT(*) 
    FROM sm.ticket_atendimento 
    WHERE status IN ('ABERTO', 'EM_ANDAMENTO')
    """
    result = db.execute(text(query_tickets_abertos)).fetchone()
    kpis["tickets_abertos"] = result[0]
    
    # 5. Taxa de Resolução de Tickets
    query_taxa_resolucao = """
    SELECT 
        COUNT(CASE WHEN status = 'RESOLVIDO' THEN 1 END) * 100.0 / COUNT(*)
    FROM sm.ticket_atendimento
    WHERE data_abertura >= CURRENT_DATE - INTERVAL '30 days'
    """
    result = db.execute(text(query_taxa_resolucao)).fetchone()
    kpis["taxa_resolucao_tickets"] = float(result[0] or 0)
    
    # 6. Vendas do Mês
    query_vendas_mes = """
    SELECT SUM(valor_compra)
    FROM vc.historico_compra h
    JOIN vc.pedidos_de_venda p ON h.pedido_id = p.pedidoid
    WHERE EXTRACT(MONTH FROM p.data_prevista_entrega) = EXTRACT(MONTH FROM CURRENT_DATE)
    AND EXTRACT(YEAR FROM p.data_prevista_entrega) = EXTRACT(YEAR FROM CURRENT_DATE)
    """
    result = db.execute(text(query_vendas_mes)).fetchone()
    kpis["vendas_mes_atual"] = float(result[0] or 0)
    
    # 7. Novos Clientes no Mês
    query_novos_clientes = """
    SELECT COUNT(*)
    FROM vc.cliente_final
    WHERE EXTRACT(MONTH FROM data_ultima_compra) = EXTRACT(MONTH FROM CURRENT_DATE)
    AND EXTRACT(YEAR FROM data_ultima_compra) = EXTRACT(YEAR FROM CURRENT_DATE)
    """
    result = db.execute(text(query_novos_clientes)).fetchone()
    kpis["novos_clientes_mes"] = result[0]
    
    return {
        "kpis": kpis,
        "data_calculo": datetime.now(),
        "periodo": "até a data atual"
    }

@router.get("/kpis/tendencia")
def tendencia_kpis(
    periodo: str = "mensal",  # diario, semanal, mensal
    kpi: str = "vendas",  # vendas, tickets, clientes
    db: Session = Depends(get_db)
):
    """Análise de tendência dos KPIs ao longo do tempo"""
    
    if periodo == "mensal":
        group_by = "DATE_TRUNC('month', data)"
        if kpi == "vendas":
            query = """
            SELECT 
                DATE_TRUNC('month', p.data_prevista_entrega) as periodo,
                COUNT(p.pedidoid) as quantidade,
                SUM(h.valor_compra) as valor
            FROM vc.pedidos_de_venda p
            LEFT JOIN vc.historico_compra h ON p.pedidoid = h.pedido_id
            WHERE p.data_prevista_entrega IS NOT NULL
            GROUP BY DATE_TRUNC('month', p.data_prevista_entrega)
            ORDER BY periodo DESC
            LIMIT 12
            """
        elif kpi == "tickets":
            query = """
            SELECT 
                DATE_TRUNC('month', data_abertura) as periodo,
                COUNT(id_ticket) as quantidade,
                COUNT(CASE WHEN status = 'RESOLVIDO' THEN 1 END) as resolvidos
            FROM sm.ticket_atendimento
            WHERE data_abertura IS NOT NULL
            GROUP BY DATE_TRUNC('month', data_abertura)
            ORDER BY periodo DESC
            LIMIT 12
            """
    
    result = db.execute(text(query)).fetchall()
    
    tendencia = [
        {
            "periodo": row[0],
            "quantidade": row[1],
            "valor": float(row[2]) if len(row) > 2 else None,
            "resolvidos": row[3] if len(row) > 3 else None
        }
        for row in result
    ]
    
    return {
        "kpi": kpi,
        "periodo": periodo,
        "tendencia": tendencia,
        "total_periodos": len(tendencia)
    }

# ========== FUNÇÕES AUXILIARES ==========
def gerar_chave_cache(sql_query: str, parametros: Optional[str] = None) -> str:
    """Gera uma chave de cache única baseada na query e parâmetros"""
    base_string = sql_query.strip().lower()
    if parametros:
        base_string += parametros
    
    # Usar hash SHA256 para garantir chave única
    hash_obj = hashlib.sha256(base_string.encode())
    return f"sql_{hash_obj.hexdigest()[:32]}"

def gerar_dados_dashboard(dashboard: Dashboard, db: Session) -> Dict[str, Any]:
    """Gera dados para um dashboard baseado em sua configuração"""
    config = dashboard.config_json or {}
    widgets = config.get("widgets", [])
    
    dados = {}
    
    for widget in widgets:
        widget_type = widget.get("type")
        widget_id = widget.get("id")
        
        if widget_type == "kpi":
            # Buscar valor do KPI
            metrica_id = widget.get("metrica_id")
            if metrica_id:
                metrica = db.query(MetricaKPI).filter(MetricaKPI.id_metrica == metrica_id).first()
                if metrica:
                    valor = calcular_valor_metrica(metrica, {}, db)
                    dados[widget_id] = {
                        "valor": valor,
                        "nome": metrica.nome,
                        "unidade": metrica.unidade_medida
                    }
        
        elif widget_type == "grafico":
            # Gerar dados para gráfico
            chart_type = widget.get("chart_type")
            if chart_type == "vendas_por_vendedor":
                # Dados pré-definidos para gráfico
                dados[widget_id] = gerar_dados_grafico_vendas(db)
            elif chart_type == "tickets_por_tipo":
                dados[widget_id] = gerar_dados_grafico_tickets(db)
    
    return dados

def calcular_valor_metrica(metrica: MetricaKPI, parametros: Dict, db: Session) -> Any:
    """Calcula o valor de uma métrica baseado em sua fórmula"""
    formula = metrica.formula_calculo or ""
    
    # Exemplos de fórmulas predefinidas
    if formula == "total_vendas":
        query = "SELECT SUM(valor_compra) FROM vc.historico_compra"
        result = db.execute(text(query)).fetchone()
        return float(result[0] or 0)
    
    elif formula == "total_clientes":
        query = "SELECT COUNT(*) FROM vc.cliente_final"
        result = db.execute(text(query)).fetchone()
        return result[0]
    
    elif formula == "ticket_medio":
        query = """
        SELECT AVG(valor_compra) 
        FROM vc.historico_compra 
        WHERE valor_compra IS NOT NULL
        """
        result = db.execute(text(query)).fetchone()
        return float(result[0] or 0)
    
    elif formula == "tickets_abertos":
        query = """
        SELECT COUNT(*) 
        FROM sm.ticket_atendimento 
        WHERE status IN ('ABERTO', 'EM_ANDAMENTO')
        """
        result = db.execute(text(query)).fetchone()
        return result[0]
    
    else:
        # Se não for fórmula predefinida, retornar valor padrão
        return 0

def gerar_dados_grafico_vendas(db: Session) -> Dict:
    """Gera dados para gráfico de vendas por vendedor"""
    query = """
    SELECT 
        v.nome,
        SUM(h.valor_compra) as valor
    FROM vc.vendedor v
    LEFT JOIN vc.pedidos_de_venda p ON v.vendedorid = p.vendedorid
    LEFT JOIN vc.historico_compra h ON p.pedidoid = h.pedido_id
    GROUP BY v.vendedorid, v.nome
    ORDER BY valor DESC NULLS LAST
    LIMIT 10
    """
    
    result = db.execute(text(query)).fetchall()
    
    return {
        "labels": [row[0] for row in result],
        "datasets": [{
            "label": "Vendas por Vendedor",
            "data": [float(row[1] or 0) for row in result]
        }]
    }

def gerar_dados_grafico_tickets(db: Session) -> Dict:
    """Gera dados para gráfico de tickets por tipo"""
    query = """
    SELECT 
        tipo,
        COUNT(*) as quantidade
    FROM sm.ticket_atendimento
    WHERE tipo IS NOT NULL
    GROUP BY tipo
    ORDER BY quantidade DESC
    """
    
    result = db.execute(text(query)).fetchall()
    
    return {
        "labels": [row[0] for row in result],
        "datasets": [{
            "label": "Tickets por Tipo",
            "data": [row[1] for row in result]
        }]
    }

@router.get("/exportar/dados")
def exportar_dados(
    formato: str = "json",  # json, csv
    tipo: str = "vendas",  # vendas, clientes, tickets
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Exporta dados em diferentes formatos"""
    
    queries = {
        "vendas": """
        SELECT 
            p.pedidoid,
            c.nome as cliente,
            v.nome as vendedor,
            p.data_prevista_entrega,
            h.valor_compra,
            p.status
        FROM vc.pedidos_de_venda p
        JOIN vc.cliente_final c ON p.cliente_finalid = c.cliente_finalid
        JOIN vc.vendedor v ON p.vendedorid = v.vendedorid
        LEFT JOIN vc.historico_compra h ON p.pedidoid = h.pedido_id
        WHERE 1=1
        """,
        "clientes": """
        SELECT 
            cliente_finalid,
            nome,
            cpf_cnpj,
            email,
            telefone,
            cidade,
            data_ultima_compra,
            valor_compra
        FROM vc.cliente_final
        WHERE 1=1
        """,
        "tickets": """
        SELECT 
            t.id_ticket,
            c.nome as cliente,
            t.assunto,
            t.tipo,
            t.status,
            t.prioridade,
            t.data_abertura,
            t.data_resolucao
        FROM sm.ticket_atendimento t
        JOIN vc.cliente_final c ON t.id_cliente_final = c.cliente_finalid
        WHERE 1=1
        """
    }
    
    if tipo not in queries:
        raise HTTPException(status_code=400, detail=f"Tipo {tipo} não suportado")
    
    query = queries[tipo]
    params = {}
    
    if data_inicio:
        if tipo == "vendas":
            query += " AND p.data_prevista_entrega >= :data_inicio"
        elif tipo == "tickets":
            query += " AND t.data_abertura >= :data_inicio"
        params["data_inicio"] = data_inicio
    
    if data_fim:
        if tipo == "vendas":
            query += " AND p.data_prevista_entrega <= :data_fim"
        elif tipo == "tickets":
            query += " AND t.data_abertura <= :data_fim"
        params["data_fim"] = data_fim
    
    if tipo == "vendas":
        query += " ORDER BY p.data_prevista_entrega DESC"
    elif tipo == "tickets":
        query += " ORDER BY t.data_abertura DESC"
    
    result = db.execute(text(query), params).fetchall()
    colunas = result.keys() if hasattr(result, 'keys') else []
    
    dados = [dict(zip(colunas, row)) for row in result]
    
    if formato == "csv":
        # Simular retorno CSV
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=colunas)
        writer.writeheader()
        writer.writerows(dados)
        
        return {
            "formato": "csv",
            "tipo": tipo,
            "dados": output.getvalue(),
            "total_registros": len(dados)
        }
    
    return {
        "formato": "json",
        "tipo": tipo,
        "dados": dados,
        "total_registros": len(dados),
        "periodo": {
            "inicio": data_inicio,
            "fim": data_fim
        }
    }