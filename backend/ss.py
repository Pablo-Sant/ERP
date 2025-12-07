import requests
import json

BASE_URL = "http://localhost:8000/api/ativos"

def test_endpoints():
    print("=== Testando API de Ativos ===\n")
    
    test_cases = [
        ("Health check", f"{BASE_URL}/teste/banco", "GET", None),
        ("Listar ativos", f"{BASE_URL}/", "GET", None),
        ("Dashboard", f"{BASE_URL}/dashboard/resumo", "GET", None),
        ("Buscar TI", f"{BASE_URL}/buscar?categoria=TI", "GET", None),
        ("Categorias", f"{BASE_URL}/categorias/listar", "GET", None),
        ("Localizações", f"{BASE_URL}/localizacoes/listar", "GET", None),
    ]
    
    for test_name, url, method, data in test_cases:
        print(f"{test_name}:")
        print(f"  URL: {url}")
        try:
            if method == "GET":
                response = requests.get(url, timeout=5)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=5)
            
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if test_name == "Listar ativos":
                        print(f"  Total de ativos: {len(data)}")
                        if data and len(data) > 0:
                            print(f"  Primeiro ativo: {data[0].get('nome', 'N/A')}")
                    elif test_name == "Dashboard":
                        print(f"  Total ativos: {data.get('total_ativos', 'N/A')}")
                        print(f"  Valor total: R$ {data.get('valor_total', 'N/A'):,.2f}")
                    else:
                        print(f"  Response OK")
                except json.JSONDecodeError as e:
                    print(f"  JSON Error: {e}")
                    print(f"  Response (text): {response.text[:200]}...")
            else:
                print(f"  Error: {response.text[:200]}...")
        except requests.exceptions.RequestException as e:
            print(f"  Connection Error: {e}")
        print()

def test_post():
    print("=== Testando POST (Criar ativo) ===\n")
    
    # Versão com campos novos
    novo_ativo = {
        "numero_tag": "ATV-004",
        "nome": "Notebook Dell XPS 15",
        "id_categoria": 1,
        "id_localizacao": 1,
        "data_aquisicao": "2024-01-15",
        "custo_aquisicao": 8500.00,
        "valor_atual": 8500.00,
        "status_ativo": "ativo",
        "criticidade": "medio"
    }
    
    print("Tentando criar ativo com campos novos...")
    try:
        response = requests.post(f"{BASE_URL}/", json=novo_ativo, timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"Ativo criado com ID: {data.get('id')}")
            print(f"Tag: {data.get('numero_tag')}")
            print(f"Nome: {data.get('nome')}")
        else:
            print(f"Error: {response.text[:200]}")
    except requests.exceptions.RequestException as e:
        print(f"Connection Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Versão com campos antigos (para compatibilidade)
    print("Tentando criar ativo com campos antigos...")
    novo_ativo_old = {
        "tag": "ATV-005",
        "nome": "Impressora HP LaserJet",
        "categoria_nome": "TI",
        "localizacao_nome": "Escritório",
        "data_aquisicao": "2024-01-20",
        "valor": 2500.00,
        "status": "ativo",
        "criticidade": "baixa"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/", json=novo_ativo_old, timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"Ativo criado com ID: {data.get('id')}")
            print(f"Tag (old->new): {data.get('tag')} -> {data.get('numero_tag')}")
        else:
            print(f"Error: {response.text[:200]}")
    except requests.exceptions.RequestException as e:
        print(f"Connection Error: {e}")

def test_get_ativo():
    print("\n=== Testando GET ativo específico ===\n")
    
    # Primeiro listar para ver IDs disponíveis
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            ativos = response.json()
            if ativos and len(ativos) > 0:
                ativo_id = ativos[0]['id']
                print(f"Testando GET para ativo ID: {ativo_id}")
                
                response = requests.get(f"{BASE_URL}/{ativo_id}", timeout=5)
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    ativo = response.json()
                    print(f"Nome: {ativo.get('nome')}")
                    print(f"Tag: {ativo.get('numero_tag')}")
                    print(f"Status: {ativo.get('status_ativo')}")
                else:
                    print(f"Error: {response.text[:200]}")
            else:
                print("Nenhum ativo encontrado para testar")
    except requests.exceptions.RequestException as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    print("Iniciando testes...")
    print(f"Base URL: {BASE_URL}\n")
    
    # Testar servidor está rodando
    try:
        test_response = requests.get("http://localhost:8000/", timeout=2)
        print(f"Servidor FastAPI rodando: {test_response.status_code}\n")
    except:
        print("ERRO: Servidor FastAPI não está rodando na porta 8000")
        print("Execute: uvicorn main:app --reload --port 8000")
        exit(1)
    
    test_endpoints()
    test_post()
    test_get_ativo()