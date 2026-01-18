
[[MESAFLOW_BEGIN:docs/tasks/details/TASK-MOB-02/specs.md]]
# 📝 Especificação Técnica: TASK-MOB-02
> **Título:** Implementação de Telas Específicas (Garçom/Cozinha/Driver)
> **Status:** ABERTO
> **Objetivo:** Criar as interfaces nativas para os três perfis operacionais do sistema.

## 1. Escopo de Telas
### 🤵 App do Garçom (Waiter POS)
- Mapa de Mesas (Grid interativo).
- Lançamento de Pedidos (Busca e Categorias).
- Fechamento de Conta (Resumo e Métodos de Pagamento).

### 👨‍🍳 KDS Mobile (Kitchen)
- Fila de Pedidos (Cards com SLA).
- Ações de Status (Iniciar/Finalizar).
- Filtro de Estação.

### 🛵 App do Entregador (Driver)
- Lista de Entregas Disponíveis.
- Detalhes da Rota (Endereço + Botão Waze).
- Confirmação de Entrega (POD).

## 2. Requisitos Técnicos
- Uso de **Zustand** para estado global de pedidos.
- Integração com **WebSockets** para atualizações real-time.
- Design System consistente com a marca MesaFlow.
[[MESAFLOW_END]]