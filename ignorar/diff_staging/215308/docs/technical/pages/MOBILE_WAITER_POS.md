# 📱 Módulo Mobile: App do Garçom (POS)
**Telas:** `WaiterTablesScreen` | `OrderEntryScreen` | `PaymentScreen`

## 1. WaiterTablesScreen (Mapa de Salão)
- **Intenção:** Visão panorâmica da ocupação.
- **Elementos:** Grid de mesas com indicadores de tempo de permanência e chamados.
- **Comportamento:** Clique longo em mesa ocupada abre o "Espião de Comanda".

## 2. OrderEntryScreen (Lançamento de Pedidos)
- **Intenção:** Rapidez máxima no atendimento.
- **Elementos:**
    - **QuickSearch:** Busca por nome ou código reduzido.
    - **Counter Component:** Botões +/- integrados ao card do produto.
- **Comportamento:** Salva rascunho localmente. Se o app fechar, o carrinho não é perdido.

## 3. PaymentScreen (Recebimento na Mesa)
- **Intenção:** Fechamento financeiro sem deslocamento ao caixa.
- **Elementos:**
    - **QR Code Generator:** Gera Pix dinâmico na tela do celular.
    - **Bluetooth Print:** Botão para emitir via para o cliente.
- **Comportamento:** Aguarda confirmação do Webhook do Mercado Pago para liberar a mesa.
