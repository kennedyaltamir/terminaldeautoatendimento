### 1️⃣ `docs/API.md` (A Prioridade: Agora com Payloads Reais)

Transformei de uma "lista de links" para uma **especificação de contrato**.

```markdown
# 🔌 API Reference

Documentação técnica dos endpoints do MesaFlow.
**Base URL:** `https://api.mesaflow.com.br` (Prod) ou `http://localhost:8000` (Dev)

---

## 1. Contexto Público (Cliente Final)
*Não requer autenticação. O contexto é definido pelo `slug` da empresa na URL.*

### 🍔 Obter Cardápio
Retorna a estrutura completa de categorias e produtos ativos.

**GET** `/api/{company_slug}/menu`

**Response (200 OK):**
```json
{
  "company": {
    "name": "Hamburgueria do Zé",
    "is_open": true
  },
  "categories": [
    {
      "id": 1,
      "name": "Lanches",
      "products": [
        {
          "id": 101,
          "name": "X-Bacon",
          "description": "Pão, carne 180g, queijo e bacon.",
          "price": 25.90,
          "image_url": "https://cdn.mesaflow.../xbacon.jpg"
        }
      ]
    }
  ]
}
```

---

### 🛒 Criar Pedido
Envia o carrinho para a cozinha. Requer validação do token da mesa.

**POST** `/api/{company_slug}/orders`

**Payload (Request Body):**
```json
{
  "table_id": 5,
  "qr_token": "a1b2c3d4-token-rotativo",
  "customer_name": "João Silva",
  "items": [
    {
      "product_id": 101,
      "quantity": 2,
      "notes": "Sem cebola, ponto bem passado"
    },
    {
      "product_id": 205,
      "quantity": 1,
      "notes": null
    }
  ]
}
```

**Response (201 Created):**
```json
{
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Pedido enviado para a cozinha!",
  "estimated_time": "15-20 min"
}
```

**Erros Comuns:**
*   `404 Not Found`: Empresa ou Mesa não encontrada.
*   `400 Bad Request`: `qr_token` inválido ou expirado (Anti-troll).
*   `422 Unprocessable Entity`: Produto indisponível ou payload malformado.

---

### 🔍 Consultar Status
Polling para o frontend saber quando o pedido ficou pronto.

**GET** `/api/orders/{order_id}/status`

**Response (200 OK):**
```json
{
  "status": "preparing", 
  "updated_at": "2025-01-01T12:30:45Z"
}
```
*(Status possíveis: pending, accepted, preparing, ready, delivered, canceled)*

---
## 2. Contexto Admin (Dono/Cozinha)
*Requer Header `Authorization: Bearer <JWT_TOKEN>` (Futuro)*

### 👨‍🍳 Listar Pedidos (KDS)
Retorna a fila de pedidos para a cozinha, incluindo detalhes dos itens e da mesa.

**GET** `/api/admin/{company_slug}/orders`

**Response (200 OK):**
```json
[
  {
    "id": "db7c4eb2-94fe-4850-9c67-e32bdbf28c0f",
    "status": "pending",
    "total_amount": 63.8,
    "customer_name": "Kennedy",
    "created_at": "2025-12-31T04:55:26.705283-03:00",
    "table": {
      "table_number": 1,
      "qr_token": "token-seguro-mesa-1"
    },
    "items": [
      {
        "quantity": 2,
        "notes": "Bem passado",
        "product": {
          "name": "X-Bacon Supremo",
          "image_url": "https://placehold.co/..."
        }
      },
      {
        "quantity": 1,
        "notes": "Com gelo",
        "product": {
          "name": "Coca-Cola Lata"
        }
      }
    ]
  }
]
```

### ✅ Atualizar Status
Muda o estado do pedido (ex: Cozinha aceita o pedido).

**PATCH** `/api/admin/orders/{order_id}`

**Payload:**
```json
{
  "status": "preparing"
}
```
```

---

### 2️⃣ `README.md` (Ajustado com Público e Fluxo)

Adicionei o diagrama mental e o público-alvo, conforme solicitado.

```markdown
# 🚀 MesaFlow

> **Sistema Operacional de Autoatendimento para Food Service.**
> Transforme mesas em pontos de venda inteligentes. Sem filas, sem apps, sem espera.

## 🎯 Público-Alvo
Este software foi desenhado para:
*   🍔 **Hamburguerias e Lanchonetes** (Giro rápido de mesas).
*   🍺 **Bares e Pubs** (Redução de garçons apenas para anotar cerveja).
*   🍕 **Pizzarias** (Cardápio digital com adicionais complexos).
*   📉 **Negócios que buscam eficiência** operacional e redução de erros.

## 🧠 Como Funciona (Fluxo Mental)

```mermaid
[Cliente Escaneia QR] -> [Abre Cardápio Web] -> [Monta Pedido] -> [Envia]
                                                                    ⬇
                                                            [API Valida Token]
                                                                    ⬇
                                                            [Tela da Cozinha (KDS) Toca Som]
                                                                    ⬇
                                                            [Garçom Entrega]
```

## 🛠️ Tech Stack
*   **Backend:** Python (FastAPI) + SQLAlchemy.
*   **Database:** PostgreSQL (Essencial para integridade relacional).
*   **Infra:** Docker Ready.

## 🚀 Como Rodar Localmente

1.  **Clone e entre na pasta:**
    ```bash
    git clone https://github.com/seu-user/mesaflow.git
    cd mesaflow
    ```

2.  **Configure as Variáveis:**
    Copie o exemplo para o arquivo real.
    ```bash
    cp .env.example .env
    ```
    *Edite o `.env` se não for usar o Docker padrão.*

3.  **Suba a Infraestrutura (Recomendado):**
    Isso subirá o PostgreSQL e a API prontos para uso.
    ```bash
    docker-compose up --build
    ```

4.  **Acesse:**
    *   Docs Interativos: `http://localhost:8000/docs`
    *   API Root: `http://localhost:8000`

## 📄 Licença
Proprietária. Todos os direitos reservados.
```

---
