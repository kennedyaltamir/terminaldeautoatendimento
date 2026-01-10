# 🚦 MesaFlow Status Page

**URL Pública:** `https://status.mesaflow.com.br` (Alias para Provedor Externo)
**Monitoramento:** Externo (Synthetic Probe)
**Frequência de Checagem:** 60 segundos

## Visão Geral
A página de status do MesaFlow é a fonte única da verdade sobre a disponibilidade dos nossos serviços. Ela é hospedada externamente à nossa infraestrutura para garantir comunicação mesmo em caso de falha total do datacenter principal.

## Componentes Monitorados

| Componente | Endpoint de Prova | Critério de Sucesso | Impacto |
| :--- | :--- | :--- | :--- |
| **API Gateway** | `GET /health` | HTTP 200 + JSON `{"status": "healthy"}` | Crítico (Parada Total) |
| **Banco de Dados** | `Internal Check` | Conexão TCP + Query `SELECT 1` | Crítico (Erro 500) |
| **Real-time (Redis)** | `Internal Check` | Ping/Pong Latency < 100ms | Alto (KDS não atualiza) |
| **Webhooks (Inbound)** | `POST /api/webhooks/*` | HTTP 200/400 (Não 5xx) | Médio (Atraso em integrações) |

## Política de Incidentes
1.  **Investigando:** Detectada anomalia automática ou reporte de cliente.
2.  **Identificado:** Causa raiz encontrada, correção em andamento.
3.  **Monitorando:** Correção aplicada, observando estabilidade.
4.  **Resolvido:** Serviço operando normalmente.

## Subscrição
Clientes Enterprise podem assinar notificações via:
- E-mail
- SMS
- Webhook (para automação de NOC)
- 