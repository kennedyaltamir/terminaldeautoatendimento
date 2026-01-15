# ⚙️ Questionário de Auditoria: Backend Engineer (100 Perguntas)
**Foco:** FastAPI, PostgreSQL, RLS, Fintech, iFood e Performance.

## Seção 1: FastAPI & API Design (20 Perguntas)
1. Por que o MesaFlow utiliza `async def` em vez de `def` nos endpoints?
2. Como funciona a Injeção de Dependência no FastAPI para o `get_db`?
3. Qual a função do `lifespan` no `main.py`?
4. Como o `SlowAPI` é configurado para proteger contra ataques de força bruta?
5. Como o FastAPI gera automaticamente a documentação Swagger?
6. O que são os `tags_metadata` e como eles organizam a API?
7. Como tratar erros globais usando `exception_handlers`?
8. Qual a diferença entre `BackgroundTasks` e Celery no MesaFlow?
9. Como o middleware de segurança injeta os headers HSTS e CSP?
10. Como validar payloads complexos usando Pydantic v2?
11. Como funciona o roteamento dinâmico para múltiplos tenants?
12. Como o FastAPI lida com o upload de arquivos de imagem?
13. O que é o `jsonable_encoder` e por que ele é usado no cache?
14. Como implementar o versionamento de endpoints sem quebrar o mobile?
15. Como o `Request` object é usado para capturar o IP do cliente?
16. Como o FastAPI integra com o Sentry para rastreio de exceções?
17. Qual a vantagem de usar `Annotated` nos schemas do Pydantic?
18. Como o sistema lida com CORS para permitir acesso do Frontend e Mobile?
19. Como o FastAPI gerencia o pool de conexões com o banco de dados?
20. Como testar um endpoint FastAPI usando o `TestClient`?

## Seção 2: PostgreSQL & RLS (20 Perguntas)
21. O que é Row-Level Security (RLS) e por que ele é vital para o MesaFlow?
22. Como a variável `app.current_company_id` é definida na sessão do banco?
23. Qual o comando SQL para habilitar RLS em uma tabela?
24. Por que usamos `FORCE ROW LEVEL SECURITY`?
25. Como criar uma política que permite ao dono ver apenas seus próprios dados?
26. Como o RLS se comporta quando o usuário logado é um Superuser?
27. Como o `set_tenant` no `database.py` previne vazamento de dados?
28. Como debugar uma query que está sendo bloqueada indevidamente pelo RLS?
29. Qual o impacto de performance do RLS em tabelas com milhões de linhas?
30. Como o RLS interage com Joins entre tabelas de diferentes domínios?
31. Por que algumas tabelas (ex: `products`) não têm `company_id` direto?
32. Como funciona o isolamento associativo via subqueries no RLS?
33. O que é o comando `SET LOCAL` e por que ele é usado em transações?
34. Como garantir que o RLS esteja ativo em ambiente de testes (SQLite vs Postgres)?
35. Como o Alembic gerencia a criação de políticas RLS?
36. Qual o risco de usar `db.execute` puro em relação ao RLS?
37. Como auditar quais políticas RLS estão ativas via `pg_policy`?
38. Como o RLS protege o sistema contra bugs de "esquecimento de filtro" no código?
39. Como criar uma role de banco de dados restrita (`mesaflow_app`)?
40. Como o RLS lida com a tabela `companies` (onde o ID é o próprio Tenant)?

## Seção 3: Modelagem e Integridade Financeira (20 Perguntas)
41. Por que todos os cálculos financeiros são feitos em centavos (Inteiros)?
42. Qual a estrutura da tabela `financial_ledger`?
43. O que é o `integrity_hash` em uma entrada do Ledger?
44. Como o `sequence_id` garante a imutabilidade da cadeia financeira?
45. Como detectar uma quebra de integridade no Ledger (Hash Mismatch)?
46. Qual a diferença entre `CREDIT` e `DEBIT` no contexto do Ledger?
47. Como o sistema lida com o arredondamento em taxas de split (ex: 2.5%)?
48. O que é a "Conciliação Automática" entre o Ledger e o Gateway?
49. Como o sistema trata transações "Órfãs" (existem no Gateway mas não no DB)?
50. Qual a função da tabela `payment_transactions`?
51. Como garantir a idempotência no processamento de Webhooks de pagamento?
52. Como o sistema calcula o saldo da `customer_wallet`?
53. Qual a lógica de expiração de créditos de cashback?
54. Como o sistema lida com estornos (Refunds) no Ledger?
55. Por que usamos `Numeric(10, 2)` no banco mas `int` no código para dinheiro?
56. Como o sistema previne o "Double Spending" em carteiras digitais?
57. Qual o fluxo de um pedido desde a criação até a liquidação financeira?
58. Como o sistema lida com pagamentos parciais em uma mesa?
59. O que é o "Marketplace Fee" e como ele é cobrado?
60. Como gerar um relatório contábil consolidado para o dono da franquia?

## Seção 4: Integrações e Real-time (20 Perguntas)
61. Como o `IfoodService` realiza o polling de pedidos?
62. Qual o fluxo de ingestão de um pedido do iFood para o KDS?
63. Como funciona a verificação de assinatura HMAC nos webhooks do iFood?
64. Como o Redis Pub/Sub distribui mensagens para múltiplos workers de WebSocket?
65. Qual a estrutura de uma mensagem WebSocket para "Novo Pedido"?
66. Como o sistema lida com a desconexão abrupta de um cliente WebSocket?
67. Como o `manager.broadcast` garante que a mensagem chegue apenas ao Tenant correto?
68. Qual a função do `heartbeat` (ping/pong) no WebSocket?
69. Como integrar o sistema de notificações do WhatsApp (Evolution API)?
70. Como o sistema trata falhas na API do WhatsApp (Retry logic)?
71. O que é o `WebhookDispatcher` e como ele enfileira tarefas no Celery?
72. Como o Stripe é usado para cobrança de assinaturas SaaS?
73. Como o sistema reage ao evento `customer.subscription.deleted` do Stripe?
74. Como o Mercado Pago é configurado para Split de Pagamento via OAuth?
75. Qual a diferença entre o Pix Estático e o Pix Dinâmico na integração?
76. Como o sistema lida com a latência de confirmação de pagamento do Gateway?
77. Como o `IfoodService` mapeia produtos externos para o ID interno do MesaFlow?
78. Como o sistema notifica o Mobile quando um pedido muda de status?
79. Qual o papel do `Celery` no processamento de tarefas pesadas?
80. Como monitorar a fila de tarefas do Celery (Flower)?

## Seção 5: Regras de Negócio e Performance (20 Perguntas)
81. Explique a "Regra 86" e como ela é implementada no código.
82. Como o sistema calcula o tempo de preparo (SLA) de um pedido?
83. Qual a lógica de ordenação de pedidos no KDS (Priority Score)?
84. Como o sistema lida com pedidos "Meio a Meio" no banco de dados?
85. Como funciona a gestão de estoque por ingredientes (Ficha Técnica)?
86. Como o sistema bloqueia pedidos fora do horário de funcionamento?
87. Qual a estratégia de cache para reduzir o tempo de resposta do cardápio?
88. Como otimizar queries SQL complexas usando `selectinload` e `joinedload`?
89. Como o sistema lida com a concorrência de dois garçons editando a mesma mesa?
90. Qual a lógica de validação de cupons de desconto (PromotionService)?
91. Como o sistema calcula a comissão dos garçons (Service Fee)?
92. Como o sistema lida com a exclusão lógica (Soft Delete) de produtos?
93. Qual o impacto do uso de Enums como String no banco de dados (RFC-009)?
94. Como o sistema gera o QR Code de mesa de forma segura?
95. Como o motor de IA (Linear Regression) prevê a demanda de vendas?
96. Como o sistema protege a API contra ataques de negação de serviço (DoS)?
97. Como o sistema lida com a tradução de conteúdos para múltiplos idiomas?
98. Qual a estratégia de backup e recuperação de desastres do banco de dados?
99. Como o sistema garante que o total do pedido bate com a soma dos itens?
100. Como o sistema lida com a mudança de plano (Upgrade/Downgrade) do cliente?

