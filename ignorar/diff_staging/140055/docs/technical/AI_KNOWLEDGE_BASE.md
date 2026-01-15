# 🧠 MesaFlow AI Knowledge Base
**Status:** ACTIVE | **Maturity:** L6.9

--- ENTRY: 2026-01-15T14:15:00 ---
**CONTEXT:** Full Loop Simulation (Customer -> Kitchen -> Driver).
**DECISION:** Utilização de Playwright para fluxos de UI e `requests` para injeção de telemetria GPS.
**LEARNING:** A simulação de GPS via API é mais estável que tentar manipular a geolocalização do navegador em tempo real para testes de longa duração. O uso de `bring_to_front()` no Playwright permite alternar o foco visual entre as personas (Cliente/Entregador) durante a demonstração.
**STATUS:** Script `full_order_simulation.py` validado.
