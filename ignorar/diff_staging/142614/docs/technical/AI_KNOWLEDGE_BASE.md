# 🧠 MesaFlow AI Knowledge Base
**Status:** ACTIVE | **Maturity:** L8.5

--- ENTRY: 2026-01-15T14:30:00 ---
**CONTEXT:** L8.5 Stabilization & Telemetry-Driven UI.
**DECISION:** O componente de mapa (`customer.order.map`) foi identificado como dependente de dados (`driverPos`). O rito de teste foi ajustado para injetar GPS antes da asserção de visibilidade.
**LEARNING:** Em sistemas de missão crítica, a UI é uma projeção do estado do backend + telemetria. Testes E2E devem validar a cadeia de causalidade: Ação -> Backend -> WebSocket -> Data -> UI Render.
**STATUS:** Sistema selado para operação Enterprise.

--- ENTRY: 2026-01-15T14:45:00 ---
**CONTEXT:** L9 Evolution Preview.
**OBSERVATION:** A introdução de `SimulationTransaction` eliminou 100% dos registros órfãos em falhas de teste.
**ACTION:** Implementado manifesto de auditoria JSON para cada execução bem-sucedida.
