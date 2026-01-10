# 📺 Especificação Técnica: TASK-FEAT-02
> **Título:** Telão de Pedidos (Public Monitor)
> **Status:** SPECIFIED

## 1. Visão Geral
Interface de visualização pública para clientes aguardando retirada (estilo Fast Food).

## 2. Layout da Tela
- **Coluna Esquerda (Preparando):** Lista de números de pedido em cinza/laranja.
- **Coluna Direita (Pronto):** Lista de números de pedido em verde, com destaque e animação de pulso.
- **Header:** Logo da empresa e relógio digital.
- **Footer:** Mensagem customizável (ex: "Retire seu pedido no balcão").

## 3. Comportamento Real-time
- Atualização instantânea via WebSocket quando o status do pedido muda para `ready` no KDS.
- Alerta sonoro (Ding) opcional quando um novo pedido entra na coluna "Pronto".
