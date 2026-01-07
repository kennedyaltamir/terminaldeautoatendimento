# 🚀 Checklist de Produção Fiscal (Go-Live)

Este documento deve ser validado integralmente antes de ativar `FISCAL_ENV=production`.

## 1. Requisitos Legais e Cadastrais
- [ ] **Certificado Digital A1:** Instalado e validado no painel da FocusNFe.
- [ ] **Credenciamento SEFAZ:** Empresa autorizada a emitir NFC-e no estado de origem.
- [ ] **CSC (Produção):** Código de Segurança do Contribuinte de produção obtido no portal da SEFAZ.
- [ ] **ID do CSC:** Identificador numérico do CSC (ex: 000001).

## 2. Configuração de Produtos
- [ ] **NCM:** Todos os produtos ativos possuem NCM válido (8 dígitos).
- [ ] **CFOP:** CFOP de venda (geralmente 5102 ou 5405) revisado pela contabilidade.
- [ ] **Unidade:** Unidade de medida padronizada (UN, KG, LT).

## 3. Infraestrutura e Segurança
- [ ] **Variáveis de Ambiente:**
    - `FISCAL_ENV=production`
    - `FISCAL_PRODUCTION_CONFIRMED=true`
    - `FISCAL_PROVIDER=focus`
- [ ] **Secrets:** `FISCAL_TOKEN` de produção configurado no Render/Vercel.
- [ ] **Webhook:** URL de retorno da FocusNFe configurada para apontar para `/api/webhooks/fiscal/focus`.

## 4. Validação Final
- [ ] **Teste Sandbox:** Pelo menos 3 emissões bem-sucedidas em ambiente de homologação nas últimas 24h.
- [ ] **Contingência:** Validar se o worker de sincronização offline está ativo.

---
*Aprovação Técnica: Arquiteto MesaFlow*
