# minimal_server.py
from fastapi import FastAPI
import uvicorn
import asyncio

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "✅ Servidor mínimo funcionando!"}

@app.get("/health")
async def health():
    return {"status": "ok", "fast": "response"}

@app.post("/api/auth/login")
async def login_test():
    return {
        "access_token": "test_token_123",
        "token_type": "bearer",
        "user": {"id": 1, "email": "test@test.com"}
    }

if __name__ == "__main__":
    print("🚀 SERVIDOR MÍNIMO INICIANDO...")
    print("🌐 http://localhost:8000")
    print("📄 http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )