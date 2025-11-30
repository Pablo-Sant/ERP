from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.auth import router as auth_router

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