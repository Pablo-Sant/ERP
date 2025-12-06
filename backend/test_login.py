# test_login_quick.py
import requests
import json

BASE_URL = "http://localhost:8000/api/auth"

print("🔐 TESTANDO LOGIN NA API")
print("=" * 50)

# Teste 1: Verifique se a rota existe
print("\n1️⃣ Verificando se a API está acessível...")
try:
    response = requests.get(f"{BASE_URL}/docs", timeout=5)
    print(f"   ✅ Swagger UI: Status {response.status_code}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# Teste 2: Tente login
print("\n2️⃣ Tentando login...")
try:
    response = requests.post(
        f"{BASE_URL}/login",
        json={
            "username": "admin@bluerp.com",  # ou "admin" se for pelo nome
            "password": "admin123"
        },
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ LOGIN BEM-SUCEDIDO!")
        print(f"   🔑 Token recebido: {data['access_token'][:30]}...")
        print(f"   👤 Usuário: {data['user']}")
    elif response.status_code == 400:
        print(f"   ❌ Erro 400: {response.text}")
        print("   Possíveis problemas:")
        print("   - Usuário não existe no banco")
        print("   - Senha incorreta")
        print("   - Usuário inativo")
    else:
        print(f"   ❌ Erro {response.status_code}: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("   ❌ Não foi possível conectar ao servidor")
    print("   Verifique se o servidor está rodando: python main.py")
except Exception as e:
    print(f"   ❌ Erro na requisição: {type(e).__name__}: {e}")