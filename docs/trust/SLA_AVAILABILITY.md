# ⏱️ Acordo de Nível de Serviço (SLA) e Disponibilidade

**Vigência:** Janeiro de 2026
**Aplicabilidade:** Clientes Planos Pro e Enterprise

## 1. Compromisso de Disponibilidade
O MesaFlow garante uma disponibilidade mensal de **99,9%** (três noves) para os Serviços Essenciais.

### Definição de Disponibilidade
O serviço é considerado indisponível se o endpoint de monitoramento externo (`/health`) retornar erro (5xx) ou timeout (> 5s) por mais de 2 minutos consecutivos.

## 2. Cálculo de SLA
$$
\text{Disponibilidade Mensal} = \left( \frac{\text{Minutos Totais no Mês} - \text{Minutos de Indisponibilidade}}{\text{Minutos Totais no Mês}} \right) \times 100
$$

*Excluem-se do cálculo:*
- Janelas de Manutenção Programada (com aviso prévio de 24h).
- Falhas de Força Maior (Desastres Naturais, Ataques DDoS massivos fora do controle da mitigação).
- Falhas na infraestrutura do Cliente (Internet local, Hardware).

## 3. Política de Crédito (SLA Breach)
Em caso de descumprimento do SLA, o cliente elegível receberá créditos na fatura seguinte conforme a tabela:

| Disponibilidade Mensal | Crédito (% da Mensalidade) |
| :--- | :--- |
| **99.0% – 99.89%** | 10% |
| **95.0% – 98.99%** | 25% |
| **< 95.0%** | 100% (Mês Gratuito) |

## 4. Monitoramento e Auditoria
A disponibilidade é medida por sondas externas (Synthetic Monitoring) a partir de múltiplas geolocalizações (Latam, US, EU). Os relatórios de uptime estão disponíveis sob demanda para auditoria no Trust Center.