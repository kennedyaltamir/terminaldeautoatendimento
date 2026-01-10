# Política de Segurança da Informação - MesaFlow

**Classificação:** PÚBLICA
**Última Atualização:** Janeiro de 2026
**Responsável:** CISO / CTO

## 1. Visão Geral
O MesaFlow adota uma abordagem de "Security by Design" e "Defense in Depth". Esta política define as diretrizes de governança, resposta a incidentes e ciclo de vida de desenvolvimento seguro (SDLC).

## 2. Governança de Segurança

### 2.1 Testes de Segurança Contínuos
- **Pentest Automatizado:** O script `scripts/security/automated_pentest.py` é executado obrigatoriamente em todo pipeline de CI/CD antes do deploy em produção.
- **Análise Estática (SAST):** Linters e verificadores de tipo rodam a cada commit.
- **Auditoria de Dependências:** Monitoramento contínuo de CVEs em pacotes Python e Node.js.

### 2.2 Gestão de Vulnerabilidades
Comprometemo-nos com os seguintes SLAs para correção de vulnerabilidades confirmadas:

| Severidade (CVSS) | Tempo de Correção (SLA) |
| :--- | :--- |
| **Crítica (9.0 - 10.0)** | 24 horas |
| **Alta (7.0 - 8.9)** | 7 dias |
| **Média (4.0 - 6.9)** | 30 dias |
| **Baixa (0.1 - 3.9)** | 90 dias |

## 3. Resposta a Incidentes

### 3.1 Canal de Denúncia
Pesquisadores de segurança e clientes podem reportar vulnerabilidades através do e-mail **security@mesaflow.com.br**.

### 3.2 Fluxo de Resposta
1.  **Triagem:** Avaliação da severidade em até 48h.
2.  **Contenção:** Mitigação imediata do risco (ex: WAF block, Hotfix).
3.  **Correção:** Desenvolvimento e deploy da solução definitiva.
4.  **Divulgação:** Notificação aos afetados conforme LGPD e transparência pública (após correção).

## 4. Controles Técnicos (Hardening)

### 4.1 Proteção de Aplicação
- **CSP Estrito:** `object-src 'none'`, `base-uri 'self'`, `frame-ancestors 'self'`.
- **HSTS Preload:** HTTPS forçado por 1 ano em todos os subdomínios.
- **Sanitização:** Inputs validados para prevenir XSS e SQL Injection.

### 4.2 Proteção de Dados
- **Isolamento:** Row-Level Security (RLS) no banco de dados.
- **Criptografia:** TLS 1.2+ em trânsito e AES-256 em repouso.
- **Logs:** Mascaramento de PII (Dados Pessoais Identificáveis) nos logs de aplicação.

---
*Esta política é revisada anualmente ou mediante mudanças arquiteturais significativas.*