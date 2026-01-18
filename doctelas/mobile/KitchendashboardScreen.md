# 📱 KitchenDashboardScreen
> **Plataforma:** MOBILE | **Domínio:** KDS | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Versão nativa do Monitor de Produção, otimizada para tablets instalados em áreas de calor (cozinha) ou balcões de entrega. Sua função é fornecer uma interface de toque robusta para que os cozinheiros gerenciem a fila de produção com zero atrito.

## 2. Estrutura e Design (Industrial)
- **High-Contrast Cards:** Pedidos exibidos em blocos grandes com fontes de alta legibilidade para leitura à distância.
- **Touch-First Controls:** Botões de ação dimensionados para operação rápida, mesmo com luvas ou mãos úmidas.
- **Grid Adaptativo:** Ajuste automático do número de colunas baseado na orientação do tablet (Landscape/Portrait).

## 3. Elementos Interativos
- **Status Advance:** Toque longo ou clique duplo para mover o pedido para "Pronto", evitando toques acidentais.
- **Item Check-off:** Permite marcar itens individuais como "preparados" dentro de um pedido complexo.
- **Sound Toggle:** Controle de alertas sonoros para novos pedidos diretamente na interface.

## 4. Regras de Produção (KDS)
- **SLA Visual:** O card muda de cor (Verde -> Amarelo -> Vermelho) conforme o tempo de preparo configurado.
- **Station Isolation:** O dispositivo pode ser configurado para exibir apenas itens de uma praça específica (ex: apenas "Grelhados").
- **Persistent State:** Em caso de reinicialização do app, a lista de pedidos é recuperada do cache local (`AsyncStorage`) antes da sincronia com o servidor.

## 5. Estados da Tela
- **New Order Flash:** Animação de borda pulsante para destacar a chegada de novos pedidos.
- **Offline Warning:** Banner persistente caso a conexão com o WebSocket seja interrompida.
- **Empty Queue:** Tela de descanso com estatísticas rápidas do turno.

## 6. Fluxo Técnico
- **WebSocket:** Recebe eventos `new_order` e `order_update` via Redis Pub/Sub.
- **Haptic Feedback:** Vibração do dispositivo ao atingir estados críticos de atraso.
- **API:** `PATCH /api/admin/orders/{id}` para atualização de status.

---
*MesaFlow Mobile Kernel v5.0*

