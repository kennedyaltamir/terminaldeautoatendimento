# 📋 AdminWaiterOrdersPage
> **Plataforma:** WEB | **Domínio:** OPERACIONAL | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Esta tela é o "Live Feed" de operações do salão. Seu objetivo é permitir que supervisores de garçons e gerentes de turno monitorem o fluxo de pedidos em tempo real, identifiquem gargalos de atendimento e realizem intervenções rápidas em comandas específicas sem a necessidade de estar fisicamente na mesa.

## 2. Estrutura e Layout (Monitor de Fluxo)
- **Active Orders Stream:** Lista cronológica de pedidos ativos com identificação visual por mesa e cliente.
- **Service Alert Sidebar:** Painel lateral dedicado a chamados de urgência (ajuda, limpeza, conta).
- **Quick Action Toolbar:** Botões de acesso rápido para cancelamento, estorno e transferência de itens.

## 3. Elementos Interativos
- **Filtro de Status:** Alternância entre pedidos "Pendentes", "Em Preparo" e "Prontos".
- **Busca por Comanda:** Localização instantânea de pedidos via ID ou nome do cliente.
- **Expandable Details:** Clique na linha para abrir a composição completa do pedido e histórico de tempo (SLA).

## 4. Regras de Negócio e Gestão
- **Ownership Tracking:** Identificação de qual funcionário realizou o lançamento original.
- **Audit Trail:** Registro de todas as alterações manuais feitas em pedidos ativos para prevenção de perdas.
- **Priority Highlighting:** Pedidos que excedem o tempo médio de preparo são destacados com bordas pulsantes.

## 5. Estados da Interface
- **Syncing:** Indicador de conexão ativa com o WebSocket.
- **Empty State:** Mensagem "Salão Tranquilo" quando não há pedidos em curso.
- **Action Loading:** Estado de bloqueio de linha enquanto uma alteração de status é processada.

## 6. Documentação Técnica (API)
- **Endpoints:** 
  - `GET /api/admin/{slug}/waiter/orders`
  - `PATCH /api/admin/orders/{id}`
- **WebSocket:** Assina o tópico `order_updates` para refletir mudanças feitas via App Mobile.

---
*MesaFlow OS — Operação de Salão de Alta Performance.*

