# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-15 13:05:00
# 🗺️ Relatório de Integração: Motor Geográfico (Leaflet + OSRM)

## 1. Mudança de Paradigma
O sistema de rastreamento foi migrado de uma simulação cinemática (CSS transforms) para uma projeção geográfica real utilizando a biblioteca Leaflet.

## 2. Componentes Implementados
- **Backend Protocol V1:** WebSocket emite `DELIVERY_LOCATION` com payload `{order_id, lat, lng}`.
- **Map Engine:** `TrackingMap.tsx` centraliza a lógica do Leaflet e React-Leaflet.
- **Routing Service:** Integração com o OSRM (Open Source Routing Machine) para exibição de trajetos reais.

## 3. Veredito de UX
- **Entregador:** Possui visão ativa e controle do mapa para navegação.
- **Cliente:** Possui visão passiva e focada na chegada, com interface read-only para garantir segurança operacional.

---
*Assinado: Optimus Kernel L6*

