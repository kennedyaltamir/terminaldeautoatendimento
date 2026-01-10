# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-09
import requests
import sys
import uuid
from decimal import Decimal
from datetime import datetime

# URL da API local
API_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"

def simular():
    print("🔍 Iniciando simulação de pedido para KDS...")
    
    # 1. Login
    auth_res = requests.post(f"{API_URL}/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    if auth_res.status_code != 200:
        print(f"❌ Erro no login: {auth_res.text}")
        return
        
    token = auth_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Garantir Produto de Cozinha
    # Cria ou busca um produto que com certeza aparece na tela de cozinha
    cat_res = requests.post(f"{API_URL}/admin/menu/categories", headers=headers, json={"name": "Testes KDS"})
    cat_id = cat_res.json()["id"]
    
    prod_res = requests.post(f"{API_URL}/admin/menu/products", headers=headers, json={
        "category_id": cat_id,
        "name": f"Burger Teste {uuid.uuid4().hex[:4]}",
        "price": 25.00,
        "station": "kitchen", # <--- CRÍTICO: Define a estação correta
        "is_available": True
    })
    prod_id = prod_res.json()["id"]
    
    print(f"✅ Produto de Cozinha criado: ID {prod_id}")

    # 3. Criar Pedido
    # Usamos 'dine_in' com mesa 1 para garantir que apareça no KDS padrão
    # Se a mesa não estiver aberta, o backend deve abrir automaticamente ou aceitar se for staff-override
    payload = {
        "table_id": 1,
        "qr_token": "staff-override",
        "order_type": "dine_in",
        "customer_name": "Teste Voz KDS",
        "payment_method": "cash",
        "items": [{"product_id": prod_id, "quantity": 1}]
    }
    
    # Tenta abrir a mesa antes, caso esteja fechada
    requests.post(f"{API_URL}/admin/tables/1/open", headers=headers, json={"customer_name": "Teste Voz KDS"})

    order_res = requests.post(f"{API_URL}/{SLUG}/orders", json=payload)
    if order_res.status_code != 201:
        print(f"❌ Erro ao criar pedido: {order_res.text}")
        return
        
    order_data = order_res.json()
    order_id = order_data["id"]
    print(f"✅ Pedido criado: #{order_id[:6]}")

    # 4. Confirmar Pagamento (Para aparecer no KDS como 'Pendente' ou 'Preparando')
    # Se for cash, já nasce pendente. Se for online, precisa pagar.
    # Vamos forçar status 'paid' para garantir.
    patch_res = requests.patch(
        f"{API_URL}/admin/orders/{order_id}/payment",
        headers=headers,
        json={"payment_status": "paid"}
    )

    if patch_res.status_code == 200:
        print("🚀 SUCESSO! Pedido pago e enviado para a cozinha.")
        print(f"👉 ID para falar: {order_id[:4]} (ou o número que aparecer na tela)")
        print(f"👉 Mesa: 1")
    else:
        print(f"❌ Erro ao confirmar: {patch_res.text}")

if __name__ == "__main__":
    simular()
