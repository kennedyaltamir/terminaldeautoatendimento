# 🧾 Guia de Configuração: Integração Fiscal (Focus NFe)

Este documento descreve os requisitos legais e técnicos para ativar a emissão de notas no MesaFlow OS.

## 1. Requisitos Legais (O que você precisa ter)

Para utilizar este módulo em **Produção**, o estabelecimento deve possuir:
- **CNPJ Ativo:** Com atividade econômica (CNAE) compatível com comércio/restaurante.
- **Inscrição Estadual:** Ativa no estado de operação.
- **Certificado Digital A1:** Arquivo eletrônico usado para assinar as notas.
- **Credenciamento na SEFAZ:** O contador da empresa deve liberar a emissão de NFC-e/NF-e para o CNPJ.

## 2. Onde obter o Token?

1.  Acesse o painel da Focus NFe: [https://focusnfe.com.br/](https://focusnfe.com.br/)
2.  Crie sua conta. No cadastro, você pode usar seu CPF para fins de teste de desenvolvedor.
3.  No menu lateral, acesse **Configurações > Tokens de API**.
4.  **IMPORTANTE:** Utilize o **Token de Homologação** para o desenvolvimento. Ele permite simular envios sem gerar impostos ou validade jurídica.

## 3. Configuração no .env

Insira as chaves no seu arquivo `C:\mesaflow\.env`:

```ini
FISCAL_PROVIDER=focus
FISCAL_ENV=sandbox
FISCAL_TOKEN=seu_token_de_homologacao_aqui
FISCAL_PRODUCTION_CONFIRMED=false
```

## 4. Validação Técnica

Após configurar, rode o Omni-Check para garantir que o sistema reconheceu o provedor:

```powershell
python scripts/validation/omni_check.py
```

## 5. Fluxo para Clientes (SaaS)

No MesaFlow, cada cliente (Tenant) terá seu próprio `fiscal_token` e `certificado_digital`. Você, como dono da plataforma, configura o seu token master na Focus para gerenciar os sub-clientes ou solicita que cada cliente insira seu próprio token no painel administrativo.

---
*MesaFlow OS — Engenharia de Estabilidade.*
