# 🔌 Estratégia de Integração Mobile

## 1. Fluxo de Comunicação
O App Mobile comunica-se com o Backend (FastAPI) através de dois canais principais:
- **REST API:** Para operações de CRUD, autenticação e consultas.
- **WebSockets (Redis):** Para eventos em tempo real (Novos pedidos no KDS, localização do motorista).

## 2. Contratos de Dados
O App deve ser um **consumidor estrito** dos Schemas Pydantic definidos no backend.
- Reuso total dos endpoints de `/api/public` e `/api/admin`.
- Implementação de **API Versioning** no Header para garantir compatibilidade durante deploys.

## 3. Estratégia de Autenticação
- **JWT (JSON Web Token):** Utilização de Access e Refresh Tokens.
- **Persistência:** Armazenamento seguro via `Expo SecureStore`.
- **Refresh Automático:** Interceptor no Axios para renovação de sessão sem interrupção da UI.

## 4. Diagrama Lógico
`[App Mobile] <--> [Nginx/Load Balancer] <--> [FastAPI Gateway] <--> [PostgreSQL / Redis]`
