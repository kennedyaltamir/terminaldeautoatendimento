# 🛵 Módulo: Operações de Campo (Garçom & Entregador)
**Rotas:** `/admin/[slug]/waiter` | `/admin/[slug]/driver`

## 1. App do Garçom (POS)
- **Intenção:** Agilidade no atendimento de mesa.
- **Elementos:**
    - **Table Grid:** Status visual das mesas (Livre, Ocupada, Alerta).
    - **Quick Search:** Busca de produtos por nome ou código.
    - **Payment Modal:** Seleção de método e cálculo de troco.
- **Comportamento:** Sincronia via WebSocket para chamados de ajuda.

## 2. App do Entregador (Logística)
- **Intenção:** Gestão de rotas e confirmação de entrega.
- **Elementos:**
    - **Delivery List:** Pedidos prontos para despacho.
    - **Map View:** Integração com Google Maps/Waze.
    - **POD Input:** Campo para digitar o código de confirmação do cliente.
- **Comportamento:** Captura coordenadas GPS em background durante a rota.
