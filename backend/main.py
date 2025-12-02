from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.auth import router as auth_router
from api.projects import router as projects_router
from api.mm import router as mm_router
from api.fi import router as fi_router
from api.am import router as ativos.router
from api.rh import router as rh_router

app = FastAPI(
    title="BluERP API",
    description="Sistema ERP Integrado",
    version="1.0.0"
)

# Configuração CORS - Mantenha esta
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Incluir rotas
app.include_router(auth_router, prefix="/api")
app.include_router(projects_router, prefix="/api")
app.include_router(mm_router, prefix="/api")
app.include_router(fi_router, prefix="/api")
app.include_router(ativos.router, prefix="/api")
app.include_router(rh_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "BluERP API - Sistema ERP Integrado"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

# Mantenha apenas esta rota de health para API
@app.get("/api/health")
async def api_health_check():
    return {
        "status": "healthy", 
        "service": "BluERP API",
        "cors": "enabled"
    }

