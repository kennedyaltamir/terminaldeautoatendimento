# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-15 10:00:00
# 📓 Log de Dívida Técnica e Hardening Futuro

Este documento rastreia decisões de engenharia tomadas para agilidade de entrega que devem ser revisitadas para escala global.

## 1. WebSocket Protocol (High Priority)
- **Dívida:** O payload atual é "flat" e não versionado.
- **Risco:** Incompatibilidade entre versões do App Mobile e Backend durante deploys.
- **Ação Futura:** Implementar envelope padrão `{ type: string, payload: object, v: number }`.

## 2. Geofencing & Map Projection (Medium Priority)
- **Dívida:** O mapa do cliente utiliza translação linear baseada em offsets fixos.
- **Risco:** Falha de renderização em localizações fora do range de Pompéu/MG ou em viewports não padronizados.
- **Ação Futura:** Integrar biblioteca de projeção (Leaflet/MapLibre) para suporte a coordenadas reais sobre tiles de mapa.

## 3. WhatsApp Fail-Open (Low Priority)
- **Dívida:** O sistema ignora falhas de conexão com o provedor de mensagens.
- **Risco:** O lojista pode não ser notificado de falhas reais na sua conta de mensageria.
- **Ação Futura:** Implementar fila de retry persistente (Celery/Redis) para notificações falhas.

---
*MesaFlow Kernel L6.22 — Technical Oversight.*
