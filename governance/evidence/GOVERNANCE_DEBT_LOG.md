# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-15 13:10:00
# 📓 Log de Dívida Técnica e Hardening Futuro

## 1. WebSocket Protocol (High Priority)
- **Dívida:** O payload atual é "flat" e não versionado.
- **Risco:** Incompatibilidade entre versões do App Mobile e Backend durante deploys.
- **Ação Futura:** Implementar envelope padrão `{ type: string, payload: object, v: number }`.

## 2. Geofencing & Map Projection (RESOLVIDO)
- **Dívida Anterior:** O mapa do cliente utilizava translação linear baseada em offsets fixos.
- **Solução:** Implementado Leaflet.js com OSRM para projeção geográfica real (L6.22).

## 3. WhatsApp Fail-Open (Low Priority)
- **Dívida:** O sistema ignora falhas de conexão com o provedor de mensagens.
- **Risco:** O lojista pode não ser notificado de falhas reais na sua conta de mensageria.
- **Ação Futura:** Implementar fila de retry persistente (Celery/Redis) para notificações falhas.

---
*MesaFlow Kernel L6.22 — Technical Oversight.*

