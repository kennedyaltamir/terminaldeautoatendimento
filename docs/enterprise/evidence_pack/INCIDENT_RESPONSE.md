# 🚨 Plano de Resposta a Incidentes

## 1. Classificação de Incidentes

| Nível | Descrição | Exemplo |
| :--- | :--- | :--- |
| **SEV-1 (Crítico)** | Indisponibilidade total ou vazamento de dados. | Banco de dados fora do ar, falha no login. |
| **SEV-2 (Alto)** | Degradação severa de funcionalidade core. | Falha no processamento de pagamentos, lentidão extrema. |
| **SEV-3 (Médio)** | Falha em funcionalidade não crítica. | Erro na geração de relatórios, bug visual. |
| **SEV-4 (Baixo)** | Dúvidas ou solicitações menores. | Dúvida sobre configuração, typo. |

## 2. Fluxo de Resposta

1.  **Detecção:** Alerta automático (Sentry/Monitoramento) ou reporte de cliente.
2.  **Triagem:** Classificação da severidade e atribuição do Comandante do Incidente (IC).
3.  **Contenção:** Ações imediatas para mitigar o impacto (ex: rollback de deploy, bloqueio de tráfego malicioso).
4.  **Comunicação:** Atualização da Status Page e notificação de clientes afetados (conforme SLA).
5.  **Resolução:** Correção da causa raiz e restauração do serviço.
6.  **Post-Mortem:** Análise do incidente, documentação da causa raiz e criação de ações preventivas (RCA).

## 3. Comunicação de Segurança
Incidentes de segurança que envolvam dados pessoais serão notificados aos controladores (clientes) e à autoridade competente (ANPD) dentro dos prazos legais estabelecidos pela LGPD, contendo:
- Natureza da violação.
- Categorias de dados afetados.
- Medidas de mitigação tomadas.
- Riscos potenciais.

## 4. Contatos
- **Reporte de Incidentes:** security@mesaflow.com.br
- **Plantão 24/7 (Crítico):** Disponível para clientes Enterprise via telefone dedicado.
