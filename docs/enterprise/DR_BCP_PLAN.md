# 🛡️ Plano de Continuidade de Negócios e Recuperação de Desastres (BCP/DRP)

**Classificação:** CONFIDENCIAL (Uso Interno & Auditores)
**Versão:** 1.0
**Data de Emissão:** Janeiro de 2026
**Responsável:** CTO / Comitê de Crise

---

## 1. Objetivo e Escopo
Este documento estabelece as diretrizes, procedimentos e responsabilidades para garantir a continuidade das operações críticas do **MesaFlow** em caso de interrupções severas ou desastres.

O plano cobre:
- Infraestrutura Tecnológica (Cloud, Dados, Rede).
- Processos Operacionais Críticos (Pedidos, Pagamentos).
- Comunicação de Crise.

---

## 2. Métricas de Recuperação (SLA de Continuidade)

Definimos os seguintes objetivos para serviços críticos (Tier 1):

| Serviço | RTO (Tempo Máx. de Parada) | RPO (Perda Máx. de Dados) |
| :--- | :---: | :---: |
| **Processamento de Pedidos** | 4 Horas | 5 Minutos |
| **KDS (Cozinha)** | 4 Horas | 5 Minutos |
| **Banco de Dados (Core)** | 2 Horas | 1 Minuto (PITR) |
| **Painel Administrativo** | 8 Horas | 1 Hora |

* **RTO (Recovery Time Objective):** Tempo alvo para restaurar o serviço após o desastre.
* **RPO (Recovery Point Objective):** Máximo de dados perdidos aceitável (janela de backup).

---

## 3. Cenários de Desastre e Estratégias

### 3.1 Falha Crítica de Banco de Dados (Neon.tech)
- **Risco:** Corrupção de dados, deleção acidental ou indisponibilidade da região AWS.
- **Estratégia:** Point-in-Time Recovery (PITR).
- **Procedimento:**
    1. Acionar `docs/sre/RUNBOOK_DATABASE_FAILOVER.md`.
    2. Restaurar backup para nova instância (Time Travel).
    3. Atualizar DNS/Env Vars da aplicação.

### 3.2 Indisponibilidade do Provedor de Aplicação (Render)
- **Risco:** Queda massiva da região Oregon ou falha de deploy.
- **Estratégia:** Redeploy em Provedor Secundário (Vercel/AWS) ou Região Alternativa.
- **Procedimento:**
    1. Ativar pipeline de CI/CD para ambiente de DR.
    2. Redirecionar DNS (Cloudflare) para o novo endpoint.

### 3.3 Falha de Serviços de Terceiros (Dependências)
- **Redis (Cache/PubSub):** Fallback automático para memória local (degradação graciosa). Ver `docs/sre/RUNBOOK_REDIS_OUTAGE.md`.
- **iFood/WhatsApp:** Fila de retry exponencial e notificação de atraso no painel.

---

## 4. Procedimentos de Backup

| Ativo | Frequência | Retenção | Tipo | Armazenamento |
| :--- | :--- | :--- | :--- | :--- |
| **PostgreSQL** | Contínuo (WAL) | 7 Dias | Incremental | AWS S3 (Gerenciado Neon) |
| **Código Fonte** | Real-time | Indefinido | Git | GitHub (Distribuído) |
| **Logs de Auditoria** | Real-time | 5 Anos | Append-only | Banco Dedicado / S3 |

---

## 5. Equipe de Resposta a Incidentes (IRT)

Em caso de desastre nível SEV1 (Parada Total), a seguinte cadeia de comando é ativada:

1.  **Comandante do Incidente (IC):** CTO (Decisão final, comunicação externa).
2.  **Líder de Operações:** Tech Lead (Execução técnica, acesso root).
3.  **Líder de Comunicação:** CS Head (Notificação de clientes, Status Page).

**Matriz de Escalonamento:**
- **T+0m:** Detecção (Sentry/UptimeRobot).
- **T+15m:** War Room aberto. IC assume.
- **T+30m:** Notificação na Status Page (Investigando).
- **T+1h:** Decisão de Failover (Ativar DR).

---

## 6. Testes e Manutenção
Este plano deve ser testado e revisado anualmente.

- **Tabletop Exercise:** Simulação teórica com a liderança (Semestral).
- **Failover Test:** Restauração de backup em ambiente de staging (Trimestral).
- **Revisão de Documentação:** Após cada incidente real ou mudança de arquitetura.

---
*Documento confidencial. A cópia não autorizada é proibida.*
