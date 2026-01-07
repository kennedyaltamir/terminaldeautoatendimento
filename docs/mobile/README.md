# 📱 MesaFlow Mobile - Documentação Mestre

## 1. Status Atual: Fase 10 (KDS Nativo)
O aplicativo mobile evoluiu de um protótipo para um **Terminal de Operação Ativa**. 

### Marcos Alcançados:
- **Infraestrutura:** Autenticação semântica, interceptores de refresh e barreira de renderização (AuthGate).
- **Realtime:** Sincronização via WebSocket com reconciliação de estado.
- **Inteligência:** Motor de SLA determinístico e Engine de Alertas Sensoriais (Vibração) com controle de cooldown.
- **Identidade:** Bootstrap de sessão dinâmico baseado em claims de JWT.

## 2. Arquitetura de Atenção (Missão 21/22)
O app utiliza um **Global Clock** (pulso de 5s) para orquestrar:
1. Atualização de timers de pedidos.
2. Re-cálculo de status de SLA (OK, WARNING, CRITICAL, BREACHED).
3. Re-ordenação da fila por prioridade.
4. Disparo de alertas físicos (Vibração) conforme a política de interrupção.

## 3. Backlog de Missões Pendentes
- **Missão 23:** Controles do Operador (Silent Mode).
- **Missão 24:** Resiliência de Rede (Exponential Backoff & Re-sync).
- **Missão 25:** Gestão de Erros Operacionais.
- **Missão 26:** Observabilidade (Logs estruturados).
- **Missão 27:** Polimento de UX e Release.

---
*Versão 1.5 — Janeiro de 2026*
