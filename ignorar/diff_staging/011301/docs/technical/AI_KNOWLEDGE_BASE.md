# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-15 01:10:00
# 🧠 AI Knowledge Base & Learned Patterns
> **System Memory:** Este arquivo registra aprendizados, correções de padrão e regras implícitas descobertas durante a operação.
> **Usage:** Deve ser consultado antes de tarefas complexas para evitar regressão.

---

## 2026-01-15 | FISCAL_EMISSION_NOT_ENABLED
- **Sintoma:** Erro 400 ao emitir nota: "Empresa ainda não habilitada para emissão de NFCe".
- **Causa Raiz:** O CNPJ está cadastrado na Focus NFe, mas o módulo de NFC-e não foi ativado para esta empresa no painel deles.
- **Resolução:** Ação manual necessária no painel da Focus NFe para autorizar o CNPJ a emitir o tipo de documento NFC-e.

## 2026-01-15 | FRONTEND_COMPILATION_SUCCESS
- **Evento:** Sucesso total na compilação do Frontend (`npx tsc --noEmit`).
- **Estado:** Zero erros de sintaxe ou tipagem TypeScript.

## 2026-01-15 | SYNTAX_ERROR_FIX
- **Sintoma:** Erro de compilação no Next.js no arquivo `src/lib/api.ts`.    
- **Causa Raiz:** Uso de `#` para comentários em arquivo `.ts`.
- **Regra Aprendida:** Arquivos `.ts`, `.tsx`, `.js` devem usar `//` para metadados de governança.

## 2026-01-14 | FISCAL_INTEGRATION_VERIFIED
- **Evento:** Sucesso no `smoke_test_focus_nfe.py`.
- **Estado:** Credenciais da Focus NFe (Sandbox) validadas e funcionais.
