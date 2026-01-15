# 🧪 Questionário de Auditoria: QA Automation Engineer (100 Perguntas)
**Foco:** Omni-Check, Testes E2E, Regressão, Performance e Qualidade de Dados.

## Seção 1: Estratégia de Testes & Qualidade (20 Perguntas)
1. Explique a pirâmide de testes aplicada ao ecossistema MesaFlow.
2. O que é o "Omni-Check" e por que ele é a prioridade zero contra o retrabalho?
3. Como o QA garante que uma nova feature não quebre o isolamento RLS?
4. Qual a diferença entre Testes de Fumaça (Smoke Tests) e Testes de Regressão?
5. Como definir o "Caminho Crítico" do sistema para automação E2E?
6. Como o QA valida a integridade financeira (Centavos) em todos os fluxos?
7. O que é o "Definition of Done" (DoD) sob a ótica da qualidade?
8. Como o QA lida com testes em sistemas multi-tenant (massa de dados isolada)?
9. Como garantir que os testes rodem de forma determinística (sem "flakiness")?
10. Qual o papel do QA na validação das RFCs de governança?
11. Como o QA valida o comportamento do sistema em condições de rede instável?
12. Como testar a lógica de "Regra 86" (Estoque Zero) de forma automatizada?
13. Como o QA valida a precisão dos relatórios de BI e Dashboards?
14. Como garantir a cobertura de testes em 100% das rotas mapeadas?
15. Como o QA interage com o `kernel_journal.jsonl` para auditar falhas?
16. Como validar a segurança de permissões (RBAC) via testes de API?
17. Como o QA testa a integração com Webhooks externos sem depender de serviços reais?
18. Qual a estratégia para testar a internacionalização (i18n) da interface?
19. Como o QA valida a conformidade com a LGPD nos fluxos de dados?
20. Como o QA garante que a documentação técnica reflete o comportamento real do código?

## Seção 2: Automação Web (Playwright) (20 Perguntas)
21. Por que escolhemos Playwright em vez de Cypress para o MesaFlow?
22. Como o Playwright lida com a autenticação (Storage State) para evitar logins repetidos?
23. Como testar o fluxo de "Pedido -> Cozinha -> Pronto" simulando dois navegadores?
24. Como o Playwright valida a renderização de Skeletons durante o carregamento?
25. Como simular a perda de conexão (Offline Mode) no Playwright?
26. Como testar a responsividade do Admin em diferentes viewports (Mobile/Desktop)?
27. Como o Playwright interage com elementos dentro de Shadow DOM ou Iframes?
28. Como validar que um som de alerta ("Ding!") foi disparado no KDS Web?
29. Como realizar testes visuais (Visual Regression) para detectar mudanças de layout?
30. Como o Playwright captura logs do console do navegador para diagnóstico?
31. Como testar o fluxo de pagamento via Pix simulando a leitura do QR Code?
32. Como validar a persistência do carrinho no LocalStorage após um refresh?
33. Como o Playwright lida com animações do Framer Motion para não quebrar asserts?
34. Como testar a funcionalidade de "Impressão Térmica" (Mocking Print API)?
35. Como validar o SEO e as Meta Tags dinâmicas de cada loja?
36. Como o Playwright testa a navegação via Middleware (Subdomínios)?
37. Como simular interações complexas como "Drag and Drop" no mapa de mesas?
38. Como o Playwright valida a integridade de dados recebidos via WebSocket?
39. Como configurar o Playwright para rodar em paralelo no CI/CD?
40. Como gerar relatórios de cobertura de código (Istanbul) a partir de testes E2E?

## Seção 3: Automação Mobile (Maestro) (20 Perguntas)
41. O que é o Maestro e por que ele é superior para testes "Human-Like" no mobile?
42. Como o Maestro identifica elementos na tela sem depender de IDs de teste (TestIDs)?
43. Como automatizar o fluxo de login no app mobile usando o Maestro?
44. Como simular a vibração do dispositivo (Haptic Feedback) em testes automatizados?
45. Como o Maestro lida com permissões nativas (Câmera, Bluetooth) no Android?
46. Como testar a sincronia entre o App do Garçom e o KDS Web usando Maestro + Playwright?
47. Como validar o modo "Offline-First" no mobile (desativando rede via ADB)?
48. Como o Maestro testa a navegação entre Stacks (Auth vs App)?
49. Como validar a renderização de QR Codes na tela do celular?
50. Como simular o recebimento de uma Notificação Push durante o teste?
51. Como o Maestro lida com listas infinitas (FlashList) e scroll?
52. Como testar a integração com impressoras Bluetooth (Mocking Bluetooth Stack)?
53. Como validar o "Production Lock" através de scripts de inspeção de binário?
54. Como o Maestro captura screenshots de falha para o relatório forense?
55. Como testar o consumo de bateria e performance do app durante carga pesada?
56. Como validar a hidratação do estado (Zustand) após fechar e abrir o app?
57. Como o Maestro interage com componentes de terceiros (ex: Google Login)?
58. Como automatizar o teste de "Deep Linking" abrindo o app via URL?
59. Como configurar o Maestro para rodar em emuladores headless no CI?
60. Como o QA valida a ofuscação de código em builds de produção?

## Seção 4: Testes de API & Backend (20 Perguntas)
61. Como o Pytest organiza as `fixtures` para garantir um banco limpo em cada teste?
62. Como testar um endpoint protegido por RLS garantindo que ele negue acesso cruzado?
63. Como validar o contrato da API (JSON Schema) usando Pydantic nos testes?
64. Como simular falhas de banco de dados (Mocking DB Session) para testar resiliência?
65. Como testar a idempotência de um endpoint de criação de pedido?
66. Como validar a cadeia de hashes do Ledger Financeiro via script?
67. Como testar a performance de um endpoint sob carga usando Locust?
68. Como validar o processamento de Webhooks de pagamento (Stripe/MP) com payloads reais?
69. Como testar a lógica de "Split de Pagamento" e conferir os valores finais?
70. Como validar a expiração de tokens JWT e o fluxo de Refresh?
71. Como testar a integração com a API do iFood (Mocking External API)?
72. Como validar a emissão de NFC-e em ambiente de homologação?
73. Como testar a concorrência de escrita (Race Conditions) em tabelas de estoque?
74. Como validar o envio de e-mails de recuperação de senha (Mocking SMTP)?
75. Como testar a lógica de IA (Previsão de Vendas) com massa de dados histórica?
76. Como validar o Rate Limiting por IP e por Usuário?
77. Como testar a integridade de arquivos de upload (Magic Numbers/MIME)?
78. Como validar a limpeza automática de logs e dados temporários?
79. Como testar a segurança de endpoints contra injeção de comandos (OS Injection)?
80. Como o QA valida a performance de busca no banco com milhões de registros?

## Seção 5: Regressão & Omni-Check (20 Perguntas)
81. Como o script `run_full_regression.py` orquestra os diferentes tipos de teste?
82. Qual o critério para adicionar um novo teste à suíte de regressão total?
83. Como o Omni-Check lida com falhas parciais (ex: API OK, mas Frontend quebrado)?
84. Como garantir que a massa de dados de teste não polua o ambiente de produção?
85. Como o QA valida o "Stability Score" antes de autorizar um release?
86. Como o Omni-Check detecta "Dead Code" ou rotas órfãs?
87. Como validar a consistência entre o `MASTER_PROJECT_SPECIFICATION.md` e o código?
88. Como o QA testa a reversibilidade (Rollback) de uma migração de banco?
89. Como o Omni-Check valida a integridade dos arquivos de governança (XML)?
90. Como automatizar a verificação de "Broken Links" em toda a documentação?
91. Como o QA valida a performance de renderização (TTI) em cada deploy?
92. Como o Omni-Check lida com dependências externas (APIs fora do nosso controle)?
93. Como gerar um relatório executivo de qualidade para o Product Manager?
94. Como o QA valida a segurança de segredos no `.env` (SEC-04)?
95. Como testar a resiliência do sistema em caso de queda do Redis?
96. Como o Omni-Check valida a conformidade de acessibilidade (A11y) automaticamente?
97. Como o QA testa a escalabilidade do sistema de WebSockets?
98. Como validar a integridade do cache de cardápio após uma alteração de preço?
99. Como o Omni-Check garante que o "Kernel" (`atualizar.py`) não foi alterado indevidamente?
100. Por que o Omni-Check é a única forma de garantir o crescimento sustentável do MesaFlow?
