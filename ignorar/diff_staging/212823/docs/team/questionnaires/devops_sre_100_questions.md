# 🛡️ Questionário de Auditoria: DevOps & SRE (100 Perguntas)
**Foco:** Infraestrutura, CI/CD, Segurança de Rede, Monitoramento e Resiliência.

## Seção 1: Infraestrutura & Cloud (20 Perguntas)
1. Por que o MesaFlow utiliza o Render.com para o Web Service e a Vercel para o Frontend?
2. Como o Neon.tech (PostgreSQL Serverless) lida com picos de tráfego repentinos?
3. O que é o "Pooled Endpoint" no Neon e por que ele é obrigatório para o Backend?
4. Como configurar o escalonamento horizontal (Autoscaling) no Render para o MesaFlow?
5. Qual a estratégia de backup do banco de dados e como realizar um Point-in-Time Recovery (PITR)?
6. Como o Redis é provisionado para garantir que o Pub/Sub não perca mensagens de KDS?
7. Como gerenciar domínios customizados de clientes (SSL dinâmico) na infraestrutura atual?
8. Qual o impacto de latência entre o banco de dados (Neon) e o servidor de aplicação (Render)?
9. Como configurar o Healthcheck do Render para evitar deploys com falha de conexão ao banco?
10. Como o sistema lida com a persistência de imagens (AWS S3 vs Local Storage)?
11. Como configurar o Cloudflare para proteger a API contra ataques de DDoS?
12. O que é o "Cold Start" em bancos serverless e como o MesaFlow mitiga isso?
13. Como isolar ambientes de Staging e Produção garantindo que chaves não se misturem?
14. Como monitorar o consumo de recursos (CPU/RAM) dos workers do Celery?
15. Qual a política de expiração de logs no provedor de nuvem?
16. Como configurar o VPC Peering (se necessário) entre diferentes provedores?
17. Como o sistema lida com a renovação automática de certificados SSL?
18. Como provisionar uma réplica de leitura para relatórios pesados de BI?
19. Qual a estratégia de "Zero Downtime Deployment" adotada no projeto?
20. Como o sistema lida com a limpeza de volumes temporários em containers Docker?

## Seção 2: CI/CD & Automação (20 Perguntas)
21. Explique o fluxo do GitHub Actions para o deploy automático do Backend.
22. Como o pipeline de CI valida o "Green Build Policy" antes do merge?
23. Como o segredo `DATABASE_URL` é injetado no pipeline sem exposição?
24. O que é o "EAS Build" e como ele automatiza a geração de APKs/IPAs?
25. Como configurar o pipeline para rodar testes de integração antes do deploy?
26. Como o CI/CD lida com migrações de banco de dados (Alembic) automaticamente?
27. Como implementar o "Blue-Green Deployment" usando as ferramentas atuais?
28. Como o pipeline notifica o time em caso de falha no deploy?
29. Como automatizar o upload de Source Maps para o Sentry durante o build?
30. Como o CI/CD valida a integridade do `registry.xml`?
31. Como configurar o cache de dependências (npm/pip) para acelerar o pipeline?
32. Como o pipeline lida com builds de diferentes sabores (Preview vs Production)?
33. Como automatizar a geração do `todososarquivos.txt` no processo de auditoria?
34. Como o CI/CD garante que o `PRODUCTION_LOCK_MOBILE.json` não foi violado?
35. Como implementar um "Canary Release" para testar novas features em apenas um restaurante?
36. Como o pipeline lida com a expiração de tokens de acesso a APIs externas (Stripe/MP)?
37. Como automatizar o rollback de uma versão de Frontend na Vercel?
38. Como o CI/CD valida a conformidade de Enums (RFC-009) antes do deploy?
39. Como configurar o pipeline para rodar o Omni-Check em ambiente de Staging?
40. Como o sistema lida com a concorrência de múltiplos deploys simultâneos?

## Seção 3: Segurança & Hardening (20 Perguntas)
41. Como o sistema protege o endpoint `/health` de ser usado para reconhecimento de infra?
42. O que é o "Boundary Audit" e quais headers de segurança são obrigatórios?
43. Como o sistema previne o vazamento de segredos em logs de erro?
44. Como configurar o Firewall do banco de dados para aceitar apenas conexões do Render?
45. Como o sistema lida com a segurança de Webhooks de entrada (iFood/Stripe)?
46. O que é o "Secrets Scan" e como ele é integrado ao repositório?
47. Como o sistema protege contra ataques de "Man-in-the-Middle" em redes Wi-Fi de restaurantes?
48. Como o RLS (Row-Level Security) atua como a última linha de defesa em caso de invasão da API?
49. Como o sistema lida com a rotação de chaves mestras de criptografia?
50. Como configurar o Rate Limiting global para evitar exaustão de recursos?
51. Como o sistema valida a integridade dos binários mobile (Checksums)?
52. Como o sistema lida com a segurança de arquivos de configuração (.env)?
53. O que é o "Least Privilege Principle" aplicado às roles do PostgreSQL?
54. Como o sistema previne ataques de "SQL Injection" em queries dinâmicas?
55. Como o sistema lida com a segurança de tokens de "Impersonation" (God Mode)?
56. Como configurar o CSP (Content Security Policy) para evitar XSS no Admin?
57. Como o sistema audita acessos administrativos a dados sensíveis de clientes?
58. Como o sistema lida com a conformidade PCI-DSS para dados de cartão?
59. Como o sistema protege a comunicação entre o Backend e o Redis?
60. Como o sistema lida com a revogação imediata de tokens em caso de comprometimento?

## Seção 4: Monitoramento & Observabilidade (20 Perguntas)
61. Como o Sentry é configurado para agrupar erros por Tenant?
62. O que são "Breadcrumbs" e como eles ajudam a debugar um pedido que sumiu?
63. Como monitorar a latência de ponta a ponta (Frontend -> API -> DB)?
64. Como configurar alertas de "Error Rate" acima de 1% no Sentry?
65. Como o `LoggerService` estruturado facilita a ingestão em ferramentas de log?
66. Como monitorar a saúde dos WebSockets em tempo real?
67. Como o sistema reporta falhas de integração com o iFood antes do cliente perceber?
68. Como visualizar o "Stability Score" histórico do projeto?
69. Como configurar dashboards de performance (TTI, LCP) para o Cardápio PWA?
70. Como o sistema lida com o rastreio de transações distribuídas (Correlation ID)?
71. Como monitorar o tempo de resposta de cada query SQL (Slow Query Log)?
72. Como o sistema reporta a taxa de sucesso de pagamentos via Pix?
73. Como configurar alertas de "Disk Space" ou "Memory Leak" no Render?
74. Como o sistema monitora a validade de certificados SSL de domínios customizados?
75. Como o Sentry captura erros de "Native Crash" no aplicativo mobile?
76. Como monitorar a taxa de reconexão dos dispositivos de cozinha?
77. Como o sistema lida com o monitoramento de custos de infraestrutura?
78. Como configurar o "Uptime Robot" para testar o fluxo crítico de pedido?
79. Como o sistema reporta a saúde da fila do Celery?
80. Como o sistema lida com a observabilidade em modo offline?

## Seção 5: SRE & Disaster Recovery (20 Perguntas)
81. O que define um incidente como "Severidade Crítica" no MesaFlow?
82. Qual o procedimento de "Failover" caso o banco de dados principal caia?
83. Como restaurar a operação em uma nova região da AWS em menos de 1 hora?
84. Como o sistema lida com a corrupção de dados no Ledger Financeiro?
85. Qual o plano de comunicação com clientes durante uma queda sistêmica?
86. Como realizar um "Chaos Engineering" testando a queda do Redis?
87. Como o sistema lida com a recuperação de mensagens perdidas durante um downtime?
88. Qual o RTO (Recovery Time Objective) e RPO (Recovery Point Objective) do sistema?
89. Como o sistema lida com a exaustão de conexões no pool do Postgres?
90. Como realizar um "Post-Mortem" técnico após um incidente grave?
91. Como o sistema lida com a falha total do provedor de DNS?
92. Como o sistema garante a integridade dos backups em `backups/`?
93. Como o sistema lida com a falha de um gateway de pagamento (Stripe/MP)?
94. Como realizar a manutenção do banco de dados sem tirar o sistema do ar?
95. Como o sistema lida com a escalada de suporte (N1 -> N2 -> SRE)?
96. Como o sistema garante a resiliência do Kernel em caso de deleção acidental de arquivos?
97. Como o sistema lida com a falha de sincronia entre o Mobile e o Backend?
98. Como realizar um "Stress Test" simulando 10.000 pedidos simultâneos?
99. Como o sistema lida com a segurança física dos dados (Data Residency)?
100. Por que a automação total da infraestrutura é o objetivo final do SRE no MesaFlow?
