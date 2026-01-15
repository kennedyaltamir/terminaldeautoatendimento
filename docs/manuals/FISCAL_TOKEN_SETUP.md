# 🧾 Guia de Configuração: Token Focus NFe

Este documento descreve o processo para obter e configurar a credencial necessária para a emissão de NFC-e no MesaFlow OS.

## 1. Onde obter o Token?

O token é fornecido pela **Focus NFe**. Siga os passos abaixo:

1.  Acesse o painel da Focus NFe: [https://focusnfe.com.br/](https://focusnfe.com.br/)
2.  Faça login com suas credenciais.
3.  No menu lateral, acesse **Configurações** ou **Minha Conta**.
4.  Localize a seção **Tokens de API**.
5.  Existem dois tipos de tokens:
    *   **Token de Homologação (Sandbox):** Usado para testes que não possuem valor jurídico.
    *   **Token de Produção:** Usado para emissão real de notas.
6.  Copie o token correspondente ao ambiente que você configurou no seu `.env` (atualmente definido como `sandbox`).

## 2. Como configurar no Projeto?

O token deve ser inserido no arquivo de variáveis de ambiente na raiz do projeto.

1.  Abra o arquivo `.env` localizado em `C:\mesaflow\.env`.
2.  Procure pela linha que contém `FISCAL_TOKEN=`.
3.  Cole o token obtido logo após o sinal de igual, sem espaços.
    *   Exemplo: `FISCAL_TOKEN=abc123def456ghi789`
4.  Certifique-se de que as outras chaves fiscais estão corretas:
    *   `FISCAL_PROVIDER=focus`
    *   `FISCAL_ENV=sandbox` (ou `production` quando for para valer)
5.  Salve o arquivo.

## 3. Validação

Após salvar o arquivo, execute o script de validação para garantir que o sistema reconheceu a nova configuração:

```powershell
python scripts/validation/verify_fiscal_integration.py
```

## 4. Segurança (Aviso Crítico)

*   **NUNCA** compartilhe seu `FISCAL_TOKEN` em chats públicos ou repositórios Git.
*   O arquivo `.env` está no `.gitignore` para evitar que esta chave vaze para o código-fonte.
*   Em caso de vazamento, revogue o token imediatamente no painel da Focus NFe e gere um novo.

---
*MesaFlow OS — Engenharia de Estabilidade.*

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
