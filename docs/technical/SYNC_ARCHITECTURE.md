# 🔄 Arquitetura de Sincronização Unificada

## 1. Banco de Dados Único
Todas as interfaces (Site, Admin, App Garçom, KDS, App Driver) conectam-se ao mesmo cluster **PostgreSQL (Neon.tech)**. 
- **Isolamento:** Garantido via `company_id` em todas as tabelas.
- **Consistência:** Transações ACID garantem que um pedido nunca seja duplicado ou perdido entre as telas.

## 2. Estratégia de Autenticação (Single Sign-On)
- **JWT:** O token gerado no login é universal. 
- **Claims:** O payload do token contém:
    - `company_id`: Para RLS (Row Level Security).
    - `role`: Para autorização de interface (ex: `kitchen` não abre o `financial`).
- **Sessão:** Mobile utiliza `SecureStore` para persistência longa, enquanto Web utiliza `Cookies/LocalStorage`.

## 3. Comunicação em Tempo Real (The Pulse)
- **Broker:** Redis Pub/Sub.
- **Fluxo:**
    1. Cliente faz pedido -> API grava no DB -> API publica no Redis.
    2. WebSocket Server (FastAPI) escuta o Redis.
    3. WebSocket envia o JSON para o KDS e App do Garçom simultaneamente.
- **Latência Alvo:** < 200ms entre o clique do cliente e o som no KDS.

## 4. Offline-First (Mobile)
- **Persistência Local:** Apps mobile utilizam uma camada de cache para permitir visualização de dados sem rede.
- **Queue:** Pedidos feitos offline são enfileirados e sincronizados automaticamente via worker assim que a conexão `ping` retornar sucesso.
