# 🛡️ Especificação Técnica: TASK-MAINT-02
> **Título:** Implementação do Auditor de Integridade Sistêmica (AIS)
> **Status:** APROVADO
> **Objetivo:** Criar uma ferramenta única de diagnóstico que valide a saúde de todos os domínios do MesaFlow.

## 1. Escopo de Auditoria
O AIS deve verificar:
- **Ambiente:** Paridade entre `.env` e `.env.example`.
- **Backend:** Conectividade DB/Redis e integridade de Schemas.
- **Frontend:** Sintaxe de comentários de metadados e presença de `node_modules`.
- **Mobile:** Assets obrigatórios do Expo e consistência do `package.json`.
- **Governança:** Presença de protocolos obrigatórios e estado do `TASKS.md`.

## 2. Regras de Falha
- O script deve retornar Exit Code 1 se encontrar inconsistências críticas.
- Deve gerar um relatório visual no terminal com cores para facilitar a leitura.
