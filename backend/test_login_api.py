# scripts/test_login_api.py
import requests
import json

def test_login_api():
    base_url = "http://localhost:8000/api/auth"
    
    # Teste 1: Login com credenciais corretas
    print("🔐 Testando login com credenciais corretas...")
    try:
        response = requests.post(
            f"{base_url}/login",
            json={
                "username": "admin@bluerp.com",  # Pode ser email ou nome
                "password": "admin123"
            },
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login bem-sucedido!")
            print(f"🔑 Token: {data['access_token'][:50]}...")
            print(f"👤 Usuário: {data['user']}")
            
            # Testar endpoint protegido
            token = data['access_token']
            print(f"\n🔒 Testando endpoint protegido /me...")
            
            me_response = requests.get(
                f"{base_url}/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            print(f"Status /me: {me_response.status_code}")
            if me_response.status_code == 200:
                print(f"✅ Dados do usuário: {me_response.json()}")
            else:
                print(f"❌ Erro no /me: {me_response.text}")
                
        else:
            print(f"❌ Erro no login: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    # Teste 2: Login com senha incorreta
    print(f"\n🔐 Testando login com senha incorreta...")
    try:
        response = requests.post(
            f"{base_url}/login",
            json={
                "username": "admin@bluerp.com",
                "password": "senhaerrada"
            },
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.text}")
        
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    # Teste 3: Login com usuário inexistente
    print(f"\n🔐 Testando login com usuário inexistente...")
    try:
        response = requests.post(
            f"{base_url}/login",
            json={
                "username": "naoexiste@teste.com",
                "password": "qualquersenha"
            },
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.text}")
        
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

if __name__ == "__main__":
    test_login_api()