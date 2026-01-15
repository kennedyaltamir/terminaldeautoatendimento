import requests
import uuid
import sys
import os
import time
from decimal import Decimal

# Adiciona o diretório raiz ao path para importar app.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuração
BASE_URL = "http://localhost:8000/api"
UNIQUE_ID = uuid.uuid4().hex[:6]

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def log(msg): print(f"{Colors.OKBLUE}[INFO]{Colors.ENDC} {msg}")
def success(msg): print(f"{Colors.OKGREEN}[OK]{Colors.ENDC} {msg}")
def fail(msg): 
    print(f"{Colors.FAIL}[FAIL]{Colors.ENDC} {msg}")
    sys.exit(1)

def main():
    print(f"{Colors.HEADER}=== INICIANDO SIMULAÇÃO LOGÍSTICA COMPLETA ==={Colors.ENDC}\n")

    # 1. SETUP: Criar Empresa e Motorista
    log("1. Criando ambiente (Empresa + Motorista)...")
    
    owner_email = f"log-{UNIQUE_ID}@test.com"
    password = "password123"
    slug = f"log-{UNIQUE_ID}"
    
    # Registro
    res = requests.post(f"{BASE_URL}/auth/register", json={
        "company_name": f"Logistics {UNIQUE_ID}",
        "company_slug": slug,
        "owner_email": owner_email,
        "password": password,
        "segment": "gastro"
    })
    if res.status_code != 201: fail(f"Erro registro: {res.text}")
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Configurar Taxa de Entrega (R$ 5,00)
    requests.patch(f"{BASE_URL}/admin/company/me", headers=headers, json={"fixed_delivery_fee": 5.00})
    
    # Criar Motorista
    # CORREÇÃO: Senha deve ter no mínimo 4 caracteres
    driver_res = requests.post(f"{BASE_URL}/admin/employees", headers=headers, json={
        "name": "João Motoboy",
        "email": f"driver-{UNIQUE_ID}@test.com",
        "password": "1234", 
        "role": "driver"
    })
    
    if driver_res.status_code != 201:
        fail(f"Erro ao criar motorista: {driver_res.text}")

    driver_id = driver_res.json()["id"]
    success(f"Ambiente pronto. Taxa de R$ 5,00 configurada. Motorista ID: {driver_id}")

    # 2. PEDIDO: Cliente faz pedido de Delivery
    log("\n2. Cliente criando pedido de Delivery...")
    
    # Criar Produto
    cat_res = requests.post(f"{BASE_URL}/admin/menu/categories", headers=headers, json={"name": "Geral"})
    cat_id = cat_res.json()["id"]
    prod_res = requests.post(f"{BASE_URL}/admin/menu/products", headers=headers, json={
        "category_id": cat_id, "name": "Pizza", "price": 45.00, "is_available": True
    })
    prod_id = prod_res.json()["id"]
    
    # Pedido
    order_payload = {
        "table_id": None,
        "qr_token": "staff-override",
        "order_type": "delivery",
        "customer_name": "Cliente Teste",
        "customer_phone": "11999999999",
        "delivery_address": "Rua Teste, 100",
        "payment_method": "cash",
        "items": [{"product_id": prod_id, "quantity": 1}]
    }
    
    order_res = requests.post(f"{BASE_URL}/{slug}/orders", json=order_payload)
    if order_res.status_code != 201:
        fail(f"Erro ao criar pedido: {order_res.text}")

    order_data = order_res.json()
    order_id = order_data["id"]
    
    # Validação da Taxa
    total = float(order_data["total_amount"])
    if total == 50.00: # 45 (Pizza) + 5 (Taxa)
        success(f"Pedido #{order_id[:6]} criado. Total R$ {total:.2f} (Inclui taxa de R$ 5,00)")
    else:
        fail(f"Erro no cálculo da taxa. Total: {total}")

    # Mover para READY (Cozinha finaliza)
    requests.patch(f"{BASE_URL}/admin/orders/{order_id}", headers=headers, json={"status": "ready"})

    # 3. DESPACHO INTELIGENTE
    log("\n3. Gerente consultando recomendação de motorista...")
    rec_res = requests.get(f"{BASE_URL}/admin/delivery/recommendation", headers=headers)
    recs = rec_res.json()
    
    if not recs:
        fail("Nenhuma recomendação retornada.")

    best_driver = recs[0]
    if best_driver["driver_id"] == driver_id:
        success(f"Sistema recomendou: {best_driver['name']} (Entregas ativas: {best_driver['active_deliveries']})")
    else:
        fail("Recomendação incorreta.")

    log("   Despachando pedido...")
    dispatch_res = requests.patch(f"{BASE_URL}/admin/delivery/orders/{order_id}/dispatch", headers=headers, json={"driver_id": driver_id})
    if dispatch_res.status_code == 200:
        success("Pedido despachado! Notificação WhatsApp enviada (Mock).")
    else:
        fail(f"Erro ao despachar: {dispatch_res.text}")
    
    # 4. PROOF OF DELIVERY (POD)
    log("\n4. Motorista tentando finalizar entrega...")
    
    # Tentativa 1: Sem código
    fail_res = requests.patch(f"{BASE_URL}/admin/delivery/orders/{order_id}/complete", headers=headers, json={})
    if fail_res.status_code == 400:
        success("Sistema bloqueou finalização sem código (Segurança OK).")
    else:
        fail(f"Sistema permitiu finalizar sem código! Status: {fail_res.status_code}")

    # Obter código do banco
    try:
        from app.database import SessionLocal
        from app.models import Order
        db = SessionLocal()
        db_order = db.query(Order).filter(Order.id == order_id).first()
        pod_code = db_order.delivery_code
        db.close()
        log(f"   [Simulação] Cliente informou o código: {pod_code}")
    except Exception as e:
        fail(f"Não foi possível ler o código do banco local: {e}")

    # Tentativa 2: Com código correto
    complete_res = requests.patch(f"{BASE_URL}/admin/delivery/orders/{order_id}/complete", headers=headers, json={"code": pod_code})
    if complete_res.status_code == 200:
        success("Entrega finalizada com sucesso!")
    else:
        fail(f"Erro ao finalizar com código: {complete_res.text}")

    # 5. FINANCEIRO (Cash Management)
    log("\n5. Verificando Carteira do Motorista...")
    
    balance_res = requests.get(f"{BASE_URL}/admin/logistics/drivers/{driver_id}/balance", headers=headers)
    balance = balance_res.json()
    debt = float(balance["current_debt"])
    
    if debt == 50.00:
        success(f"Dívida registrada corretamente: R$ {debt:.2f}")
    else:
        fail(f"Erro no ledger. Dívida esperada: 50.00. Encontrada: {debt}")

    # 6. PRESTAÇÃO DE CONTAS (Settlement)
    log("\n6. Realizando Prestação de Contas...")
    
    settle_res = requests.post(f"{BASE_URL}/admin/logistics/drivers/{driver_id}/settle", headers=headers, json={
        "amount": 50.00,
        "description": "Fechamento do caixa"
    })
    
    if settle_res.status_code == 200:
        balance_res_2 = requests.get(f"{BASE_URL}/admin/logistics/drivers/{driver_id}/balance", headers=headers)
        new_debt = float(balance_res_2.json()["current_debt"])
        if new_debt == 0.00:
            success("Dívida zerada com sucesso!")
        else:
            fail(f"Saldo não zerou. Atual: {new_debt}")
    else:
        fail(f"Erro no acerto de contas: {settle_res.text}")

    # 7. DASHBOARD
    log("\n7. Verificando Dashboard Logístico...")
    dash_res = requests.get(f"{BASE_URL}/admin/logistics/dashboard", headers=headers)
    dash = dash_res.json()
    
    if dash["deliveries_today"] >= 1 and dash["total_collected_cash"] >= 50.00:
        success(f"Dashboard atualizado: {dash['deliveries_today']} entregas, R$ {dash['total_collected_cash']} arrecadados.")
    else:
        fail(f"Dashboard não refletiu os dados. Entregas: {dash['deliveries_today']}, Cash: {dash['total_collected_cash']}")

    print(f"\n{Colors.HEADER}=== TESTE CONCLUÍDO COM SUCESSO ==={Colors.ENDC}")

if __name__ == "__main__":
    main()