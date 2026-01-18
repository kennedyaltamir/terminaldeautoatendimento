# 🟢 TrustStatusPage
> **Plataforma:** WEB | **Domínio:** OBSERVABILIDADE | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Monitor de saúde do sistema em tempo real. Fornece aos lojistas e desenvolvedores a confirmação visual de que todos os subsistemas (API, Banco, Real-time) estão operacionais, reduzindo chamados de suporte durante instabilidades globais.

## 2. Estrutura e Componentes (Real-time)
- **Global Status Indicator:** Banner principal (Verde/Amarelo/Vermelho) com o estado geral do ecossistema.
- **Service Health Grid:** Lista individual de componentes:
  - **API Gateway:** Latência e disponibilidade.
  - **Database Engine:** Conectividade do banco relacional.
  - **Real-time Broker:** Status do Redis e WebSockets.
- **Uptime History:** Gráfico de barras dos últimos 90 dias de operação.

## 3. Elementos Interativos
- **Manual Refresh:** Botão para forçar uma nova verificação de saúde.
- **Incident History:** Lista cronológica de manutenções programadas e incidentes passados com resoluções.
- **Subscribe to Alerts:** Opção para receber notificações de status via e-mail ou webhook.

## 4. Regras de Monitoramento
- **Healthcheck Endpoint:** Consome a rota `/api/health` do backend.
- **Polling Frequency:** Atualização automática a cada 30 segundos.
- **Fail-Open Logic:** Se o monitor falhar ao conectar, ele reporta "Status Desconhecido" em vez de "Operacional".

## 5. Estados da Interface
- **Healthy:** Todos os serviços em verde.
- **Degraded:** Um ou mais serviços com latência alta ou falhas parciais.
- **Outage:** Falha crítica em componentes core (API ou DB).

## 6. Integração Técnica
- **Backend:** `GET /api/health` retorna JSON com status de cada serviço.
- **Frontend:** Utiliza SWR com revalidação em foco para garantir dados frescos.

---
*MesaFlow Status — Transparência em tempo real.*
# 🟢 TrustStatusPage
> **Plataforma:** WEB | **Domínio:** OBSERVABILIDADE | **Status:** SEALED (100%)

## 1. Visão Geral e Propósito
Monitor de disponibilidade pública. Prova a estabilidade do sistema através de métricas reais de uptime.

## 2. Estrutura e Layout (Componentes)
- **Live Vitals:** Status individual de API, DB e Redis.
- **Uptime Calendar:** Histórico visual dos últimos 90 dias.

## 3. Interações e Ações (Botões)
- **Refresh Health:** Força nova checagem de sinais vitais.
- **Subscribe:** Cadastro para alertas.

## 4. Estados e Cenários (Loading/Error)
- **Operational:** Tudo verde.
- **Major Outage:** Alerta vermelho para serviços offline.

## 5. Fluxo de Navegação
1. Acesso via Trust Center.
2. Consulta de status.
3. Verificação de histórico.

## 6. Documentação Técnica (API)
- **Endpoints:** `GET /api/health`
- **Assets:** ![Status Preview](https://raw.githubusercontent.com/mesaflow/assets/main/screenshots/status-full.png)
