# 🧾 Especificação Técnica: Homologação Fiscal (NFC-e)

## 1. Visão Geral
Este documento define o protocolo de transição do módulo fiscal do MesaFlow do estado de simulação (Mock) para a operação real com valor jurídico perante a SEFAZ.

## 2. Estratégia de Ambientes
O comportamento do `FiscalProvider` será regido pela variável de ambiente `FISCAL_ENV`.

| Ambiente | `FISCAL_ENV` | Comportamento | Valor Jurídico |
| :--- | :--- | :--- | :--- |
| **Mock** | `mock` | Respostas imediatas simuladas (padrão de desenvolvimento). | Não |
| **Sandbox** | `sandbox` | Comunicação real com o ambiente de homologação da FocusNFe/SEFAZ. | Não |
| **Produção** | `production` | Comunicação real com a SEFAZ. | **SIM** |

## 3. Matriz de Erros e Rejeições SEFAZ
Mapeamento das rejeições mais comuns e o comportamento esperado do sistema:

| Código | Rejeição | Causa Provável | Ação do Sistema |
| :--- | :--- | :--- | :--- |
| **204** | Duplicidade de NF-e | O pedido já foi enviado anteriormente. | Recuperar a chave existente e atualizar o banco. |
| **539** | Duplicidade com diferença na Chave | Tentativa de reemitir o mesmo pedido com dados alterados. | Bloquear e alertar o gestor sobre inconsistência. |
| **225** | Falha no Esquema XML | NCM ou CFOP inválido no cadastro do produto. | Marcar como `error` e exigir correção no cadastro. |
| **703** | Data de Emissão atrasada | Contingência offline enviada após o prazo legal. | Notificar falha crítica de sincronização. |
| **999** | Erro não catalogado | Indisponibilidade momentânea da SEFAZ. | Iniciar retry exponencial (3 tentativas). |

## 4. Protocolo de Testes (Homologação)
Antes de ativar o modo `production`, o lojista deve realizar o seguinte roteiro em `sandbox`:
1. **Configuração:** Inserir Token de Homologação e CSC de teste.
2. **Emissão Simples:** Emitir uma nota com 1 item e pagamento em dinheiro.
3. **Emissão Complexa:** Emitir nota com múltiplos itens, adicionais e desconto de cashback.
4. **Cancelamento:** Realizar o cancelamento de uma nota emitida em menos de 30 minutos.
5. **Validação Visual:** Abrir o PDF (DANFE) gerado e validar se os dados da empresa e do cliente aparecem corretamente.

## 5. Segurança de Credenciais e Certificados
*   **Certificado A1:** O arquivo do certificado (.pfx) deve ser carregado diretamente no painel do provedor (FocusNFe). O MesaFlow **não armazena** o arquivo físico para reduzir a superfície de ataque.
*   **Tokens:** O `FISCAL_TOKEN` deve ser armazenado exclusivamente em variáveis de ambiente (Secrets) no PaaS (Render/Vercel).
*   **Logs:** Dados sensíveis do XML não devem ser registrados em logs de texto plano.

---
*Versão 1.0 - Janeiro de 2026*
