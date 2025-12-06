# run_server.py
import uvicorn
import logging

# Configura logging detalhado
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn")

if __name__ == "__main__":
    print("🚀 Iniciando servidor FastAPI...")
    print("📡 URL: http://localhost:8000")
    print("📄 Docs: http://localhost:8000/docs")
    print("=" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug",
        access_log=True
    )