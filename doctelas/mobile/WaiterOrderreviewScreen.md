# 📋 WaiterOrderreviewScreen
> **Plataforma:** MOBILE | **Domínio:** WAITER | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Esta tela serve como o "Check-out de Lançamento". É o ponto de revisão final onde o garçom valida os itens selecionados, ajusta quantidades e confirma o envio para a cozinha, garantindo a precisão do pedido antes da produção.

## 2. Estrutura e Layout (UX)
- **Order Summary List:** Exibição compacta dos itens com destaque para modificadores e observações.
- **Financial Footer:** Totalizador destacado com cálculo automático de subtotal.
- **Action Bar:** Botões fixos para "Adicionar Mais Itens" e "Confirmar e Enviar".

## 3. Elementos Interativos
- **Swipe to Delete:** Gesto lateral para remover itens do carrinho de forma rápida.
- **Quantity Adjuster:** Botões de incremento/decremento para ajustes de última hora.
- **Submit Trigger:** Botão de confirmação com estado de `loading` para prevenir envios duplicados.

## 4. Regras de Negócio e Validação
- **Empty Cart Guard:** O botão de envio é desabilitado se o carrinho estiver vazio.
- **Table Context:** O sistema valida se a mesa ainda está ativa no backend antes de processar o envio.
- **Optimistic Feedback:** A UI exibe uma animação de sucesso imediata após o 200 OK da API.

## 5. Estados da Tela
- **Submitting:** Overlay de processamento que bloqueia interações durante a persistência.
- **Network Error:** Alerta nativo caso a conexão falhe, oferecendo a opção de salvar na **Fila Offline**.
- **Success View:** Transição para a tela de confirmação com opção de impressão de ticket.

## 6. Fluxo Técnico e API
1. **Persistência:** Chamada ao endpoint `POST /api/hamburgueria-ze/orders`.
2. **Payload:** Envio de array de `product_id`, `quantity` e `notes`.
3. **Broadcast:** O backend emite um evento `new_order` via WebSocket para todos os terminais KDS.

---
*MesaFlow Mobile Kernel v5.0*

