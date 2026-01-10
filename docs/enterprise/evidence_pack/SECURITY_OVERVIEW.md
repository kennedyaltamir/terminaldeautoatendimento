# 🛡️ Visão Geral de Segurança (Security Overview)

## 1. Segurança de Aplicação (AppSec)

### 1.1 Autenticação e Autorização
- **Mecanismo:** JWT (JSON Web Tokens) com rotação de Refresh Tokens.
- **Controle de Acesso:** RBAC (Role-Based Access Control) estrito com perfis segregados (Owner, Manager, Cashier, Kitchen, Driver).
- **Proteção de Sessão:** Tokens armazenados de forma segura (SecureStore no Mobile, HttpOnly Cookies/LocalStorage sanitizado na Web).

### 1.2 Isolamento de Dados (Multi-tenancy)
- **Estratégia:** Row-Level Security (RLS) nativo no PostgreSQL.
- **Implementação:** Políticas de banco de dados forçam o filtro por `company_id` em nível de engine, impedindo vazamento de dados entre clientes (Cross-Tenant Leakage) mesmo em caso de falha de código.

### 1.3 Hardening de API
- **Headers de Segurança:** Implementação de HSTS (Preload), CSP Estrito, X-Frame-Options e NoSniff.
- **Validação de Entrada:** Sanitização rigorosa de inputs via Pydantic e Zod para prevenção de Injection (SQLi, XSS).
- **Rate Limiting:** Proteção contra Brute-force e DDoS na camada de aplicação (SlowAPI).

## 2. Segurança de Infraestrutura (InfraSec)

### 2.1 Criptografia
- **Em Trânsito:** TLS 1.2 ou superior obrigatório para todas as comunicações (HTTPS/WSS).
- **Em Repouso:** Dados armazenados em volumes criptografados (AES-256) no provedor de banco de dados (Neon.tech).

### 2.2 Gestão de Segredos
- **Política:** Nenhuma credencial hardcoded no código fonte.
- **Armazenamento:** Variáveis de ambiente injetadas em tempo de execução pela plataforma de orquestração (Render/Vercel).

## 3. Ciclo de Vida de Desenvolvimento Seguro (SDLC)
- **Análise Estática (SAST):** Linters e verificadores de tipo no pipeline de CI.
- **Pentest Automatizado:** Script de verificação de segurança executado antes de cada deploy em produção.
- **Code Review:** Aprovação obrigatória de pares para merge na branch principal.
