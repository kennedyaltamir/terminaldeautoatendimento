# 🛵 DriverDashboardScreen
> **Plataforma:** MOBILE | **Domínio:** LOGÍSTICA | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Interface principal para o entregador da frota própria. Permite a visualização de pedidos prontos para entrega, gestão de rotas ativas e confirmação de recebimento no destino final, integrando telemetria GPS em tempo real.

## 2. Estrutura e Layout (Mobile-First)
- **Delivery Tabs:** Alternância entre "A Retirar" (Pedidos na expedição) e "Em Rota" (Entregas em curso).
- **Map View:** Integração com Leaflet/Google Maps para visualização do trajeto e localização do cliente.
- **Order Cards:** Informações críticas em destaque: Nome do Cliente, Endereço e Valor a Receber (se for dinheiro).

## 3. Elementos Interativos
- **Pickup Trigger:** Botão "Pegar Pedido" que inicia o rastreamento e notifica o cliente via WebSocket.
- **Navigation Shortcuts:** Botões de atalho para abrir o endereço diretamente no **Waze** ou **Google Maps**.
- **POD (Proof of Delivery):** Campo para inserção do código de segurança fornecido pelo cliente para finalizar a entrega.

## 4. Regras de Negócio e Logística
- **GPS Telemetry:** O app envia coordenadas a cada 3 segundos enquanto houver uma entrega ativa.
- **Cash Management:** Registra automaticamente dívidas no `DriverLedger` para pedidos pagos em dinheiro no ato da entrega.
- **Idempotência de Coleta:** Impede que dois motoristas coletem o mesmo pedido simultaneamente através de locks no backend.

## 5. Estados da Tela
- **Idle:** Lista de pedidos disponíveis para coleta.
- **Active Delivery:** Modo focado no mapa e informações de trânsito.
- **Offline:** Aviso de perda de sinal GPS ou internet, mantendo os dados da rota atual em cache.

## 6. Fluxo Técnico (Real-time)
1. Motorista clica em "Pegar".
2. App chama `PATCH /api/admin/delivery/orders/{id}/dispatch`.
3. Backend emite evento `delivery.status` para o cliente.
4. App inicia o loop de `POST /api/admin/delivery/orders/{id}/location`.

---
*MesaFlow Logistics Kernel v5.0*

