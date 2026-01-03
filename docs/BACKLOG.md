# 📋 Backlog de Produto: MesaFlow (Próximos Passos)

Este documento lista 50 tarefas potenciais para evoluir o MesaFlow de um MVP para um SaaS robusto e comercializável.

## 🍔 Experiência do Pedido (Cliente Final)
*Foco: Aumentar o ticket médio e reduzir a fricção.*

1.  **[Feature] Adicionais e Observações:** Permitir que o cliente escolha "Sem Cebola" ou "Adicionar Bacon" (Relacionamento N:N no banco).
2.  **[Feature] Variação de Produtos:** Suporte para tamanhos (P, M, G) com preços diferentes para o mesmo produto.
3.  **[Feature] Lógica de "Meio a Meio":** Essencial para Pizzarias (cálculo do preço pela maior ou média).
4.  **[UX] Busca no Cardápio:** Barra de pesquisa para encontrar itens rapidamente.
5.  **[UX] Filtros de Dieta:** Tags para filtrar itens Veganos, Sem Glúten, Picantes.
6.  **[Feature] Combos Promocionais:** Lógica para "Compre X leve Y" ou "Combo Burguer + Refri" com desconto.
7.  **[UX] Favoritos / Recentes:** Salvar os últimos pedidos no LocalStorage para pedir de novo rápido.
8.  **[Feature] Gorjeta Digital:** Opção de adicionar % de serviço no checkout.
9.  **[UX] Animações de Feedback:** Usar Framer Motion para animar a entrada de itens no carrinho.
10. **[Feature] Avaliação do Pedido:** Pequeno modal de 1-5 estrelas após o pedido ser entregue.

## 💳 Pagamentos & Financeiro
*Foco: Monetização e Checkout Transparente.*

11. **[Backend] Integração Stripe/Mercado Pago:** Criar intenção de pagamento no backend.
12. **[Frontend] Checkout Transparente:** Formulário de cartão/Pix dentro do app (sem redirecionar).
13. **[Backend] Webhooks de Pagamento:** Ouvir confirmação do banco para mudar status do pedido automaticamente.
14. **[Feature] Split de Pagamento:** Permitir que a mesa divida a conta por pessoa.
15. **[Feature] Pagamento no Balcão:** Opção "Pagar no Caixa" (Dinheiro/Maquininha física).
16. **[Admin] Relatório de Vendas:** Gráfico de faturamento diário/mensal.
17. **[Admin] Exportação Contábil:** Exportar pedidos para CSV/Excel.

## 👨‍🍳 Cozinha & Operação (KDS)
*Foco: Eficiência operacional e tempo de resposta.*

18. **[Feature] Alerta Sonoro:** Tocar um som ("Ding!") na cozinha quando chegar pedido novo.
19. **[Feature] Impressão Térmica:** Gerar layout de cupom não fiscal para impressoras térmicas (via Browser Print).
20. **[Feature] Separação por Estação:** Bebidas vão para a tela do Bar, Comidas para a Cozinha.
21. **[Feature] Botão "Recall":** Desfazer a finalização de um pedido (caso tenha clicado errado).
22. **[Feature] Tempo de Preparo:** Mostrar cronômetro colorido (Verde > Amarelo > Vermelho) no card.
23. **[Feature] Itens Individuais:** Dar baixa em itens específicos (ex: "Hambúrguer pronto", falta "Batata").
24. **[Feature] Modo "Pausa":** Cozinha pode pausar o recebimento de pedidos se estiver sobrecarregada.

## 🏢 Gestão & SaaS (Admin)
*Foco: Controle para o dono e funcionalidades multi-tenant.*

25. **[Feature] Gerador de QR Code:** Criar PDF pronto para impressão com o logo da mesa e QR Code.
26. **[Feature] Horário de Funcionamento:** Bloquear pedidos fora do horário configurado.
27. **[Feature] Controle de Estoque:** Decrementar quantidade disponível ao vender (aviso de "Esgotado").
28. **[Feature] Gestão de Colaboradores:** Criar usuários "Garçom" e "Cozinheiro" com permissões limitadas.
29. **[Feature] Múltiplas Unidades:** Um dono gerenciar várias filiais.
30. **[SaaS] Planos de Assinatura:** Integração com Stripe Customer Portal para o dono pagar o SaaS.
31. **[SaaS] Limites de Plano:** Bloquear criação de produtos se exceder o plano Grátis.
32. **[Onboarding] Tour Guiado:** Tutorial interativo para o dono configurar a loja pela primeira vez.

## 🛡️ Segurança & Auth
*Foco: Proteção de dados e robustez.*

33. **[Auth] Recuperação de Senha:** Fluxo de "Esqueci minha senha" com envio de email (SMTP/SendGrid).
34. **[Auth] Confirmação de Email:** Exigir validação de email no cadastro.
35. **[Auth] Refresh Token:** Implementar rotação de tokens para não deslogar o usuário.
36. **[Security] Rate Limiting:** Limitar número de pedidos por IP para evitar spam/ataques.
37. **[Security] Logs de Auditoria:** Registrar quem alterou o preço ou apagou um produto.
38. **[Security] Validação de Geolocalização:** (Opcional) Permitir pedidos apenas se o GPS estiver perto do restaurante.

## 🏗️ Engenharia & DevOps
*Foco: Qualidade de código, performance e deploy.*

39. **[Infra] Docker Compose Prod:** Configuração otimizada para produção (Nginx, Gunicorn).
40. **[Backend] Testes Unitários:** Aumentar cobertura de testes para >80% (Pytest).
41. **[Frontend] Testes E2E:** Implementar Cypress ou Playwright para testar o fluxo de compra.
42. **[Backend] Cache com Redis:** Cachear o cardápio público para reduzir load no banco.
43. **[Backend] Migrações Automáticas:** Script de deploy que roda o Alembic automaticamente.
44. **[Infra] Monitoramento:** Integrar Sentry para rastreamento de erros em tempo real.
45. **[Frontend] PWA (Progressive Web App):** Tornar o site instalável no celular (manifest.json).
46. **[Code] Linting & Formatting:** Configurar Husky e Prettier para padronizar commits.

## 🤖 Inovação & IA
*Foco: Diferenciais competitivos.*

47. **[AI] Gerador de Descrições:** Usar OpenAI API para criar descrições apetitosas dos pratos.
48. **[AI] Sugestão de Preço:** Analisar concorrência e sugerir preços (Futuro).
49. **[Integration] WhatsApp API:** Enviar status do pedido para o WhatsApp do cliente.
50. **[Integration] iFood Bridge:** (Complexo) Sincronizar pedidos do iFood na mesma tela KDS.





# 📋 Backlog de Produto: MesaFlow (Próximos Passos)

Este documento lista tarefas para evoluir o MesaFlow.

## 🏦 Ativação Financeira (Mercado Pago) - *EM ESPERA*
*Estas tarefas estão prontas no código, aguardando validação da conta no Mercado Pago.*

1.  **[Infra] Validar Conta MP:** Enviar documentos (RG/CNH) para o Mercado Pago para liberar credenciais de produção.
2.  **[Config] Inserir Token:** Rodar `python scripts/configurar_mp_real.py` com o token `APP_USR-...`.
3.  **[Infra] Configurar Webhook:** Em produção (Vercel/Render), configurar a URL do webhook no painel do MP.
4.  **[Feature] Testar Split:** Verificar se a comissão (ex: 2%) está caindo na conta do MesaFlow e o restante na do restaurante.

## 🍔 Experiência do Pedido (Cliente Final)
*Foco: Aumentar o ticket médio e reduzir a fricção.*

5.  **[Feature] Adicionais e Observações:** Permitir que o cliente escolha "Sem Cebola" ou "Adicionar Bacon" (Relacionamento N:N no banco).
6.  **[Feature] Variação de Produtos:** Suporte para tamanhos (P, M, G) com preços diferentes para o mesmo produto.
7.  **[Feature] Lógica de "Meio a Meio":** Essencial para Pizzarias (cálculo do preço pela maior ou média).
8.  **[UX] Busca no Cardápio:** Barra de pesquisa para encontrar itens rapidamente.
9.  **[UX] Filtros de Dieta:** Tags para filtrar itens Veganos, Sem Glúten, Picantes.
10. **[Feature] Combos Promocionais:** Lógica para "Compre X leve Y" ou "Combo Burguer + Refri" com desconto.
11. **[UX] Favoritos / Recentes:** Salvar os últimos pedidos no LocalStorage para pedir de novo rápido.
12. **[Feature] Gorjeta Digital:** Opção de adicionar % de serviço no checkout.
13. **[UX] Animações de Feedback:** Usar Framer Motion para animar a entrada de itens no carrinho.
14. **[Feature] Avaliação do Pedido:** Pequeno modal de 1-5 estrelas após o pedido ser entregue.

## 👨‍🍳 Cozinha & Operação (KDS)
*Foco: Eficiência operacional e tempo de resposta.*

15. **[Feature] Impressão Térmica:** Gerar layout de cupom não fiscal para impressoras térmicas (via Browser Print).
16. **[Feature] Separação por Estação:** Bebidas vão para a tela do Bar, Comidas para a Cozinha.
17. **[Feature] Botão "Recall":** Desfazer a finalização de um pedido (caso tenha clicado errado).
18. **[Feature] Tempo de Preparo:** Mostrar cronômetro colorido (Verde > Amarelo > Vermelho) no card.
19. **[Feature] Itens Individuais:** Dar baixa em itens específicos (ex: "Hambúrguer pronto", falta "Batata").
20. **[Feature] Modo "Pausa":** Cozinha pode pausar o recebimento de pedidos se estiver sobrecarregada.

## 🏢 Gestão & SaaS (Admin)
*Foco: Controle para o dono e funcionalidades multi-tenant.*

21. **[Feature] Gerador de QR Code:** Criar PDF pronto para impressão com o logo da mesa e QR Code.
22. **[Feature] Controle de Estoque:** Decrementar quantidade disponível ao vender (aviso de "Esgotado").
23. **[Feature] Gestão de Colaboradores:** Criar usuários "Garçom" e "Cozinheiro" com permissões limitadas.
24. **[Feature] Múltiplas Unidades:** Um dono gerenciar várias filiais.
25. **[SaaS] Planos de Assinatura:** Integração com Stripe Customer Portal para o dono pagar o SaaS.
26. **[SaaS] Limites de Plano:** Bloquear criação de produtos se exceder o plano Grátis.
27. **[Onboarding] Tour Guiado:** Tutorial interativo para o dono configurar a loja pela primeira vez.

## 🛡️ Segurança & Auth
*Foco: Proteção de dados e robustez.*

28. **[Auth] Recuperação de Senha:** Fluxo de "Esqueci minha senha" com envio de email (SMTP/SendGrid).
29. **[Auth] Confirmação de Email:** Exigir validação de email no cadastro.
30. **[Auth] Refresh Token:** Implementar rotação de tokens para não deslogar o usuário.
31. **[Security] Rate Limiting:** Limitar número de pedidos por IP para evitar spam/ataques.
32. **[Security] Logs de Auditoria:** Registrar quem alterou o preço ou apagou um produto.
33. **[Security] Validação de Geolocalização:** (Opcional) Permitir pedidos apenas se o GPS estiver perto do restaurante.

## 🏗️ Engenharia & DevOps
*Foco: Qualidade de código, performance e deploy.*

34. **[Infra] Docker Compose Prod:** Configuração otimizada para produção (Nginx, Gunicorn).
35. **[Backend] Testes Unitários:** Aumentar cobertura de testes para >80% (Pytest).
36. **[Frontend] Testes E2E:** Implementar Cypress ou Playwright para testar o fluxo de compra.
37. **[Backend] Cache com Redis:** Cachear o cardápio público para reduzir load no banco.
38. **[Backend] Migrações Automáticas:** Script de deploy que roda o Alembic automaticamente.
39. **[Infra] Monitoramento:** Integrar Sentry para rastreamento de erros em tempo real.
40. **[Frontend] PWA (Progressive Web App):** Tornar o site instalável no celular (manifest.json).
41. **[Code] Linting & Formatting:** Configurar Husky e Prettier para padronizar commits.

📑 Relatório de Evolução Estratégica: MesaFlow 2.0

Data: 01 de Janeiro de 2026
Responsável: Arquiteto de Software Sênior
Contexto: SaaS B2B de Autoatendimento para Food Service

1. Expansão da Experiência do Cliente (Frontend & UX)

Objetivo: Aumentar o Ticket Médio e a Retenção.

1.1. Inteligência de Upselling (IA Simples)

Atualmente, o cardápio é estático. Podemos implementar um motor de recomendação baseado em regras ou filtragem colaborativa.

Funcionalidade: Quando o cliente adiciona um "Hambúrguer" ao carrinho, o sistema sugere imediatamente: "Que tal uma Batata Frita por + R$ 5,00?" ou "Clientes que pediram isso também levaram Coca-Cola".

Impacto: Aumento estimado de 15-20% no ticket médio.

Implementação: Tabela product_recommendations (N:N) ou lógica no backend baseada no histórico de pedidos (order_items).

1.2. Programa de Fidelidade Integrado (Cashback)

Substituir o cartãozinho de papel por fidelidade digital.

Funcionalidade: "Ganhe 5% de cashback em pontos para o próximo pedido". O cliente precisa informar o telefone (já implementado no Delivery) para acumular.

Impacto: Retenção brutal. O cliente volta ao restaurante porque tem "dinheiro parado" lá.

Implementação: Nova tabela customer_wallets vinculada ao customer_phone e company_id.

1.3. Chamada de Garçom Digital

Mesmo com autoatendimento, o cliente pode precisar de ajuda.

Funcionalidade: Botão flutuante no menu: "Chamar Garçom". Opções: "Ajuda com Pedido", "Limpeza", "Trazer Conta".

KDS: Toca um som diferente na cozinha ou em um painel específico de garçons.

Implementação: Novo tipo de evento no WebSocket (type: "waiter_call").

1.4. Modo "Racha-Conta" (Split Bill)

A maior dor de cabeça de mesas grandes.

Funcionalidade: O sistema permite que várias pessoas escaneiem o mesmo QR Code. O carrinho é compartilhado (multiplayer) ou individual, e no final, o sistema calcula quanto cada um deve pagar.

Implementação: WebSocket para sincronizar carrinhos em tempo real entre dispositivos da mesma mesa.

2. Expansão Operacional (KDS & Gestão)

Objetivo: Eficiência Operacional e Controle.

2.1. KDS Setorizado (Roteamento de Impressão/Tela)

Restaurantes maiores têm Bar e Cozinha separados.

Funcionalidade: Bebidas aparecem apenas na tela do Bar. Comidas apenas na tela da Cozinha.

Implementação: Adicionar campo station (enum: kitchen, bar, dessert) na tabela products. O frontend do KDS filtra os itens baseados na configuração da tela.

2.2. Gestão de Estoque Avançada (Ficha Técnica)

O controle atual é "1 produto = 1 unidade". Restaurantes precisam de controle de ingredientes.

Funcionalidade: Um "X-Bacon" consome: 1 Pão, 1 Hambúrguer (180g), 2 Fatias de Bacon, 1 Fatia de Queijo.

Impacto: O dono sabe exatamente quanto custa cada prato (CMV - Custo de Mercadoria Vendida) e previne roubos.

Implementação: Tabelas ingredients, recipes (relacionando produto x ingredientes).

2.3. Integração Fiscal (NFC-e / SAT) - CRÍTICO PARA BRASIL

Para vender para restaurantes médios/grandes, a emissão fiscal é obrigatória.

Estratégia: Não construir do zero. Integrar com APIs de parceiros como eNotas, Focus NFe ou Nuven Fiscal.

Fluxo: Pedido Pago -> Envia JSON para API Fiscal -> Recebe PDF/XML da Nota -> Envia link para o cliente via WhatsApp/Email.

2.4. App do Garçom (Comanda Mobile)

Transformar o MesaFlow em uma ferramenta para o garçom também, não só para o cliente.

Funcionalidade: Uma interface simplificada onde o garçom lança pedidos na mesa (para clientes que se recusam a usar o celular).

Implementação: Nova rota no frontend /admin/{slug}/waiter com autenticação simplificada (PIN).

3. Expansão Técnica (Arquitetura & DevOps)

Objetivo: Estabilidade, Segurança e Performance.

3.1. Migração para Redis (Cache & Pub/Sub)

Atualmente usamos memória do processo Python para WebSockets (ConnectionManager). Isso não escala se tivermos múltiplos workers ou servidores (Docker Swarm/K8s).

Ação: Usar Redis para gerenciar as filas de mensagens do WebSocket e cachear o cardápio público (que é muito lido e pouco alterado).

3.2. PWA (Progressive Web App) Real

Tornar o site instalável como um aplicativo nativo.

Ação: Configurar next-pwa, Service Workers para cache offline (o cardápio abre mesmo sem internet, só precisa de rede para enviar o pedido) e notificações Push.

3.3. Testes E2E (End-to-End)

Garantir que o fluxo crítico (Pedir -> Pagar -> Cozinha Receber) nunca quebre.

Ferramenta: Playwright ou Cypress.

Cenário: Script que simula um cliente fazendo pedido e verifica se apareceu na tela do admin.

4. Estratégia de Negócio (SaaS)

Objetivo: Monetização.

4.1. Planos e Limites (Paywall)

Implementar lógica de limitação baseada no plan_tier da empresa.

Free: Até 50 pedidos/mês, Cardápio Básico.

Pro: Pedidos ilimitados, KDS, Estoque.

Enterprise: Múltiplas filiais, API Fiscal.

Implementação: Middleware no Backend que checa count(orders) do mês atual antes de criar novo pedido.

4.2. White Label

Permitir que grandes redes usem o sistema com domínio próprio (pedidos.hamburgueriaze.com.br) em vez de mesaflow.com/....

Implementação: Configuração de DNS e roteamento dinâmico no Next.js (Middleware para reescrever domínios).

5. Roadmap Sugerido (Prioridade)

Se eu tivesse que priorizar a execução agora, seguiria esta ordem:

Curto Prazo (1-2 semanas):

Notificações WhatsApp: Usar API (ex: Twilio ou Evolution API) para enviar "Seu pedido foi aceito" e "Saiu para entrega". Isso reduz ansiedade do cliente no Delivery.

Impressão Térmica Automática: Melhorar o CSS de impressão para suportar impressoras de 58mm e 80mm perfeitamente (layout de cupom).

Médio Prazo (1 mês):

KDS Setorizado: Separar Bar e Cozinha.

Upselling: "Deseja adicionar batata?".

Longo Prazo (3 meses+):

Integração Fiscal: Necessário para escalar vendas B2B.

App do Garçom: Para substituir sistemas legados (Totvs, etc).