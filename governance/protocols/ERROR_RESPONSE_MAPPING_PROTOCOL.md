# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-09 22:30:00
# 🚨 ERROR → RESPONSE MAPPING PROTOCOL (ERMP)

**Versão:** 3.0
**Classificação:** CONSTITUTIONAL
**Status:** ATIVO
> **Classificação:** CONSTITUTIONAL
> **Integração:** `FAIL_FAST_PROTOCOL` + `atualizar.py`
---

## 1. Objetivo
Definir o comportamento determinístico que a IA deve adotar ao receber um código de erro do executor `atualizar.py`.

**Regra de Ouro:** A IA não deve "pedir desculpas" ou "tentar explicar". Ela deve analisar o código do erro e executar a ação corretiva mapeada abaixo.

---

## 2. Fluxo de Diagnóstico Obrigatório

Sempre que uma execução de código resultar em erro (seja no terminal, no teste ou na validação), a IA deve seguir este fluxo **sem exceção**:

### Passo 1: Relatório de Incidente (Markdown)
Criar um arquivo `docs/reports/INCIDENT_YYYY_MM_DD_ERROR.md` contendo:
- **Erro:** O que aconteceu (Log/Traceback).
- **Arquivos Envolvidos:** Lista de arquivos suspeitos.
- **5 Principais Hipóteses:** Lista numerada de possíveis causas raízes.

### Passo 2: Script de Diagnóstico (Python)
Gerar um script `scripts/diagnosis/debug_incident_xxx.py` que:
- Testa programaticamente as 5 hipóteses levantadas.
- Imprime no terminal qual hipótese foi confirmada ou descartada.
- **Não altera nada**, apenas lê e testa.

### Passo 3: Resolução (Fix)
Somente após o diagnóstico confirmar a causa, gerar o código de correção.

---

## 3. Tabela de Mapeamento (FFP Codes & System Errors)

| Código | Significado | Ação Obrigatória da IA |
| :--- | :--- | :--- |
| **FFP-01** | **Violação de Formato** | **REGENERATE_FULL:** Reescrever a resposta inteira corrigindo as tags XML (`<Task_Classification>`, `[[MESAFLOW_BEGIN]]`). |
| **FFP-02** | **Omissão de Código** | **COMPLETE_FILE:** Identificar o arquivo onde houve `...` e reescrevê-lo **integralmente**, linha por linha. |
| **FFP-03** | **Escopo Violado** | **JUSTIFY_OR_REMOVE:** Se for teste faltando, adicionar `[TEST_EXEMPT]`. Se for refatoração indevida, reverter para o original. |
| **FFP-04** | **Ambiguidade** | **CLARIFY:** A instrução recebida é impossível de executar. Solicitar clarificação ao humano. |
| **FFP-05** | **Não Determinístico** | **FIX_SYNTAX:** O código gerado tem erro de sintaxe (Python/TS). Corrigir o bug lógico e reenviar. |
| **FFP-06** | **Quebra de Governança** | **ABORT:** Você tentou alterar um arquivo protegido (`atualizar.py`, `docs/governance/*`). Pare imediatamente. |
| **FFP-ABORT_AI** | **Recusa da IA** | **REVIEW_MISSION:** A IA anterior recusou a missão. Analise o motivo e não tente forçar a execução. |
| **SYSTEM_ERROR** | **Falha de Ambiente** | **CHECK_PATHS:** O arquivo de entrada não foi encontrado. Verifique se o comando foi rodado no diretório correto. |
| **SECURITY_ERROR** | **Risco de Segurança** | **SANITIZE_PATHS:** Remova qualquer tentativa de acesso a diretórios pais (`..`) ou caminhos absolutos. |
| **RUNTIME_ERR** | **Erro de Execução** | **DIAGNOSE:** Iniciar Fluxo de Diagnóstico (Relatório -> Script -> Fix). |

---

## 4. Fluxo de Correção

1. **Recebimento:** O usuário cola o erro do terminal (ex: `❌ ABORT: [FFP-02] OMISSÃO DE CÓDIGO`).
2. **Análise:** A IA lê o código `FFP-02`.
3. **Execução:**
   - *Pensamento:* "O executor rejeitou porque usei placeholders. Preciso enviar o arquivo completo."
   - *Ação:* Gera o XML novamente com o conteúdo integral.

## 5. Exemplo de Resposta de Correção

Se o erro for `FFP-02` em `app/main.py`:

```xml
<Task_Classification>TRIVIAL</Task_Classification>
<Domain>BACKEND</Domain>

<Schema_Execution>
<Execution_Result>
<Files>
<File>
<Path>app/main.py</Path>
<Content><![CDATA[
[[MESAFLOW_BEGIN:app/main.py]]
... código completo sem omissões ...
[[MESAFLOW_END]]
]]]]><![CDATA[></Content>
</File>
</Files>
</Execution_Result>
</Schema_Execution>
```

> **Nota:** Ao citar tags de protocolo em documentação (como acima), use CDATA aninhado ou escape para evitar que o `atualizar.py` as interprete como início de arquivo real.
## 3. Usabilidade e Clareza
O sistema deve ser fácil e intuitivo.
- Se o erro for de configuração, o script de diagnóstico deve dizer exatamente qual variável de ambiente falta.
- Se o erro for de dependência, o script deve fornecer o comando `pip install` ou `npm install` exato.
