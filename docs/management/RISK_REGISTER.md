# ⚠️ Matriz de Riscos (Risk Register)

Este documento monitora ameaças potenciais ao sucesso do MesaFlow e define planos de mitigação.

| ID | Risco | Probabilidade | Impacto | Severidade | Plano de Mitigação | Status |
|:---|:---|:---:|:---:|:---:|:---|:---|
| **R01** | **Queda de Conectividade no Cliente** | Alta | Crítico | 🔥 EXTREMA | Implementação de arquitetura Offline-First (Dexie.js) e fila de sincronização assíncrona. | ✅ Mitigado |
| **R02** | **Indisponibilidade da SEFAZ** | Média | Alto | ALTA | Sistema de contingência offline para emissão de notas e retry automático. | ✅ Mitigado |
| **R03** | **Vazamento de Dados entre Tenants** | Baixa | Crítico | 🔥 EXTREMA | RLS (Row Level Security) lógico obrigatório em todas as queries e testes de IDOR automatizados. | ✅ Mitigado |
| **R04** | **Bloqueio de WhatsApp (Meta)** | Média | Médio | MÉDIA | Uso de API oficial (ou provedores robustos como Evolution) e rotação de números/instâncias. | 🔄 Monitorando |
| **R05** | **Latência em Horário de Pico** | Média | Alto | ALTA | Cache L2 (Redis) para cardápio público e otimização de queries SQL. | ✅ Mitigado |
| **R06** | **Fraude em Pagamentos (Chargeback)** | Baixa | Médio | MÉDIA | Uso de 3DSecure e análise de risco dos gateways (Stripe/MP). | 🔄 Monitorando |
| **R07** | **Dependência de Terceiros (iFood)** | Alta | Alto | ALTA | Arquitetura de Polling resiliente e tratamento de erros de API externa. | ✅ Mitigado |
| **R08** | **Obsolescência Tecnológica Mobile** | Média | Médio | MÉDIA | Uso de Expo Managed Workflow para facilitar upgrades de SDK (ex: SDK 54). | ✅ Mitigado |

## Legenda
- **Probabilidade:** Baixa (<20%), Média (20-60%), Alta (>60%).
- **Impacto:** Baixo (Incômodo), Médio (Funcionalidade parcial), Alto (Parada), Crítico (Perda financeira/legal).
