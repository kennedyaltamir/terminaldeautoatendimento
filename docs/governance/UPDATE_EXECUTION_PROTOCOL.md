
# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-09 22:30:00
# ⚙️ Update Execution Protocol (UEP)

**Versão:** 3.0
**Classificação:** CONSTITUTIONAL
**Executor:** `atualizar.py`
> **Entrada Oficial:** `resposta.txt`
**Gatilho de Abortagem:** `FAIL_FAST_PROTOCOL.md`

---
## 1. Objetivo

Este protocolo governa a comunicação estrita entre as Inteligências Artificiais (Architect/Executor) e o script de aplicação `atualizar.py`.

Ele define:
- O formato obrigatório das respostas da IA.
- As validações executadas antes de qualquer escrita em disco.
- As mensagens de erro canônicas que o sistema devolve à IA.
- O comportamento esperado quando o executor recusa uma resposta.

> **Princípio Zero:** O `atualizar.py` não interpreta intenções. Se a IA não seguir este protocolo byte a byte, o código não roda.

---

## 2. Contrato de Entrada da IA (Obrigatório)

Para que uma alteração seja aplicada, a resposta da IA deve conter **todos** os elementos abaixo:

### 2.1 Metadados de Cabeçalho
A primeira e a segunda linha da resposta devem ser, obrigatoriamente o nome do arquivo(diretorio completo baseado a partir da raiz do projeto) e o horário que ele foi gerado.

## 1. Princípio de Segurança de Aplicação

O script `atualizar.py` opera sob a premissa de **"Non-Raw Input"**.
- O usuário copia e cola a resposta da IA.
- O script deve ser resiliente a formatações de markdown extras.
- **Fluxo de Segurança:**
    1. Ler `resposta.txt`.
    2. Extrair blocos `[[MESAFLOW_BEGIN]]`.
    3. Salvar em `Copy/caminho/arquivo`.
    4. Abrir Diff (VSCode) para revisão humana.
    5. Aguardar confirmação explícita (`s` ou `y`).
    6. Aplicar substituição.

---

## 2. Contrato de Resposta (Obrigatório)

Toda resposta da IA deve conter, **necessariamente**, os seguintes elementos na ordem:

1. **Classificação:** `<Task_Classification>` e `<Domain>`.
2. **Execução:** `<Schema_Execution>` contendo os arquivos.
3. **Comandos Finais:** Bloco `<Terminal_Commands>` com:
    - Comando de aplicação (`python atualizar.py`).
    - Comando de validação (`python scripts/validation/...`).
    - **Comando de Commit:** `git add . && git commit -m "..."`.

### Regra de Commit por Task
> **TODA TASK RESOLVIDA DEVE GERAR UM COMMIT.**
> Isso garante o histórico na timeline do Git/VSCode, substituindo a necessidade de histórico local de arquivo.

### 2.1 Classificação e Domínio
Essencial para o motor de Fail-Fast.
```xml
<Task_Classification>TRIVIAL | COMPLEXA</Task_Classification>
<Domain>MOBILE | FRONTEND | BACKEND | DOCUMENTATION | DEVOPS_SCRIPTS | ROOT_CONFIG</Domain>
```

### 2.2 Justificativa de Testes
Obrigatório para tasks `COMPLEXA`.
`[TEST_EXEMPT: motivo técnico claro]` ou inclusão de arquivo em `scripts/tests/`.

### 2.3 Envelope de Execução
Todo código deve residir dentro de `<Schema_Execution>`.
```xml
<Schema_Execution>
    <Execution_Result>
        <Files>
            <File>
                <Path>caminho/do/arquivo.ext</Path>
                <Content><![CDATA[
                [[MESAFLOW_BEGIN:caminho/do/arquivo.ext]]
                ...conteúdo INTEGRAL...
                [[MESAFLOW_END]]
                ]]]]><![CDATA[></Content>
            </File>
        </Files>
    </Execution_Result>
</Schema_Execution>
```

---

## 3. Regras de Escrita (UEP-Rules)

1.  **Regra da Integralidade:** Proibido o uso de `...` ou `restante do código`. O script `atualizar.py` rejeitará o arquivo (FFP-02).
2.  **Regra do Override:** Alterações em arquivos de governança ou no próprio `atualizar.py` exigem a tag:
    `<Governance_Override>TRUE</Governance_Override>`
3.  **Regra do Domínio:** Alterações devem se restringir ao domínio declarado. Mudanças que tocam múltiplos domínios (ex: Backend + Mobile) devem ser tratadas como Task `COMPLEXA` com análise de impacto.
### 2.3 Blocos de Exclusão (Delete Blocks)
Para remover arquivos:

```text
[[MESAFLOW_DELETE:caminho/do/arquivo.ext]]
```

### 2.4 Validação de Testes (QA Check)
Toda resposta deve satisfazer uma das condições:

- **Opção A (Com Teste):** Incluir um arquivo em `tests/`, `scripts/tests/` ou `*.spec.ts`.
- **Opção B (Isenção Explícita):** Incluir a tag de justificativa no corpo da resposta:
  `[TEST_EXEMPT: justificativa técnica clara]`

---

## 3. Validações do Executor (`atualizar.py`)

O script executa o **Protocolo de Validação v4.4** antes de tocar no disco:

### 3.1 Validação Estrutural
- Contagem exata de tags `BEGIN` vs `END`.
- Validação de caminhos (prevenção de Path Traversal).
- Detecção de tags malformadas.

### 3.2 Validação Semântica
- Verificação de Placeholders proibidos.
- Verificação de Classificação da Task.
- Verificação de Testes ou Isenção.

### 3.3 Validação Técnica
- **Sintaxe Python:** Arquivos `.py` passam por `py_compile` em memória. Se houver erro de sintaxe, a escrita é abortada.
- **Hash de Conteúdo:** Se o conteúdo novo for idêntico ao existente, a escrita é pulada (Idempotência).
- **Detecção de Edição Manual:** O script alerta se o arquivo local foi modificado por um humano recentemente.

---

## 4. Comportamento de Escrita de Arquivos

O `atualizar.py` opera sob as seguintes garantias:

1. **Arquivo inexistente**
   - Será criado automaticamente.
   - Diretórios pais são criados recursivamente se necessário.

2. **Arquivo existente**
   - Backup salvo automaticamente na pasta `Copy/` na raiz.
   - Conteúdo sobrescrito integralmente.
   - **Diff Visual:** O script tentará abrir automaticamente o VS Code (`code --diff`) comparando o backup com a nova versão.

3. **Falha após escrita**
   - Backup permanece preservado em `Copy/`.
   - Nenhum rollback automático ocorre sem protocolo explícito.

---

## 4. Integração com ERROR → RESPONSE MAPPING PROTOCOL

Toda falha emitida pelo `atualizar.py` possui um significado normativo.

A IA é **obrigada** a consultar o `ERROR_RESPONSE_MAPPING_PROTOCOL.md` antes de gerar qualquer nova resposta após um erro. O código do erro define se a IA deve tentar um patch, reescrever tudo ou abortar.

---

## 5. Proteção de Arquivos Sensíveis

O executor deve **bloquear** a escrita nos seguintes arquivos, a menos que a tag `<Governance_Override>TRUE</Governance_Override>` esteja presente:
- `atualizar.py`
- `gerartxt.py`
- `docs/governance/*`
- `.env`

---

## 6. Formato de Saída

- **Markdown Específico:** A resposta não deve conter "conversinha". Deve ser técnica e direta.
- **Negar Resumo:** Não resuma o código. Entregue o arquivo completo.
- **Comandos no Final:** A última parte da resposta deve ser sempre o bloco de comandos para copiar e colar no terminal.

```xml
<Terminal_Commands>
    <Command>python atualizar.py</Command>
    <Command>python scripts/validation/verify_TASK-XXX.py</Command>
    <Command>git add .</Command>
    <Command>git commit -m "feat(module): description of task xxx"</Command>
</Terminal_Commands>
```
## 6. Placeholders Proibidos (Falha Crítica)

A IA **NUNCA** pode usar expressões de omissão. A detecção de qualquer um dos padrões abaixo causa rejeição total:

- `...` (isolado ou em comentários)
- `// ...restante do código`
- `# ...code omitted`
- `/* mantém o resto */`
- `keep the rest`

📛 **Consequência:** O arquivo é descartado e um erro de protocolo é gerado.

---

## 7. Respostas Canônicas de Falha

Quando o `atualizar.py` recusa uma resposta, ele emite mensagens padronizadas. A IA deve tratar essas mensagens como **sinais de controle**, não como texto de conversa.

### ❌ ERRO 01 — Violação Estrutural
```text
[PROTOCOL_ERROR]
Divergência de tags MESAFLOW_BEGIN / MESAFLOW_END.
Resposta inválida para execução automática.
```
➡️ **Ação da IA:** Regenerar a resposta inteira corrigindo o fechamento das tags.

### ❌ ERRO 02 — Classificação Ausente
```text
[PROTOCOL_ERROR]
Classificação de Task (TRIVIAL ou COMPLEXA) não encontrada.
```
➡️ **Ação da IA:** Reenviar adicionando as tags de cabeçalho.

### ❌ ERRO 03 — Omissão Detectada
```text
[PROTOCOL_ERROR]
Placeholder de omissão detectado.
Conteúdo parcial não é aceito pelo executor.
```
➡️ **Ação da IA:** Reenviar o arquivo **completo**, sem preguiça.

### ❌ ERRO 04 — Teste Ausente
```text
[PROTOCOL_ERROR]
Task sem arquivo de teste e sem justificativa TEST_EXEMPT.
```
➡️ **Ação da IA:** Criar o teste faltante OU adicionar `[TEST_EXEMPT: motivo]`.

### ❌ ERRO 05 — Erro de Sintaxe
```text
[EXECUTION_ERROR]
Erro de sintaxe detectado no arquivo gerado: [Detalhes do erro Python]
```
➡️ **Ação da IA:** Corrigir o código fonte e reenviar.

## 8. Cláusula Final
Este protocolo é a única forma válida de mutação de código no MesaFlow. Qualquer desvio invalida a entrega.
Este protocolo garante que o sistema MesaFlow seja:
1. **Determinístico:** A mesma entrada gera sempre o mesmo resultado.
2. **Reversível:** Backups automáticos são criados antes de qualquer escrita.
3. **Auditável:** Toda mudança é registrada e validada.
4. **Imune a Alucinações:** Código incompleto ou quebrado é rejeitado na porta de entrada.