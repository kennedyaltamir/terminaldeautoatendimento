# DOMAIN: OPERATIONS
# LAST_MODIFIED: 2026-01-08 22:45:00
from locust import HttpUser, task, between, tag
import random

class MesaFlowUser(HttpUser):
    wait_time = between(1, 3) # Simula tempo de pensamento do usuário (1-3s)
    
    # Dados de teste
    slug = "hamburgueria-ze"
    token = None

    def on_start(self):
        """Executado quando o usuário virtual "nasce"."""
        # 1. Acessar Cardápio Público (Cache Warmup)
        self.client.get(f"/api/{self.slug}/menu", name="/menu (Public)")

    @task(3)
    @tag('public')
    def view_menu(self):
        """Simula navegação no cardápio (Alta frequência)."""
        self.client.get(f"/api/{self.slug}/menu", name="/menu (Browse)")

    @task(1)
    @tag('order')
    def create_order(self):
        """Simula criação de pedido (Escrita)."""
        payload = {
            "table_id": None,
            "qr_token": "staff-override", # Simula Kiosk/Takeout
            "order_type": "takeout",
            "customer_name": "Load Test User",
            "payment_method": "cash",
            "items": [
                {"product_id": 1, "quantity": 1} # Assumindo ID 1 existe (Seed)
            ]
        }
        
        # Post com validação de resposta
        with self.client.post(f"/api/{self.slug}/orders", json=payload, catch_response=True, name="/orders (Create)") as response:
            if response.status_code == 201:
                response.success()
            elif response.status_code == 404:
                response.failure("Produto/Loja não encontrado (Seed necessário)")
            else:
                response.failure(f"Erro {response.status_code}: {response.text}")

    @task(1)
    @tag('admin')
    def admin_flow(self):
        """Simula fluxo administrativo (Login + Dashboard)."""
        # Login apenas se não tiver token
        if not self.token:
            res = self.client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"}, name="/auth/token")
            if res.status_code == 200:
                self.token = res.json()["access_token"]
            else:
                return # Falha no login, aborta task

        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Dashboard (Pesado - Agregação)
        self.client.get("/api/admin/metrics", headers=headers, name="/admin/metrics")
        
        # KDS (Lista de Pedidos)
        self.client.get(f"/api/admin/{self.slug}/orders", headers=headers, name="/admin/orders")
