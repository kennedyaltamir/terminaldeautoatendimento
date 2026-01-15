# 🏗️ Melhorias: Infraestrutura & Backend

Este documento detalha as 10 melhorias críticas para a escalabilidade e resiliência do core MesaFlow.

1.  **Docker Multi-stage Build:** Refatoração do Dockerfile para separar o ambiente de compilação (build) do ambiente de execução (runtime), reduzindo a imagem de ~1.2GB para menos de 200MB.
2.  **Health Checks Avançados:** Implementação de um sistema de monitoramento interno que valida não apenas se a porta 8000 está aberta, mas se a latência do PostgreSQL está abaixo de 100ms e se o Redis está aceitando conexões.
3.  **Redis Caching (Layer 2):** Implementação de cache distribuído para o cardápio público. O sistema deixará de consultar o banco em cada acesso, invalidando o cache apenas quando houver alteração de preço ou disponibilidade no Admin.
4.  **Database Sharding Strategy:** Preparação da camada de dados para suportar múltiplos bancos de dados (shards), permitindo que grandes redes de restaurantes operem em hardware isolado sem afetar os pequenos lojistas.
5.  **Rate Limiting por Tenant:** Configuração de limites de requisições dinâmicos baseados no `company_id`, protegendo a infraestrutura contra ataques de negação de serviço (DoS) direcionados a um único cliente.
6.  **Sentry Breadcrumbs:** Configuração avançada de observabilidade para capturar o estado das variáveis locais no momento exato de uma exceção, facilitando o debug em produção.
7.  **Auto-Migration Check:** Implementação de um hook de pré-deploy que valida se existem migrações do Alembic pendentes, impedindo que o código suba sem a estrutura de banco correspondente.
8.  **API Versioning (v2):** Estruturação de rotas versionadas para garantir que clientes usando versões antigas do PWA (em cache) continuem funcionando enquanto novas funcionalidades são lançadas.
9.  **Connection Pooling Tuning:** Ajuste fino dos parâmetros `pool_size` e `max_overflow` do SQLAlchemy para otimizar o reaproveitamento de conexões em horários de pico.
10. **Background Task Queue (Celery):** Migração de tarefas pesadas (geração de PDFs fiscais, relatórios mensais e disparos em massa) para uma fila de processamento assíncrono dedicada.
