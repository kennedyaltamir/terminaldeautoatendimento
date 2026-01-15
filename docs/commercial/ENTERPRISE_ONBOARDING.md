
# 🤝 Guia de Onboarding: Cliente Enterprise

Este roteiro garante que uma nova operação de grande porte (ex: Estádio ou Rede de Franquias) entre no ar com 100% de sucesso.

## Fase 1: Setup de Infraestrutura (Dia 1)
- [ ] **Provisionamento de Tenant:** Criação do `company_id` e `slug` no Kernel.
- [ ] **Configuração de Pagamento:** Vinculação de chaves de produção (Stripe/MP).
- [ ] **Custom Domain:** Apontamento de CNAME para `pedidos.cliente.com.br`.

## Fase 2: Configuração Operacional (Dia 2)
- [ ] **Importação de Cardápio:** Execução do `ImporterService` (via iFood ou CSV).
- [ ] **Mapeamento de Mesas:** Geração e impressão de QR Codes com o Token de 10 dígitos.
- [ ] **Equipe:** Cadastro de funcionários e atribuição de Roles (Kitchen, Waiter, Driver).

## Fase 3: Homologação de Hardware (Dia 3)
- [ ] **Impressão:** Teste de buffer ESC/POS em impressoras Bluetooth locais.
- [ ] **KDS:** Validação de latência do WebSocket em tablets de produção.

## Fase 4: Go-Live (Dia 4)
- [ ] **Smoke Test:** Realização de um pedido real com pagamento e emissão de NFC-e.
- [ ] **Handover:** Entrega do painel de métricas para a gerência.

---
*MesaFlow Customer Success Team*

