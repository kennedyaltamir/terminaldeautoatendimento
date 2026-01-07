import requests
import uuid
import sys

# Configuração
BASE_URL = "http://localhost:8000/api"
UNIQUE_ID = uuid.uuid4().hex[:6]

# Cores para o terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def print_step(msg):
    print(f"\n{Colors.HEADER}=== {msg} ==={Colors.ENDC}")

def print_success(msg):
    print(f"{Colors.OKGREEN}✅ {msg}{Colors.ENDC}")

def print_fail(msg, response=None):
    print(f"{Colors.FAIL}❌ {msg}{Colors.ENDC}")
    if response:
        print(f"{Colors.FAIL}   Status: {response.status_code}{Colors.ENDC}")
        print(f"{Colors.FAIL}   Body: {response.text}{Colors.ENDC}")

def get_token(email, password):
    res = requests.post(f"{BASE_URL}/auth/token", data={
        "username": email,
        "password": password
    })
    if res.status_code == 200:
        return res.json()["access_token"]
    return None

def test_access(role_name, email, password):
    print(f"Testing access for: {Colors.OKBLUE}{role_name}{Colors.ENDC} ({email})")
    
    # 1. Login
    token = get_token(email, password)
    if not token:
        print_fail("Falha no Login")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Tentar acessar a rota problemática
    url = f"{BASE_URL}/admin/delivery/orders"
    try:
        res = requests.get(url, headers=headers)
        
        if res.status_code == 200:
            print_success(f"Acesso PERMITIDO! (Retornou {len(res.json())} pedidos)")
        elif res.status_code == 403:
            print_fail("Acesso NEGADO (403 Forbidden)", res)
        else:
            print_fail(f"Erro inesperado ({res.status_code})", res)
            
    except Exception as e:
        print_fail(f"Erro de conexão: {e}")

def main():
    print_step("1. CRIANDO AMBIENTE DE TESTE")
    
    owner_email = f"dono_{UNIQUE_ID}@test.com"
    driver_email = f"driver_{UNIQUE_ID}@test.com"
    manager_email = f"manager_{UNIQUE_ID}@test.com"
    password = "password123"
    slug = f"delivery-test-{UNIQUE_ID}"

    # 1. Registrar Empresa (Dono)
    payload = {
        "company_name": f"Delivery Test {UNIQUE_ID}",
        "company_slug": slug,
        "owner_email": owner_email,
        "password": password,
        "segment": "gastro"
    }
    res = requests.post(f"{BASE_URL}/auth/register", json=payload)
    if res.status_code != 201:
        print_fail("Falha ao criar empresa", res)
        sys.exit(1)
    
    owner_token = res.json()["access_token"]
    print_success(f"Empresa criada: {slug}")

    # 2. Criar Entregador
    driver_payload = {
        "name": "João Motoboy",
        "email": driver_email,
        "password": password,
        "role": "driver"
    }
    res_driver = requests.post(f"{BASE_URL}/admin/employees", json=driver_payload, headers={"Authorization": f"Bearer {owner_token}"})
    if res_driver.status_code == 201:
        print_success("Entregador criado")
    else:
        print_fail("Falha ao criar entregador", res_driver)

    # 3. Criar Gerente
    manager_payload = {
        "name": "Maria Gerente",
        "email": manager_email,
        "password": password,
        "role": "manager"
    }
    res_manager = requests.post(f"{BASE_URL}/admin/employees", json=manager_payload, headers={"Authorization": f"Bearer {owner_token}"})
    if res_manager.status_code == 201:
        print_success("Gerente criado")

    # --- INÍCIO DOS TESTES DE ACESSO ---
    
    print_step("2. TESTANDO ACESSO À ROTA DE DELIVERY")
    
    # Teste A: Dono
    test_access("DONO (Owner)", owner_email, password)
    
    # Teste B: Entregador
    test_access("ENTREGADOR (Driver)", driver_email, password)
    
    # Teste C: Gerente
    test_access("GERENTE (Manager)", manager_email, password)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelado.")