# 📱 Task 27: Observabilidade & Diagnóstico Operacional

## 1. Contexto
Implementação da camada de inteligência de logs para o App Mobile. Em operações críticas de cozinha, falhas silenciosas são o pior cenário. O sistema agora registra eventos vitais, permitindo auditoria técnica e suporte proativo.

## 2. Decisões Técnicas
- **Structured Logging:** Criação do `LoggerService` com suporte a níveis de severidade e contextos nomeados.
- **Instrumentação:**
    - **Realtime:** Logs de abertura, fechamento, erro e reconexão de WebSockets.
    - **Sync:** Rastreio de início e fim de reconciliação de estado.
    - **Data:** Registro de payloads de eventos recebidos (em modo DEBUG).
- **Singleton Pattern:** O Logger é uma instância única para garantir consistência de timestamps e configuração global.
- **Environment Awareness:** Logs de nível `DEBUG` são automaticamente suprimidos em builds de produção para economizar recursos.

## 3. Arquivos Afetados
- `mobile/src/services/logger.service.ts` (Novo)
- `mobile/src/services/orders.realtime.service.ts` (Instrumentação)
- `mobile/src/services/orders.sync.service.ts` (Instrumentação)

## 4. Política de Testes
[TEST_EXEMPT: Serviço de log puro. Validação via console do Metro/Debugger: 1. Abrir o app. 2. Verificar logs de boot e conexão. 3. Simular erro de rede e verificar log de erro estruturado.]

---
*Fase 10 — Janeiro de 2026*
