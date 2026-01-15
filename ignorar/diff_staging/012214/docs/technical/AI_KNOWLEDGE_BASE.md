# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-15 01:25:00
# 🧠 AI Knowledge Base & Learned Patterns

---

## 2026-01-15 | FISCAL_MOCK_TESTING
- **Estratégia:** Para validar a integridade do sistema MesaFlow sem dependências externas (Certificado Digital), utiliza-se o `FISCAL_PROVIDER=mock`.
- **Validação:** Este modo simula o ciclo de vida completo da nota (Pendente -> Processando -> Emitida) e permite testar a UI do Histórico e a persistência no banco de dados.
- **Transição:** Uma vez validado o fluxo em Mock, a ativação para produção exige apenas a troca do provider e a inserção do certificado no painel da Focus NFe.

## 2026-01-15 | DIGITAL_CERTIFICATE_ACQUISITION
- **Fato:** O sistema exige certificado e-CNPJ tipo A1 para emissão real.
