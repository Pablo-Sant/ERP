from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.api_router import api_router  


def create_app() -> FastAPI:
    
    app = FastAPI(
        title="BluERP API",
        description="Sistema ERP Integrado",
        version="1.0.0"
    )

    
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

    
    app.include_router(api_router, prefix="/api/v1")

    
    @app.get("/")
    async def root():
        return {"message": "BluERP API - Sistema ERP Integrado"}

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    @app.get("/api/health")
    async def api_health_check():
        return {"status": "healthy", "service": "BluERP API"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
