# 🧾 Guia Mestre: Integração Fiscal (Focus NFe v2)
**Domínio:** BACKEND / FISCAL
**Versão:** 2.0 — Gold Master Edition
**Status:** CONSTITUCIONAL

Este documento é o guia definitivo para configuração, homologação e operação do módulo fiscal do MesaFlow OS.

---

## 1. Requisitos Legais e Burocráticos

Para que o sistema emita documentos com validade jurídica (Produção), o estabelecimento deve cumprir os seguintes pré-requisitos:

### 1.1 Documentação da Empresa
- **CNPJ Ativo:** Regularizado perante a Receita Federal.
- **Inscrição Estadual (IE):** Obrigatória para venda de mercadorias (NFC-e).
- **CNAE Compatível:** Atividade econômica de restaurante, bar ou comércio.

### 1.2 Infraestrutura Fiscal
- **Certificado Digital A1:** Arquivo `.pfx` ou `.p12` (não aceitamos A3/Cartão/Token físico).
- **CSC (Código de Segurança do Contribuinte):** Gerado no portal da SEFAZ do estado de origem.
- **ID do CSC:** Identificador numérico vinculado ao código acima.

---

## 2. Configuração Técnica (Passo a Passo)

### Passo 1: Obtenção do Token na Focus NFe
1. Acesse [https://focusnfe.com.br/](https://focusnfe.com.br/) e crie uma conta.
2. No painel, navegue até **Configurações > Tokens de API**.
3. Copie o **Token de Homologação** para testes iniciais.

### Passo 2: Configuração do Ambiente (.env)
Edite o arquivo `C:\mesaflow\.env` e configure as chaves conforme a tabela abaixo:

| Chave | Valor Sugerido | Descrição |
| :--- | :--- | :--- |
| `FISCAL_PROVIDER` | `focus` | Ativa o driver da Focus NFe. |
| `FISCAL_ENV` | `sandbox` | Use `sandbox` para testes e `production` para real. |
| `FISCAL_TOKEN` | `seu_token_aqui` | Token obtido no painel da Focus. |
| `FISCAL_PRODUCTION_CONFIRMED` | `false` | Trava de segurança. Mude para `true` apenas em produção. |

### Passo 3: Cadastro do Tenant (Empresa)
No banco de dados ou via API Admin, os seguintes campos da tabela `companies` devem ser preenchidos para o cliente:
- `cnpj`, `inscricao_estadual`, `csc_token`, `csc_id`.

---

## 3. Validação e Testes

### 3.1 Teste de Conectividade
Execute o validador de integração para garantir que o backend consegue falar com a Focus NFe:
```powershell
python scripts/validation/verify_fiscal_integration.py
```

### 3.2 Teste de Emissão (Sandbox)
1. Realize um pedido no sistema.
2. Marque o pedido como **PAID** (Pago).
3. Verifique o log do backend. O sistema tentará enviar o JSON para a SEFAZ de homologação.
4. O campo `fiscal_status` do pedido deve transicionar para `emitted`.

---

## 4. Matriz de Erros e Resolução

| Erro | Causa Provável | Ação Corretiva |
| :--- | :--- | :--- |
| **401 Unauthorized** | Token inválido ou expirado. | Verifique o `FISCAL_TOKEN` no `.env`. |
| **422 Rejeição 204** | Duplicidade de NF-e. | O sistema recupera automaticamente via `ref`. |
| **422 Rejeição 703** | CSC inválido ou não cadastrado. | Verifique o CSC no portal da SEFAZ. |
| **500 Connection** | Focus NFe ou SEFAZ offline. | O sistema entrará em modo de contingência. |

---

## 5. Segurança e Boas Práticas

1. **Isolamento:** Nunca utilize o token de produção em ambiente de desenvolvimento.
2. **Sigilo:** O `.env` deve ser mantido fora do controle de versão (Git).
3. **Contingência:** Em caso de falha na SEFAZ, o MesaFlow armazena o pedido para emissão posterior assim que o serviço for restabelecido.

---
**MesaFlow OS — Engineered for Stability, Sealed for Market.**
