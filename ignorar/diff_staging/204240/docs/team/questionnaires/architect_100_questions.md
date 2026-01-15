# 🏛️ Questionário de Auditoria: Chief Architect (100 Perguntas)
**Foco:** Kernel, Protocolos, SSOT e Integridade Sistêmica.

## Seção 1: Protocolo INDA (20 Perguntas)
1. O que significa a sigla INDA?
2. Qual a diferença entre a fase de 'Inspection' e 'Normalization'?
3. Em qual fase do INDA é gerado o ADR (Architecture Decision Record)?
4. Por que a fase 'Action' deve ser a última e atômica?
5. Como o INDA previne o retrabalho em funcionalidades legadas?
6. O que acontece se um Agente pular a fase de 'Normalization'?
7. Como o protocolo INDA lida com falhas detectadas na fase de 'Action'?
8. Qual o artefato obrigatório da fase de 'Inspection'?
9. Como o INDA se aplica a uma alteração trivial de CSS?
10. Quem tem autoridade para mover uma task de 'Decision' para 'Action'?
11. Como o INDA garante o determinismo em ambientes distribuídos?
12. Explique o conceito de "Kernel Fechado" dentro do INDA.
13. Como o INDA protege a integridade do banco de dados?
14. Qual a relação entre o INDA e o script `atualizar.py`?
15. Como documentar uma decisão que viola temporariamente o INDA?
16. O que define uma "Normalization" bem-sucedida?
17. Como o INDA trata dependências circulares entre tasks?
18. Qual o papel do "Reviewer" no ciclo INDA?
19. Como o INDA escala para times de mais de 10 pessoas?
20. Por que o INDA é considerado a "Constituição" do MesaFlow?

## Seção 2: Sistema KERNEL & Automação (20 Perguntas)
21. Qual a função principal do `atualizar.py`?
22. Como o Kernel valida a integridade de um arquivo antes de sobrescrevê-lo?
23. O que é o RFC-005 (Kernel Snapshot Protocol)?
24. Como o `gerartxt.py` decide quais arquivos incluir no bundle?
25. Qual a importância do `session_id` em cada execução do Kernel?
26. Como o Kernel lida com conflitos de escrita simultânea?
27. O que é o `kernel_journal.jsonl` e qual sua estrutura base?
28. Como o Kernel calcula o "Stability Score"?
29. O que acontece se o SHA-256 de um arquivo em disco divergir da memória do Kernel?
30. Como o Kernel protege arquivos sensíveis como o `.env`?
31. Explique o mecanismo de `Governance_Override`.
32. Como o Kernel automatiza o rollback em caso de erro de I/O?
33. Qual a diferença entre o modo `FULL` e o modo `DELTA` no `gerartxt.py`?
34. Como o Kernel identifica "Placeholders Proibidos" (ex: `...`)?
35. Qual a linguagem base do Kernel e por que foi escolhida?
36. Como o Kernel interage com o sistema de arquivos do Windows?
37. O que é o "Cortex Optimizer" e como ele gera novas tasks?
38. Como o Kernel garante que os backups em `backups/` não consumam todo o disco?
39. Qual o gatilho para o Kernel entrar em modo `READ_ONLY`?
40. Como o Kernel valida a sintaxe AST de um arquivo Python antes da aplicação?

## Seção 3: Arquitetura e SSOT (20 Perguntas)
41. Onde reside a "Fonte Única de Verdade" (SSOT) do projeto?
42. Qual a diferença entre o `MASTER_PROJECT_SPECIFICATION.md` e o `registry.xml`?
43. Por que o MesaFlow utiliza um Monólito Modular em vez de Microserviços?
44. Como a separação de domínios é garantida na estrutura de pastas?
45. Qual a estratégia de escalabilidade horizontal do backend?
46. Como o sistema resolve o problema de "Split Brain" em WebSockets?
47. Qual o papel do Redis na arquitetura de eventos?
48. Como o RLS (Row-Level Security) é injetado na arquitetura de banco?
49. Por que usamos UUID v4 para IDs de Tenant?
50. Como a arquitetura suporta o modo "Offline-First"?
51. Qual a política de versionamento da API?
52. Como o sistema lida com migrações de banco de dados em tempo real?
53. O que define um "Módulo" dentro do monólito?
54. Como é feita a comunicação entre o módulo de Pedidos e o módulo Financeiro?
55. Qual a estratégia de cache para o cardápio público?
56. Como o sistema garante a idempotência em transações financeiras?
57. O que é o "MesaFlow Passport" na visão arquitetural?
58. Como o sistema lida com a expiração de sessões em múltiplos dispositivos?
59. Qual a infraestrutura de observabilidade (Sentry/Logs) recomendada?
60. Como a arquitetura previne o vazamento de dados entre Tenants no nível de cache?

## Seção 4: Agentes e Papéis (20 Perguntas)
61. Quais são os 4 papéis de IA definidos no `AI_ROLE_PROTOCOL.md`?
62. O que o Agente `Architect` está proibido de fazer?
63. Qual o output esperado de um Agente `Executor`?
64. Como o Agente `Reviewer` valida uma entrega técnica?
65. Qual a função do Agente `Didactic` no processo de handoff?
66. Como evitar a "Contaminação de Papel" entre IAs?
67. O que define uma "Violação de Escopo Nível 3"?
68. Como o protocolo MIHP garante a transferência de contexto entre sessões?
69. Por que o `Executor` não deve conversar com o usuário fora do XML?
70. Como o `Architect` define uma `Schema_Mission`?
71. Qual o critério para uma IA ser considerada "L6 Autonomous"?
72. Como os Agentes lidam com instruções contraditórias do usuário?
73. O que é o "Cognitive Noise Isolation" (OPS-01)?
74. Como o Agente `Guardian` monitora a saúde da infraestrutura?
75. Qual a responsabilidade do Agente `Strategist` no Roadmap?
76. Como os Agentes de IA são auditados pelo Kernel?
77. O que acontece se uma IA tentar alterar o `atualizar.py`?
78. Como o Agente `Hunter` (QA) interage com o Omni-Check?
79. Qual o limite de tokens recomendado para um bundle de contexto?
80. Como a IA deve reagir a um erro de "Context Window Exceeded"?

## Seção 5: Governança e Compliance (20 Perguntas)
81. O que é o "Hard Gate" no processo de deploy?
82. Como o `registry.xml` impede o deploy de um código sem evidência de teste?
83. Qual a política de retenção de logs de auditoria?
84. Como o sistema garante conformidade com a LGPD?
85. O que é o "Production Lock" no domínio Mobile?
86. Como o sistema trata a depreciação de Enums (RFC-010)?
87. Qual o rito para aprovação de uma nova RFC?
88. Como o "Zero-Config Gap Analyzer" identifica falhas de setup?
89. O que define um sistema como "Gold Master Ready"?
90. Como a governança lida com "Hotfixes" emergenciais?
91. Qual a importância dos "Mandatory Headers" em cada arquivo?
92. Como o sistema audita o uso de segredos no `.env`?
93. O que é o "Maturity Model L5" e como atingi-lo?
94. Como a governança previne a "Dívida Técnica Silenciosa"?
95. Qual o papel do "Comitê de Arquitetura" no MesaFlow?
96. Como o sistema lida com auditorias externas de investidores?
97. O que é o "Failure Modes Analysis" (FMEA) do projeto?
98. Como a governança garante a portabilidade entre Cloud Providers?
99. Qual o protocolo para "Disaster Recovery" do Kernel?
100. Por que a honestidade técnica é o valor supremo da governança MesaFlow?
