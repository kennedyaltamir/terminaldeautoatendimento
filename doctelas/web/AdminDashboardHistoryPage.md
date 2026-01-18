# 📜 AdminDashboardHistoryPage
> **Plataforma:** WEB | **Domínio:** AUDITORIA | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Esta tela fornece uma trilha de auditoria completa e retroativa de todas as transações e mudanças de estado do sistema. É a ferramenta principal para resolução de disputas financeiras, conferência de fechamento de caixa e análise de performance histórica de longo prazo.

## 2. Estrutura e Componentes Técnicos
- **Data Table Engine:** Tabela de alta densidade com suporte a paginação server-side para lidar com milhares de registros sem degradação de performance.
- **Filtros Avançados:** Painel lateral ou superior para filtragem por Status (Pago, Cancelado), Período (Date Range Picker) e Origem (MesaFlow, iFood).
- **Order Detail Modal:** Componente de visualização profunda que exibe itens, taxas, descontos e logs de tempo de cada etapa do pedido.

## 3. Elementos Interativos
- **Paginação Dinâmica:** Controles de "Anterior/Próximo" que atualizam a URL via query params para permitir compartilhamento de links de busca.
- **Visualizador de Recibo:** Botão para re-emitir ou visualizar o cupom térmico original do pedido.
- **Exportador de Auditoria:** Função para gerar relatórios consolidados em PDF ou CSV para contabilidade.

## 4. Regras de Negócio e Integridade
- **Imutabilidade:** Pedidos finalizados ou cancelados não podem ser editados, apenas visualizados.
- **Sincronia de Status:** O histórico reflete o estado final persistido no banco de dados, servindo como "Fonte da Verdade" em caso de divergência no KDS.
- **Cálculo de Taxas:** Exibição clara do split de comissão e taxas de entrega aplicadas no momento da venda.

## 5. Estados da Interface
- **Searching:** Estado de carregamento com Skeletons de linha durante a filtragem.
- **No Results:** Feedback visual amigável quando nenhum pedido atende aos critérios de busca.
- **API Error:** Alerta de falha de comunicação com opção de recarregamento manual.

## 6. Documentação de API
- **Endpoint Principal:** `GET /api/admin/{slug}/history?page=1&limit=10&status=paid`
- **Contrato de Resposta:** Objeto `OrderPagination` contendo metadados de totalização e array de `OrderResponse`.

---
*MesaFlow OS — Auditoria e Transparência.*
# 📜 AdminDashboardHistoryPage
> **Plataforma:** WEB | **Domínio:** AUDITORIA | **Status:** SEALED (100%)

## 1. Visão Geral e Propósito
Trilha de auditoria retroativa. Permite a conferência de todos os pedidos realizados, servindo como base para fechamento de caixa.

## 2. Estrutura e Layout (Componentes)
- **History Table:** Lista paginada de pedidos finalizados.
- **Filter Panel:** Busca por data, status e método de pagamento.

## 3. Interações e Ações (Botões)
- **View Details:** Abre modal com composição completa do pedido.
- **Export Data:** Gera relatório consolidado do período.

## 4. Estados e Cenários (Loading/Error)
- **Loading:** Skeletons de linha durante o fetch.
- **No Results:** Feedback para busca sem ocorrências.

## 5. Fluxo de Navegação
1. Seleção de período.
2. Localização de pedido específico.
3. Conferência de itens e valores.

## 6. Documentação Técnica (API)
- **Endpoints:** `GET /api/admin/{slug}/history`
- **Assets:** ![History Preview](https://raw.githubusercontent.com/mesaflow/assets/main/screenshots/admin-history-full.png)
