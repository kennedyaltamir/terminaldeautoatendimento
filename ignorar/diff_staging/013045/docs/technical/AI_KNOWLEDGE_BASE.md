# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-15 01:25:00
# 🧠 AI Knowledge Base & Learned Patterns
> **System Memory:** Este arquivo registra aprendizados, correções de padrão e regras implícitas descobertas durante a operação.
> **Usage:** Deve ser consultado antes de tarefas complexas para evitar regressão.

---

## 2026-01-15 | FISCAL_EMISSION_400_DIAGNOSIS
- **Sintoma:** Erro "Empresa ainda não habilitada para emissão de NFCe" ao tentar emitir nota via Focus NFe.
- **Causa Raiz:** No painel da Focus NFe, a empresa está cadastrada mas o módulo NFC-e não está ativo ou o Certificado Digital está ausente. Mesmo em Sandbox, a Focus exige um certificado (pode ser um de teste fornecido por eles ou o seu real) para habilitar o CNPJ.
- **Ação:** O MesaFlow está operando corretamente (enviou o JSON e recebeu o erro tratado). O ajuste deve ser feito no painel da Focus NFe.

## 2026-01-15 | SYNTAX_ERROR_FIX
- **Sintoma:** Erro de compilação no Next.js no arquivo `src/lib/api.ts`.    
- **Causa Raiz:** Uso de `#` para comentários em arquivo `.ts`.
- **Regra Aprendida:** Arquivos `.ts`, `.tsx`, `.js` devem usar `//` para metadados de governança.

## 2026-01-14 | FISCAL_INTEGRATION_VERIFIED
- **Evento:** Sucesso no `smoke_test_focus_nfe.py`.
- **Estado:** Credenciais da Focus NFe (Sandbox) validadas e funcionais.
