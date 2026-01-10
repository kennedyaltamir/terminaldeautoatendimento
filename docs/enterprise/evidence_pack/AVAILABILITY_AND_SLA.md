# ⏱️ Disponibilidade e Acordo de Nível de Serviço (SLA)

## 1. Compromisso de Nível de Serviço
O MesaFlow compromete-se com um **Uptime Mensal de 99,9%** para os serviços críticos da plataforma.

### Serviços Cobertos
- API de Processamento de Pedidos.
- Sistema de KDS (Cozinha) em Tempo Real.
- Gateway de Pagamentos.

## 2. Monitoramento e Transparência
- **Status Page:** Disponibilizamos uma página pública de status (`/trust/status`) monitorada por sondas externas independentes.
- **Health Check:** Endpoint público `/health` para verificação automatizada por Load Balancers e sistemas de monitoramento do cliente.

## 3. Janelas de Manutenção
- **Programadas:** Comunicadas com antecedência mínima de 24 horas. Realizadas preferencialmente fora do horário de pico (03:00 - 05:00 BRT).
- **Emergenciais:** Comunicadas imediatamente através dos canais de suporte e Status Page.

## 4. Plano de Continuidade de Negócios (BCP)
- **RTO (Recovery Time Objective):** 4 horas para restauração completa de serviços críticos.
- **RPO (Recovery Point Objective):** 5 minutos (perda máxima de dados em caso de desastre).
- **Backup:** Rotinas de backup contínuo (Point-in-Time Recovery) com retenção de 7 dias.

## 5. Suporte Enterprise
- **Canais:** E-mail dedicado, Portal de Chamados e WhatsApp (para incidentes críticos).
- **Tempos de Resposta:**
    - **Crítico (P1):** < 1 hora (24/7).
    - **Alto (P2):** < 4 horas (Horário Comercial).
    - **Normal (P3):** < 1 dia útil.
