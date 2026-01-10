# 🔐 Security Boundary Protocol (SBP)

> **Versão:** 1.0
> **Classificação:** SECURITY_STANDARD

## 1. Objetivo
Definir as fronteiras lógicas de segurança para impedir vazamento de dados, credenciais ou contexto entre ambientes e papéis.

---

## 2. Classificação de Ativos

### Nível 1: Público (Public)
- Código fonte do Frontend (exceto envs).
- Documentação de uso.
- **Acesso:** Qualquer IA.

### Nível 2: Interno (Internal)
- Código do Backend.
- Lógica de Negócio.
- Logs de execução (sem dados sensíveis).
- **Acesso:** Architect, Executor.

### Nível 3: Confidencial (Confidential)
- Arquivos `.env`.
- Chaves de API (Stripe, AWS, Google).
- Certificados Fiscais (.pfx).
- **Acesso:** **PROIBIDO** para IAs (devem apenas referenciar a variável de ambiente, nunca ler o valor).

## 3. Regras de Fronteira

### R1: Environment Isolation
- O código nunca deve conter chaves hardcoded. Sempre usar `process.env` ou `os.getenv`.
- O Executor é proibido de criar arquivos que contenham segredos reais. Deve usar placeholders (`YOUR_KEY_HERE`).

### R2: Context Leakage Prevention
- Ao gerar o contexto (`gerartxt.py`), arquivos listados no `.gitignore` e arquivos de segredos (`.env`, `*.pem`) são estritamente filtrados.

### R3: Sanitização de Logs
- O `LoggerService` e scripts de diagnóstico devem sanitizar dados sensíveis (CPF, Cartão, Senha) antes de imprimir no terminal.

## 4. Auditoria de Fronteira
Scripts de auditoria (`security_audit.py`) devem rodar periodicamente para verificar se algum segredo foi commitado ou se alguma regra de fronteira foi violada.
