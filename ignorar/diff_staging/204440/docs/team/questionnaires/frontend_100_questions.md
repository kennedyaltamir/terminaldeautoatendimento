# 🎨 Questionário de Auditoria: Frontend Engineer (100 Perguntas)
**Foco:** Next.js 14, Tailwind CSS, PWA, Multi-tenancy e UX Administrativa.

## Seção 1: Next.js 14 & App Router (20 Perguntas)
1. Qual a diferença fundamental entre Server Components e Client Components no MesaFlow?
2. Por que utilizamos o diretório `src/app` em vez do `pages` legado?
3. Como o Next.js 14 lida com o cache de requisições de dados (fetch) por padrão?
4. O que é o arquivo `layout.tsx` e como ele mantém o estado da Sidebar no Admin?
5. Como funciona o `loading.tsx` para gerar Skeletons automáticos durante a navegação?
6. Explique o uso de `error.tsx` para capturar falhas de renderização em tempo de execução.
7. Como o Next.js otimiza imagens automaticamente através do componente `<Image />`?
8. O que são "Parallel Routes" e como poderiam ser usadas no Dashboard Financeiro?
9. Como o "Streaming" com Suspense melhora a percepção de velocidade no Cardápio PWA?
10. Qual a função do arquivo `generateMetadata` para o SEO das lojas dos clientes?
11. Como o Next.js lida com variáveis de ambiente no lado do cliente (`NEXT_PUBLIC_`)?
12. O que é "Static Site Generation" (SSG) e onde ele se aplica no MesaFlow?
13. Como funciona o "Incremental Static Regeneration" (ISR) para atualizar preços sem novo deploy?
14. Como o App Router resolve conflitos de rotas dinâmicas (ex: `[slug]` vs `admin`)?
15. Qual a importância do `use client` no topo de arquivos que usam Hooks?
16. Como o Next.js 14 minimiza o bundle de JavaScript enviado ao navegador?
17. Como implementar "Route Groups" (pastas com parênteses) para organizar o código?
18. O que é o "Link Prefetching" e como ele acelera a navegação do garçom?
19. Como o Next.js lida com fontes customizadas sem causar "Layout Shift"?
20. Como debugar um Server Component que está falhando no servidor mas não no cliente?

## Seção 2: Multi-tenancy & Middleware (20 Perguntas)
21. Como o `middleware.ts` identifica o Tenant através do subdomínio ou domínio customizado?
22. Explique a lógica de "Rewrite" vs "Redirect" no contexto de domínios de clientes.
23. Como o Frontend comunica ao Backend qual o `company_id` ativo em cada request?
24. O que acontece se um usuário tenta acessar `loja-a.mesaflow.com` com um token da `loja-b`?
25. Como o Middleware protege rotas administrativas de usuários não autenticados?
26. Como o sistema resolve o slug da empresa a partir de um domínio como `pedidos.meurestaurante.com`?
27. Qual a estratégia para evitar que o Middleware adicione latência excessiva em cada clique?
28. Como o Frontend lida com a troca de cores (Theming) dinâmica baseada no Tenant?
29. Onde são armazenadas as preferências visuais (logo, cores) de cada empresa no Frontend?
30. Como o Middleware lida com arquivos estáticos (imagens, ícones) para não interceptá-los?
31. Como garantir que o `favicon` mude de acordo com a empresa acessada?
32. Como o sistema lida com o "Cold Start" de um novo domínio customizado?
33. Qual o papel do `resolve-domain` endpoint na inicialização do Frontend?
34. Como o Frontend previne ataques de "Host Header Injection"?
35. Como o estado do Tenant é persistido entre recarregamentos de página?
36. Como o sistema lida com URLs amigáveis para produtos (ex: `/burguer-artesanal`)?
37. Como o Middleware trata a rota de `health` para monitoramento do Vercel?
38. Como implementar um "Maintenance Mode" específico para apenas um Tenant?
39. Como o Frontend lida com a expiração de sessão em abas de diferentes Tenants?
40. Como o sistema garante que o Google indexe corretamente as páginas de cada cliente?

## Seção 3: Estado Global & PWA (20 Perguntas)
41. Por que usamos Zustand em vez de Redux para o gerenciamento de estado?
42. Como o `CartStore` persiste os itens do carrinho mesmo se o navegador fechar?
43. O que é o `Dexie.js` e qual sua função na arquitetura Offline-First?
44. Como o Frontend detecta que o usuário perdeu a conexão com a internet?
45. Explique o fluxo de sincronização de pedidos feitos em modo offline.
46. O que é o `manifest.json` e como ele define a experiência de "App" do PWA?
47. Como os Service Workers lidam com o cache de assets estáticos no MesaFlow?
48. Como implementar notificações Push no navegador para avisar que o pedido está pronto?
49. Qual a estratégia para evitar que o cache do PWA exiba preços desatualizados?
50. Como o Zustand lida com estados voláteis (ex: modais abertos, filtros de busca)?
51. Como o Frontend gerencia o estado de "Mesa Ativa" via QR Code?
52. O que é o "Hydration Error" no React e como o MesaFlow o previne?
53. Como o sistema lida com a concorrência de múltiplos dispositivos na mesma mesa?
54. Como o PWA se comporta em dispositivos iOS (Safari) em comparação ao Android (Chrome)?
55. Qual a importância do `theme-color` dinâmico no cabeçalho do PWA?
56. Como o Frontend valida o estoque localmente antes de permitir a adição ao carrinho?
57. Como o sistema lida com a limpeza de dados antigos do IndexedDB para economizar espaço?
58. Como o Zustand integra com o React Query para gerenciar dados do servidor?
59. Como implementar um "Undo" (Desfazer) no carrinho usando Zustand?
60. Como o PWA garante que o usuário sempre use a versão mais recente do código?

## Seção 4: UI/UX & Design System (20 Perguntas)
61. O que é o Tailwind CSS e por que ele é a escolha padrão para o MesaFlow?
62. Como os "Design Tokens" (cores, espaçamentos) são organizados no projeto?
63. Como o Shadcn/UI acelera o desenvolvimento sem sacrificar a customização?
64. Explique o uso de `framer-motion` para animações de transição de página.
65. Como garantir a acessibilidade (WCAG) em um cardápio com cores vibrantes?
66. O que é o "Responsive Design" no MesaFlow (Mobile-first vs Desktop Admin)?
67. Como o sistema lida com o "Dark Mode" no Painel Administrativo?
68. Como criar componentes reutilizáveis que aceitam variantes (ex: Button primary/outline)?
69. Como o Tailwind lida com a purga de CSS para manter o arquivo final leve?
70. Como implementar um "Infinite Scroll" performático na lista de pedidos do Admin?
71. Qual a importância do feedback visual (Toasts/Sonner) após cada ação do usuário?
72. Como o Design System trata estados de "Empty State" (ex: Carrinho Vazio)?
73. Como otimizar a renderização de listas grandes usando "Windowing" ou "Virtualization"?
74. Como o Frontend lida com diferentes formatos de imagem (WebP, Avif)?
75. Como garantir que o layout não quebre em telas de tablets (KDS)?
76. Como o sistema lida com a internacionalização (i18n) da interface?
77. O que é o "Cumulative Layout Shift" (CLS) e como os Skeletons ajudam a reduzi-lo?
78. Como implementar um sistema de "Drag and Drop" para organizar o mapa de mesas?
79. Como o Design System lida com mensagens de erro de formulário (Zod + Hook Form)?
80. Como garantir que o botão de "Finalizar Pedido" seja sempre acessível no mobile?

## Seção 5: Integração & Segurança (20 Perguntas)
81. Como o Frontend armazena o JWT de forma segura (LocalStorage vs Cookies)?
82. Como funciona o interceptor do Axios para renovar o token automaticamente?
83. Como o Frontend lida com erros 403 (Forbidden) de forma amigável?
84. Como integrar o SDK do Mercado Pago para Checkout Transparente?
85. Como o Frontend gera e exibe o QR Code Pix para pagamento na mesa?
86. Como o sistema lida com a segurança de formulários contra ataques CSRF?
87. Como o Frontend sanitiza inputs do usuário para prevenir XSS?
88. Como funciona a integração com a API de impressão térmica do navegador?
89. Como o Frontend monitora a latência da API em tempo real?
90. Como o Sentry captura erros de JavaScript no navegador do cliente?
91. Como o Frontend lida com o "Rate Limiting" vindo do Backend?
92. Como implementar o "God Mode" (Impersonation) visualmente para o suporte?
93. Como o Frontend valida o formato de documentos (CNPJ, CPF) antes do envio?
94. Como o sistema lida com a segurança de links de "Recuperação de Senha"?
95. Como o Frontend integra com o Google Analytics/Pixel sem degradar a performance?
96. Como o sistema lida com a conformidade de Cookies (LGPD Banner)?
97. Como o Frontend testa a conectividade com o WebSocket antes de tentar o handshake?
98. Como o sistema lida com a expiração forçada de cache em caso de atualização crítica?
99. Como o Frontend valida a integridade dos dados recebidos via WebSocket?
100. Por que a separação entre lógica de negócio e componentes visuais é crucial no MesaFlow?
