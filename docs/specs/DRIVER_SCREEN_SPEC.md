# 🛵 Especificação Funcional: App do Entregador (Logistics)

## 1. Visão Geral
Interface simplificada para smartphones, focada em navegação e confirmação de entrega.

## 2. Telas e Comportamentos

### 2.1. Fila de Entregas
- **A Retirar:** Lista de pedidos com status `ready` marcados como `delivery`.
- **Aceite:** O motorista clica em "Pegar Pedido" para assumir a responsabilidade.

### 2.2. Rota e Navegação
- **Visual:** Card com endereço do cliente e valor a cobrar (se for dinheiro).
- **Deep Linking:** Botões diretos para abrir o endereço no **Waze** ou **Google Maps**.
- **WhatsApp Direto:** Botão para iniciar conversa com o cliente sem salvar contato.
- **GPS Relay:** O app envia a coordenada GPS para o backend a cada 15 segundos enquanto estiver "Em Rota".

### 2.3. Confirmação (POD)
- **Validação:** O motorista deve solicitar o código de 4 dígitos ao cliente.
- **Finalização:** Ao digitar o código correto, o pedido muda para `delivered` e o pagamento é confirmado.

## 3. Regras de Sincronização
- **Ledger:** Pedidos pagos em dinheiro geram um débito automático na "Carteira do Motorista" no banco de dados para acerto de contas posterior.
