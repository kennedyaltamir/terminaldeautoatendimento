# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-15 01:20:00
# 🧠 AI Knowledge Base & Learned Patterns

---

## 2026-01-15 | DIGITAL_CERTIFICATE_ACQUISITION
- **Fato:** O sistema exige certificado e-CNPJ tipo A1 para qualquer emissão fiscal (mesmo em Sandbox na Focus NFe).
- **Restrição:** Certificados tipo A3 (físicos) são incompatíveis com a arquitetura SaaS.
- **Documentação:** Criado guia detalhado em `docs/manuals/DIGITAL_CERTIFICATE_GUIDE.md`.

## 2026-01-15 | FOCUS_NFE_PANEL_REQUIREMENTS
- **Fato:** A API da Focus NFe retorna erro 400 (Empresa não habilitada) se o Certificado Digital (A1) não estiver anexado ao cadastro da empresa no painel deles.
- **Dependência:** Mesmo em ambiente de Homologação/Sandbox, a assinatura digital é um pré-requisito para a ativação do CNPJ no provedor.

## 2026-01-15 | FISCAL_EMISSION_NOT_ENABLED
- **Sintoma:** Erro 400 ao emitir nota: "Empresa ainda não habilitada para emissão de NFCe".
- **Causa Raiz:** Módulo de NFC-e não ativado ou falta de dados cadastrais no provedor.
