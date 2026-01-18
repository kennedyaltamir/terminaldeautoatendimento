# 🎨 Software Design Specification: Frontend
**Domínio:** FRONTEND | **Versão:** 5.0

## 1. Arquitetura de Dados
- **Zustand:** Gerenciamento de estado volátil (UI, Modais, Filtros).
- **Dexie.js:** Banco de dados local (IndexedDB) para persistência offline de pedidos e fila fiscal.
- **React Query:** Sincronização de estado do servidor e cache de API.

## 2. Estrutura de Rotas (Next.js App Router)
- `/[slug]/menu`: Interface PWA do cliente final.
- `/admin/[slug]/dashboard`: Visão tática do proprietário.
- `/admin/[slug]/kitchen`: Monitor de Produção (KDS).
- `/admin/[slug]/driver`: Painel de Logística e GPS.

## 3. Componentes Core
- **OrderStatusView:** Reage a eventos WebSocket para atualizar o stepper e montar o mapa de rastreamento.
- **TrackingMap:** Utiliza Leaflet.js e OSRM para projeção geográfica real do entregador.
- **EscPosBuilder:** Gerador de buffer binário para impressão térmica via RawBT.

## 4. Resiliência Offline
O `useOfflineSync` monitora a conectividade. Pedidos feitos sem rede são salvos no Dexie e sincronizados automaticamente via `background-sync` assim que o sinal é restaurado.

