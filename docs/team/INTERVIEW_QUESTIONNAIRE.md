# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-13 00:50:51

# 📝 Questionário de Avaliação Técnica (100 Perguntas)
Este questionário visa validar a profundidade técnica e o alinhamento cultural dos candidatos com o Protocolo INDA e a stack do MesaFlow.
---
## 🧠 Arquiteto de Software (20 Perguntas)
1.  Como você desenharia uma arquitetura multi-tenant onde o isolamento de dados é garantido no nível do banco de dados e não apenas na aplicação?
2.  Explique a diferença entre Consistência Eventual e Consistência Forte. Onde você aplicaria cada uma no MesaFlow?
3.  Como você lidaria com uma falha parcial no Redis em um ambiente de produção crítica?
4.  Descreva uma estratégia de "Circuit Breaker" para a integração com o iFood.
5.  Qual a sua estratégia para evitar "Vendor Lock-in" ao usar serviços como Neon e Render?
6.  Como você versionaria uma API REST sem quebrar clientes mobile antigos que não foram atualizados?
7.  Explique o padrão "Saga" para transações distribuídas. Ele é necessário no MesaFlow? Por quê?
8.  Como você protegeria o sistema contra ataques de DDoS na camada de aplicação?
9.  Qual a melhor estratégia para lidar com migrações de banco de dados destrutivas em um sistema 24/7?
10. Defina "Idempotência" e dê um exemplo prático na nossa API de pagamentos.
11. Como você arquitetaria o sistema de WebSockets para escalar além de um único servidor?
12. Qual a diferença entre autenticação Stateful (Session) e Stateless (JWT)? Qual usamos e por quê?
13. Como você garantiria que logs de auditoria sejam imutáveis?
14. Explique o conceito de "Hexagonal Architecture" e se ele se aplica ao nosso backend Python.
15. Como você lidaria com a conformidade LGPD em relação à exclusão de dados em backups?
16. Qual sua abordagem para documentação técnica viva (que não fica obsoleta)?
17. Como você avalia o trade-off entre "Build vs Buy" para componentes como Chat e Fiscal?
18. Descreva um cenário onde você teve que refatorar um monolito. Qual foi a estratégia?
19. Como você garante a observabilidade em um sistema distribuído?
20. O que é o Teorema CAP e como ele influencia a escolha do nosso banco de dados?
## ⚙️ Engenheiro Backend (Python/FastAPI) (20 Perguntas)
21. Explique como o `async/await` funciona no Python e como ele difere de Threads.
22. Como você previne N+1 queries no SQLAlchemy?
23. Qual a diferença entre Pydantic v1 e v2? Como isso afeta a performance?
24. Como você implementaria um Rate Limiter customizado no FastAPI?
25. Explique o ciclo de vida de uma dependência (`Depends`) no FastAPI.
26. Como você lidaria com tarefas de longa duração (ex: gerar relatório PDF) sem bloquear a API?
27. Qual a melhor forma de gerenciar configurações sensíveis (.env) em múltiplos ambientes?
28. Como você implementaria testes unitários para uma função que depende do horário atual?
29. Explique como funcionam as Migrations do Alembic e como resolver conflitos de head.
30. Como você otimizaria uma query SQL lenta que faz join em 5 tabelas?
31. Qual a diferença entre `Session` e `ScopedSession` no SQLAlchemy?
32. Como você implementaria Webhooks de saída com garantia de entrega (retries)?
33. Explique o conceito de "Dependency Injection" e como o FastAPI o utiliza.
34. Como você trataria erros de validação de dados vindos de um payload JSON malformado?
35. Qual a estratégia para lidar com Timezones em uma aplicação global?
36. Como você implementaria cacheamento de respostas de API usando Redis?
37. Explique como proteger uma rota para que apenas usuários com role 'admin' acessem.
38. Como você faria o debug de um memory leak em uma aplicação Python?
39. Qual a diferença entre `List`, `Tuple` e `Set` em Python e quando usar cada um?
40. Como você estruturaria o tratamento de exceções globais na API?
## 🎨 Engenheiro Frontend (React/Next.js) (20 Perguntas)
41. Explique a diferença entre Server Components e Client Components no Next.js 14.
42. Como você gerenciaria o estado global de um carrinho de compras complexo sem causar re-renders desnecessários?
43. Qual a estratégia para otimizar o LCP (Largest Contentful Paint) em uma Landing Page?
44. Como você implementaria uma estratégia de "Optimistic UI" ao adicionar um item ao pedido?
45. Explique como funciona o `revalidatePath` e `revalidateTag` no Next.js.
46. Como você lidaria com a internacionalização (i18n) no App Router?
47. Qual a melhor forma de carregar fontes customizadas para evitar CLS (Cumulative Layout Shift)?
48. Como você implementaria um tema Dark/Light sem "flicker" no carregamento?
49. Explique o uso de `useCallback` e `useMemo`. Quando *não* usá-los?
50. Como você faria a integração com WebSockets para atualizar o KDS em tempo real?
51. Qual a diferença entre `localStorage`, `sessionStorage` e `cookies`? Quando usar cada um?
52. Como você implementaria testes E2E com Playwright para um fluxo de checkout?
53. Explique como funciona o Hydration no React e como evitar erros de "Hydration Mismatch".
54. Como você criaria um componente de Modal acessível (A11y)?
55. Qual a estratégia para lidar com formulários complexos e validação (Zod/React Hook Form)?
56. Como você otimizaria imagens pesadas enviadas pelos usuários?
57. Explique o conceito de "Boundary" (Error Boundary, Suspense Boundary) no React.
58. Como você implementaria uma funcionalidade de "Modo Offline" usando Service Workers?
59. Qual a diferença entre `layout.tsx` e `template.tsx` no Next.js?
60. Como você protegeria rotas administrativas no lado do cliente e do servidor?
## 📱 Engenheiro Mobile (React Native) (20 Perguntas)
61. Qual a diferença entre Expo Managed Workflow e Bare Workflow? Por que escolheríamos um ou outro?
62. Como você lidaria com a persistência de dados offline (Offline-first) no app do garçom?
63. Explique como funciona a Bridge do React Native e o que muda com a Nova Arquitetura (Fabric/TurboModules).
64. Como você implementaria a impressão térmica via Bluetooth em Android e iOS?
65. Qual a estratégia para manter o app atualizado sem passar pela revisão da loja (OTA Updates)?
66. Como você gerenciaria a navegação profunda (Deep Linking) para abrir uma mesa específica via QR Code?
67. Explique como otimizar listas longas (FlatList/FlashList) com imagens.
68. Como você lidaria com permissões de sistema (Câmera, Localização) de forma graciosa?
69. Qual a melhor forma de escalar interfaces para diferentes tamanhos de tela e densidades?
70. Como você implementaria notificações Push garantindo que cheguem mesmo com o app fechado?
71. Explique o ciclo de vida de um componente React Native e como ele interage com o AppState.
72. Como você faria o debug de um crash nativo que só acontece em produção?
73. Qual a estratégia para compartilhar código (tipos, lógica) entre o Frontend Web e o Mobile?
74. Como você implementaria autenticação biométrica no app?
75. Explique como funciona o gerenciamento de memória no React Native e como evitar leaks.
76. Como você lidaria com a sincronização de dados em background (Background Fetch)?
77. Qual a diferença entre `StyleSheet` e bibliotecas de estilo como `NativeWind`?
78. Como você configuraria os Flavors/Schemes para ambientes de Dev, Staging e Prod?
79. Como você testaria componentes nativos que dependem de hardware (ex: GPS)?
80. Explique o processo de assinatura e build para Android (AAB) e iOS (IPA).
## 🛡️ DevOps & QA (20 Perguntas)
81. Como você desenharia um pipeline de CI/CD que impede deploy se a cobertura de testes cair?
82. Explique a estratégia de "Blue-Green Deployment" e "Canary Release". Qual se aplica ao MesaFlow?
83. Como você gerenciaria segredos (API Keys) de forma segura em ambientes de container?
84. Qual a estratégia de backup e restore para um banco PostgreSQL de 1TB?
85. Como você monitoraria a latência da API e alertaria a equipe se passasse de 500ms?
86. Explique como funciona o Docker Multi-stage build e por que ele é importante.
87. Como você implementaria Infrastructure as Code (Terraform/Pulumi) para nossa stack?
88. Qual a estratégia para sanitização de dados de produção para uso em ambiente de staging?
89. Como você automatizaria testes de carga para simular 10.000 pedidos simultâneos?
90. Explique como funciona o isolamento de rede em containers Docker.
91. Como você garantiria que uma migration de banco não trave a aplicação em produção?
92. Qual a diferença entre testes de Regressão Visual e Testes Funcionais?
93. Como você implementaria testes de segurança (SAST/DAST) no pipeline?
94. Explique o conceito de "Chaos Engineering" e como aplicá-lo ao MesaFlow.
95. Como você gerenciaria logs centralizados de múltiplos serviços?
96. Qual a estratégia para garantir a idempotência em scripts de automação?
97. Como você validaria a conformidade com a LGPD em nível de infraestrutura?
98. Explique como funciona o auto-scaling baseado em métricas de CPU vs métricas de Request.
99. Como você criaria um ambiente de desenvolvimento efêmero para cada Pull Request?
100. Qual o papel do QA na definição dos critérios de aceite (DoD)?
