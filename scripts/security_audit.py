import requests
import uuid
import time
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

# ==============================================================================
# CONFIGURAÇÃO DO AMBIENTE DE ATAQUE
# ==============================================================================
BASE_URL = "http://localhost:8000/api"
REPORT_FILE = "docs/SECURITY_AUDIT_REPORT.md"

# Cores para o terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

results = []

def log(section, test_name, status, details, severity="INFO"):
    icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    color = Colors.GREEN if status == "PASS" else Colors.RED if status == "FAIL" else Colors.YELLOW
    
    print(f"{color}[{status}] {section}: {test_name}{Colors.ENDC}")
    if status != "PASS":
        print(f"   └── {details}")

    results.append({
        "section": section,
        "test": test_name,
        "status": status,
        "severity": severity,
        "details": details
    })

# ==============================================================================
# 0. SETUP: CRIAÇÃO DE CENÁRIO (Empresa A vs Empresa B)
# ==============================================================================
def setup_environment():
    print(f"{Colors.HEADER}--- 0. SETUP: Criando Cenário de Guerra ---{Colors.ENDC}")
    
    # Empresa A (A Atacante)
    slug_a = f"corp-a-{uuid.uuid4().hex[:6]}"
    email_a = f"admin-a-{uuid.uuid4().hex[:6]}@test.com"
    pass_a = "SenhaForte123!"
    
    # Empresa B (A Vítima)
    slug_b = f"corp-b-{uuid.uuid4().hex[:6]}"
    email_b = f"admin-b-{uuid.uuid4().hex[:6]}@test.com"
    pass_b = "SenhaForte123!"

    # Registrar A
    res_a = requests.post(f"{BASE_URL}/auth/register", json={
        "company_name": "Corp A Attacker", "company_slug": slug_a,
        "owner_email": email_a, "password": pass_a, "segment": "gastro"
    })
    token_a = res_a.json()["access_token"]

    # Registrar B
    res_b = requests.post(f"{BASE_URL}/auth/register", json={
        "company_name": "Corp B Victim", "company_slug": slug_b,
        "owner_email": email_b, "password": pass_b, "segment": "gastro"
    })
    token_b = res_b.json()["access_token"]

    # Criar Produto na Empresa B (Alvo do roubo/deleção)
    headers_b = {"Authorization": f"Bearer {token_b}"}
    cat_res = requests.post(f"{BASE_URL}/admin/menu/categories", headers=headers_b, json={"name": "Cat B"})
    cat_id_b = cat_res.json()["id"]
    
    prod_res = requests.post(f"{BASE_URL}/admin/menu/products", headers=headers_b, json={
        "category_id": cat_id_b, "name": "Produto Secreto B", "price": 100.00
    })
    prod_id_b = prod_res.json()["id"]

    # Criar Funcionário (Garçom) na Empresa A (Para testar Privilege Escalation)
    headers_a = {"Authorization": f"Bearer {token_a}"}
    waiter_email = f"waiter-{uuid.uuid4().hex[:6]}@test.com"
    waiter_pass = "123456"
    requests.post(f"{BASE_URL}/admin/employees", headers=headers_a, json={
        "name": "Garçom A", "email": waiter_email, "password": waiter_pass, "role": "cashier"
    })
    
    # Login Garçom
    res_waiter = requests.post(f"{BASE_URL}/auth/token", data={"username": waiter_email, "password": waiter_pass})
    token_waiter = res_waiter.json()["access_token"]

    return {
        "token_owner_a": token_a,
        "token_waiter_a": token_waiter,
        "token_owner_b": token_b,
        "slug_a": slug_a,
        "slug_b": slug_b,
        "prod_id_b": prod_id_b,
        "cat_id_b": cat_id_b,
        "email_a": email_a
    }

# ==============================================================================
# 1. TESTES DE CONTROLE DE ACESSO (RBAC)
# ==============================================================================
def test_rbac(env):
    print(f"\n{Colors.HEADER}--- 1. Testando RBAC (Controle de Acesso) ---{Colors.ENDC}")
    
    # 1.1 Privilege Escalation
    # Garçom tentando criar outro funcionário (Ação de Dono)
    headers_waiter = {"Authorization": f"Bearer {env['token_waiter_a']}"}
    res = requests.post(f"{BASE_URL}/admin/employees", headers=headers_waiter, json={
        "name": "Hacker", "email": "hacker@test.com", "password": "123", "role": "manager"
    })
    
    if res.status_code == 403:
        log("RBAC", "Privilege Escalation (Garçom -> Admin)", "PASS", "Bloqueado com 403 Forbidden")
    else:
        log("RBAC", "Privilege Escalation (Garçom -> Admin)", "FAIL", f"Permitiu! Status: {res.status_code}", "CRITICAL")

    # 1.2 Acesso Anônimo
    res_anon = requests.get(f"{BASE_URL}/admin/company/me") # Sem header
    if res_anon.status_code == 401:
        log("RBAC", "Acesso Anônimo em Rota Protegida", "PASS", "Bloqueado com 401 Unauthorized")
    else:
        log("RBAC", "Acesso Anônimo em Rota Protegida", "FAIL", f"Permitiu! Status: {res_anon.status_code}", "CRITICAL")

# ==============================================================================
# 2. TESTES DE ISOLAMENTO MULTI-TENANT (IDOR)
# ==============================================================================
def test_idor(env):
    print(f"\n{Colors.HEADER}--- 2. Testando IDOR (Isolamento de Dados) ---{Colors.ENDC}")
    
    headers_a = {"Authorization": f"Bearer {env['token_owner_a']}"}
    
    # 2.1 Cross-Tenant Delete
    # Empresa A tenta deletar produto da Empresa B
    target_url = f"{BASE_URL}/admin/menu/products/{env['prod_id_b']}"
    res = requests.delete(target_url, headers=headers_a)
    
    # O sistema deve retornar 404 (Não encontrado no contexto da empresa A) ou 403
    if res.status_code in [404, 403]:
        log("IDOR", "Deleção Cruzada de Recursos", "PASS", f"Recurso protegido (Status: {res.status_code})")
    else:
        log("IDOR", "Deleção Cruzada de Recursos", "FAIL", f"Empresa A deletou produto da Empresa B! Status: {res.status_code}", "CRITICAL")

    # 2.2 Cross-Tenant Read (Via Slug)
    # Empresa A tenta ler pedidos da Empresa B mudando o slug na URL
    res_read = requests.get(f"{BASE_URL}/admin/{env['slug_b']}/orders", headers=headers_a)
    
    if res_read.status_code == 403:
        log("IDOR", "Leitura Cruzada (Slug Tampering)", "PASS", "Bloqueado com 403 Forbidden")
    else:
        log("IDOR", "Leitura Cruzada (Slug Tampering)", "FAIL", f"Vazamento de dados! Status: {res_read.status_code}", "CRITICAL")

# ==============================================================================
# 3. TESTES DE INTEGRIDADE FINANCEIRA
# ==============================================================================
def test_financial(env):
    print(f"\n{Colors.HEADER}--- 3. Testando Integridade Financeira ---{Colors.ENDC}")
    
    # Criar categoria para A
    headers_a = {"Authorization": f"Bearer {env['token_owner_a']}"}
    cat_res = requests.post(f"{BASE_URL}/admin/menu/categories", headers=headers_a, json={"name": "Fin"})
    cat_id = cat_res.json()["id"]
    
    # Criar produto de R$ 50.00
    prod_res = requests.post(f"{BASE_URL}/admin/menu/products", headers=headers_a, json={
        "category_id": cat_id, "name": "Item Caro", "price": 50.00
    })
    prod_id = prod_res.json()["id"]

    # 3.1 Price Tampering (Manipulação de Preço no Payload)
    # O atacante tenta enviar o pedido dizendo que o preço unitário é R$ 0.01
    payload = {
        "table_id": None, "qr_token": "staff-override", "order_type": "takeout",
        "items": [{
            "product_id": prod_id, 
            "quantity": 1, 
            "unit_price": 0.01 # TENTATIVA DE GOLPE
        }]
    }
    
    res_order = requests.post(f"{BASE_URL}/{env['slug_a']}/orders", json=payload)
    if res_order.status_code == 201:
        order_data = res_order.json()
        total = float(order_data["total_amount"])
        if total == 50.00:
            log("FINANCEIRO", "Price Tampering (Injeção de Preço)", "PASS", "Backend ignorou preço injetado e usou o do banco.")
        else:
            log("FINANCEIRO", "Price Tampering (Injeção de Preço)", "FAIL", f"Vulnerável! Vendeu por R$ {total}", "HIGH")
    else:
        log("FINANCEIRO", "Price Tampering", "WARN", f"Erro ao criar pedido: {res_order.status_code}")

    # 3.2 Negative Quantity
    payload_neg = {
        "table_id": None, "qr_token": "staff-override", "order_type": "takeout",
        "items": [{"product_id": prod_id, "quantity": -10}] # TENTATIVA DE CRÉDITO
    }
    res_neg = requests.post(f"{BASE_URL}/{env['slug_a']}/orders", json=payload_neg)
    
    # Espera-se 422 (Validation Error do Pydantic) ou 400
    if res_neg.status_code in [400, 422]:
        log("FINANCEIRO", "Valores Negativos", "PASS", "Bloqueado corretamente.")
    else:
        log("FINANCEIRO", "Valores Negativos", "FAIL", f"Aceitou quantidade negativa! Status: {res_neg.status_code}", "HIGH")

# ==============================================================================
# 4. TESTES DE INJEÇÃO E VALIDAÇÃO
# ==============================================================================
def test_injection(env):
    print(f"\n{Colors.HEADER}--- 4. Testando Injeção e Validação ---{Colors.ENDC}")
    
    headers_a = {"Authorization": f"Bearer {env['token_owner_a']}"}

    # 4.1 XSS Stored
    # Tentar salvar script no nome da categoria
    xss_payload = "<script>alert('XSS')</script>"
    res_xss = requests.post(f"{BASE_URL}/admin/menu/categories", headers=headers_a, json={"name": xss_payload})
    
    # O backend provavelmente vai salvar (o que é ok, desde que o frontend sanitize).
    # Mas vamos verificar se ele não quebrou ou executou algo no backend.
    if res_xss.status_code == 201:
        data = res_xss.json()
        if data["name"] == xss_payload:
            log("INJECTION", "XSS Stored (Persistência)", "WARN", "Backend salvou tags HTML. Frontend deve sanitizar!", "MEDIUM")
        else:
            log("INJECTION", "XSS Stored (Sanitização)", "PASS", "Backend limpou o input.")
    
    # 4.2 Upload Malicioso
    filename = "malware.jpg"
    
    # Criar arquivo falso .exe renomeado para .jpg
    with open(filename, "wb") as f:
        f.write(b"MZ9000... fake exe content")
    
    try:
        # Abre o arquivo dentro de um bloco 'with' para garantir que ele feche após o envio
        with open(filename, 'rb') as f:
            files = {'file': (filename, f, 'image/jpeg')}
            res_upload = requests.post(f"{BASE_URL}/upload/", headers=headers_a, files=files)
        
        # Se o backend validar magic numbers ou conteúdo, deve bloquear.
        if res_upload.status_code == 200:
            log("INJECTION", "Upload de Arquivo Falso", "FAIL", "Aceitou arquivo com conteúdo inválido (apenas validação de extensão?)", "MEDIUM")
        else:
            log("INJECTION", "Upload de Arquivo Falso", "PASS", "Bloqueou arquivo suspeito.")
            
    finally:
        # Limpa o arquivo mesmo se der erro
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except Exception as e:
                print(f"Aviso: Não foi possível remover {filename}: {e}")

# ==============================================================================
# 5. TESTES DE DISPONIBILIDADE (DOS & BRUTE FORCE)
# ==============================================================================
def test_availability(env):
    print(f"\n{Colors.HEADER}--- 5. Testando Disponibilidade (DoS & Rate Limit) ---{Colors.ENDC}")
    
    # 5.1 Brute Force Login
    print("   -> Disparando 20 tentativas de login falhas...")
    blocked = False
    for i in range(20):
        res = requests.post(f"{BASE_URL}/auth/token", data={"username": env['email_a'], "password": f"wrong{i}"})
        if res.status_code == 429:
            blocked = True
            break
    
    if blocked:
        log("AVAILABILITY", "Rate Limiting (Login)", "PASS", "Sistema bloqueou tentativas excessivas (429).")
    else:
        log("AVAILABILITY", "Rate Limiting (Login)", "FAIL", "Não bloqueou força bruta após 20 tentativas.", "HIGH")

    # 5.2 DoS em Rota Pública (Cardápio)
    # Tentar derrubar a rota de leitura do cardápio
    print("   -> Disparando 50 requests concorrentes no cardápio...")
    
    def call_menu():
        return requests.get(f"{BASE_URL}/{env['slug_a']}/menu").status_code

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(call_menu) for _ in range(50)]
        status_codes = [f.result() for f in futures]
    
    if 429 in status_codes:
        log("AVAILABILITY", "Rate Limiting (API Pública)", "PASS", "Detectou tráfego abusivo e retornou 429.")
    else:
        log("AVAILABILITY", "Rate Limiting (API Pública)", "WARN", "Não bloqueou 50 requests rápidos (Pode ser configuração permissiva).", "MEDIUM")

# ==============================================================================
# GERAÇÃO DE RELATÓRIO
# ==============================================================================
def generate_report():
    print(f"\n{Colors.HEADER}--- Gerando Relatório Final ---{Colors.ENDC}")
    
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("# 🛡️ Relatório de Auditoria de Segurança: MesaFlow\n\n")
        f.write(f"**Data:** {time.strftime('%d/%m/%Y %H:%M')}\n\n")
        
        f.write("| Categoria | Teste | Status | Severidade | Detalhes |\n")
        f.write("|---|---|---|---|---|\n")
        
        for r in results:
            icon = "✅" if r["status"] == "PASS" else "❌" if r["status"] == "FAIL" else "⚠️"
            f.write(f"| {r['section']} | {r['test']} | {icon} {r['status']} | {r['severity']} | {r['details']} |\n")
    
    print(f"📄 Relatório salvo em: {REPORT_FILE}")

if __name__ == "__main__":
    try:
        env = setup_environment()
        test_rbac(env)
        test_idor(env)
        test_financial(env)
        test_injection(env)
        test_availability(env)
    except Exception as e:
        print(f"{Colors.RED}Erro fatal na execução dos testes: {e}{Colors.ENDC}")
    finally:
        generate_report()