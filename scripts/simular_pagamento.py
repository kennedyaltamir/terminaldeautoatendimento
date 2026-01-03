import requests
import sys

# URL da API local
API_URL = "http://localhost:8000/api"
SLUG = "hamburgueria-ze"

def simular():
    # 1. Listar pedidos pendentes para pegar o ID
    print("🔍 Buscando pedidos pendentes...")
    try:
        # Precisamos de um token de admin para listar, vamos logar rapidinho
        auth_res = requests.post(f"{API_URL}/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
        token = auth_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        orders_res = requests.get(f"{API_URL}/admin/{SLUG}/orders", headers=headers)
        orders = orders_res.json()
        
        pending_orders = [o for o in orders if o['payment_status'] == 'pending']
        
        if not pending_orders:
            print("❌ Nenhum pedido pendente encontrado.")
            return

        print(f"✅ Encontrados {len(pending_orders)} pedidos pendentes.")
        target_order = pending_orders[-1] # Pega o último
        print(f"🎯 Alvo: Pedido {target_order['id']} (Mesa {target_order['table']['table_number']})")
        
        # 2. Simular o Webhook do Mercado Pago
        # O sistema espera receber o ID do pagamento no MP.
        # No nosso mock, salvamos o ID como "simulated_12345" ou algo assim.
        # Vamos forçar a atualização via API de Admin para garantir
        
        print("💸 Enviando confirmação de pagamento...")
        
        # Opção 1: Via Webhook (Se tivermos o ID correto do MP)
        # requests.post(f"{API_URL}/webhooks/mercadopago?topic=payment&id=simulated_12345")
        
        # Opção 2: Via Admin (Mais garantido para teste manual)
        patch_res = requests.patch(
            f"{API_URL}/admin/orders/{target_order['id']}/payment",
            headers=headers,
            json={"payment_status": "paid"}
        )
        
        if patch_res.status_code == 200:
            print("🚀 SUCESSO! O pagamento foi confirmado.")
            print("👀 Olhe para a tela do 'celular' (Menu) agora. Ela deve ficar verde em 3 segundos.")
        else:
            print(f"❌ Erro ao confirmar: {patch_res.text}")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    simular()