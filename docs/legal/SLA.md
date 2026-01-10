# Acordo de Nível de Serviço (SLA)

Este documento define os compromissos de disponibilidade e suporte técnico da plataforma MesaFlow para clientes dos planos **Pro** e **Enterprise**.

## 1. Disponibilidade do Serviço (Uptime)

O MesaFlow garante uma disponibilidade mensal de **99,9%** para os serviços críticos.

### Serviços Críticos
- API de Pedidos (`POST /orders`)
- KDS em Tempo Real (WebSockets)
- Processamento de Pagamentos

### Cálculo de Uptime
O tempo de atividade é calculado mensalmente, excluindo-se janelas de manutenção programada.

## 2. Janelas de Manutenção

Manutenções programadas que possam causar indisponibilidade serão comunicadas com antecedência mínima de 24 horas via painel administrativo ou e-mail.

- **Horário Preferencial:** Entre 03:00 e 05:00 (Horário de Brasília).
- **Duração Máxima:** 2 horas por janela.

## 3. Suporte Técnico

| Severidade | Definição | Tempo de Resposta (SLA) | Canal |
| :--- | :--- | :--- | :--- |
| **Nível 1 (Crítico)** | Sistema totalmente inoperante. Loja parada. | < 1 hora (24/7) | WhatsApp Emergência |
| **Nível 2 (Alto)** | Funcionalidade core falhando (ex: Impressão, Pix). | < 4 horas (Comercial) | Chat / E-mail |
| **Nível 3 (Médio)** | Dúvidas operacionais, bugs visuais não impeditivos. | < 1 dia útil | E-mail |
| **Nível 4 (Baixo)** | Sugestões de melhoria, dúvidas financeiras. | < 3 dias úteis | E-mail |

## 4. Compensação (SLA Breach)

Caso a disponibilidade mensal fique abaixo do garantido, o cliente terá direito a créditos na fatura seguinte:

- **99.0% - 99.8%:** 10% de desconto.
- **95.0% - 98.9%:** 25% de desconto.
- **Abaixo de 95%:** 100% de desconto (Mês grátis).

*Excluem-se falhas causadas por terceiros (ex: Queda da AWS, Mercado Pago fora do ar, falta de internet no restaurante).*