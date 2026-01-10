import requests
import uuid
import os
import sys
import json
from datetime import datetime

# Configuração
BASE_URL = "http://localhost:8000/api"
REPORT_PATH = "docs/ROUTE_TEST_REPORT.md"

# Cores para o terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

# Armazenamento de Resultados
results = []

def log_result(route, method, status, message, success):
    icon = "✅" if success else "❌"
    print(f"{icon} [{method}] {route}: {message}")
    results.append({
        "route": route,
        "method": method,
        "status": status,
        "message": message,
        "success": success
    })

def run_test(name, func, *args):
    print(f"\n{Colors.HEADER}--- Testando: {name} ---{Colors.ENDC}")
    try:
        return func(*args)
    except Exception as e:
        print(f"{Colors.FAIL}Erro Crítico: {e}{Colors.ENDC}")
        return None

def main():
    # Dados Dinâmicos para o Teste
    unique_id = uuid.uuid4().hex[:6]
    email = f"test-{unique_id}@mesaflow.com"
    password = "Password123!"
    slug = f"restaurante-{unique_id}"
    
    token = None
    headers = {}

    # 1. AUTH: Registro
    def test_register():
        payload = {
            "company_name": f"Restaurante Teste {unique_id}",
            "company_slug": slug,
            "owner_email": email,
            "password": password,
            "segment": "gastro"
        }
        res = requests.post(f"{BASE_URL}/auth/register", json=payload)
        if res.status_code == 201:
            log_result("/auth/register", "POST", 201, "Conta criada com sucesso", True)
            return res.json()["access_token"]
        else:
            log_result("/auth/register", "POST", res.status_code, f"Falha: {res.text}", False)
            sys.exit(1)

    token = run_test("Autenticação", test_register)
    headers = {"Authorization": f"Bearer {token}"}

    # 2. SETTINGS: Atualizar Tema e Cores (Novos Campos)
    def test_update_theme():
        payload = {
            "primary_color": "#FF0000",
            "background_color": "#000000",
            "text_color": "#FFFFFF",
            "accent_color": "#00FF00"
        }
        res = requests.patch(f"{BASE_URL}/admin/company/me", headers=headers, json=payload)
        if res.status_code == 200:
            data = res.json()
            if data["background_color"] == "#000000":
                log_result("/admin/company/me", "PATCH", 200, "Cores atualizadas (Schema OK)", True)
            else:
                log_result("/admin/company/me", "PATCH", 200, "Retornou 200 mas cores não mudaram", False)
        else:
            log_result("/admin/company/me", "PATCH", res.status_code, f"Falha: {res.text}", False)

    run_test("Configurações de Tema", test_update_theme)

    # 3. UPLOAD: Enviar Imagem Fake (CORRIGIDO)
    def test_upload():
        filename = "test_image.png"
        
        # Cria um arquivo dummy
        with open(filename, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82")
        
        try:
            # Abre o arquivo dentro de um bloco 'with' para garantir que ele feche após o envio
            with open(filename, 'rb') as f:
                files = {'file': (filename, f, 'image/png')}
                res = requests.post(f"{BASE_URL}/upload/", headers=headers, files=files)
            
            # Agora que o arquivo está fechado, podemos validar e deletar
            if res.status_code == 200:
                url = res.json()["url"]
                log_result("/upload/", "POST", 200, f"Upload OK: {url}", True)
            else:
                log_result("/upload/", "POST", res.status_code, f"Falha: {res.text}", False)
                
        finally:
            # Limpa o arquivo mesmo se der erro
            if os.path.exists(filename):
                os.remove(filename)

    run_test("Upload de Arquivos", test_upload)

    # 4. PAYMENT: Gerar URL OAuth
    def test_payment_auth():
        res = requests.get(f"{BASE_URL}/admin/payment/auth-url/mercadopago", headers=headers)
        if res.status_code == 200:
            url = res.json()["url"]
            if "mercadopago.com" in url:
                log_result("/admin/payment/auth-url", "GET", 200, "URL OAuth gerada corretamente", True)
            else:
                log_result("/admin/payment/auth-url", "GET", 200, "URL inválida retornada", False)
        else:
            log_result("/admin/payment/auth-url", "GET", res.status_code, f"Falha: {res.text}", False)

    run_test("Integração de Pagamento", test_payment_auth)

    # 5. MENU: Criar Categoria e Produto
    def test_menu_creation():
        # Categoria
        cat_res = requests.post(f"{BASE_URL}/admin/menu/categories", headers=headers, json={"name": "Test Cat"})
        if cat_res.status_code != 201:
            log_result("/admin/menu/categories", "POST", cat_res.status_code, "Falha ao criar categoria", False)
            return
        
        cat_id = cat_res.json()["id"]
        log_result("/admin/menu/categories", "POST", 201, "Categoria criada", True)

        # Produto
        prod_payload = {
            "category_id": cat_id,
            "name": "Test Burger",
            "price": 25.50,
            "short_code": "10",
            "station": "kitchen"
        }
        prod_res = requests.post(f"{BASE_URL}/admin/menu/products", headers=headers, json=prod_payload)
        if prod_res.status_code == 201:
            log_result("/admin/menu/products", "POST", 201, "Produto criado com campos novos", True)
        else:
            log_result("/admin/menu/products", "POST", prod_res.status_code, f"Falha: {prod_res.text}", False)

    run_test("Gestão de Cardápio", test_menu_creation)

    # 6. PUBLIC: Acessar Cardápio
    def test_public_access():
        res = requests.get(f"{BASE_URL}/{slug}/menu")
        if res.status_code == 200:
            data = res.json()
            # Verifica se as cores estão vindo no público
            if "background_color" in data["company"]:
                log_result(f"/{slug}/menu", "GET", 200, "Cardápio público acessível com tema", True)
            else:
                log_result(f"/{slug}/menu", "GET", 200, "Cardápio acessível mas SEM tema", False)
        else:
            log_result(f"/{slug}/menu", "GET", res.status_code, "Falha ao acessar público", False)

    run_test("Acesso Público", test_public_access)

    # --- GERAÇÃO DO RELATÓRIO ---
    generate_markdown_report()

def generate_markdown_report():
    total = len(results)
    passed = len([r for r in results if r["success"]])
    failed = total - passed
    
    md_content = f"""# 📊 Relatório de Verificação de Rotas - MesaFlow

**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
**Status Geral:** {'✅ APROVADO' if failed == 0 else '⚠️ COM FALHAS'}

## Resumo
- **Total de Testes:** {total}
- **Sucesso:** {passed}
- **Falhas:** {failed}

## Detalhamento

| Rota | Método | Status | Resultado | Mensagem |
| :--- | :---: | :---: | :---: | :--- |
"""

    for r in results:
        icon = "🟢" if r["success"] else "🔴"
        md_content += f"| `{r['route']}` | **{r['method']}** | {r['status']} | {icon} | {r['message']} |\n"

    md_content += "\n---\n*Relatório gerado automaticamente pelo script `verify_full_system.py`*"

    os.makedirs("docs", exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"\n📄 Relatório gerado em: {Colors.OKBLUE}{REPORT_PATH}{Colors.ENDC}")

if __name__ == "__main__":
    print("Certifique-se que o servidor está rodando em localhost:8000")
    main()