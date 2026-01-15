# ⚙️ Update Execution Protocol (UEP)
# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-14 21:20:00
# VERSION: 8.0 (Unified Kernel & Immune System)

> **Status:** CONSTITUCIONAL
> **Executor:** `atualizar.py` (MesaFlow Kernel v8+)
> **Entrada Oficial:** `resposta.txt`

---

## 1. Objetivo e Filosofia
Este protocolo define o funcionamento do **MesaFlow Kernel Executor**, um sistema operacional cognitivo que orquestra o **Ciclo INDA** (Input, Neural, Decision, Action). O objetivo é garantir integridade, segurança e durabilidade (ACID) em cada intervenção no código.

## 2. O Ciclo INDA (Kernel Pipeline)
O executor opera em fases estritas. A falha em qualquer fase aborta a operação e aciona o Rollback automático.
1. **BOOT & RECEIVE:** Inicializa sessão e valida estrutura XML.
2. **ANALYZE:** Realiza Análise Estática (AST) e verifica placeholders proibidos (`...`).
3. **PLAN & SECURITY:** Verifica permissões contra `PROTECTED_EXACT_FILES`.
4. **APPLY:** Cria Snapshot (KSP) e realiza escrita atômica.
5. **VERIFY:** Valida SHA-256 do disco vs memória.
6. **REPORT:** Emite Score de Integridade e status da transação.

## 3. Contrato de Resposta (XML Strict)
A resposta da IA deve ser um envelope XML puro. **Qualquer texto fora das tags resulta em ABORT.**

### 3.1 Tags Obrigatórias e Ordem:
1. `<Task_Classification>`: TRIVIAL ou COMPLEXA.
2. `<Domain>`: Contexto da alteração.
3. `<Schema_Execution>`: Container mestre.
4. `<Execution_Result>`: Resultado da execução.
5. `<Files>`: Lista de objetos `<File>`.
6. `<Terminal_Commands>`: Lista de comandos para aplicar/validar.
7. `<Knowledge_Accumulation>`: Bloco de aprendizado persistente.

## 4. Regras de Escrita e Resiliência
### 4.1 Omissão Proibida (FFP-02)
É terminantemente proibido o uso de elipses (`...`) ou comentários de "resto do código". A entrega deve ser integral.

### 4.2 Compatibilidade Windows (Encoding)
Todo script Python gerado deve conter o cabeçalho de resiliência Unicode:
```python
import sys, io
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

### 4.3 Acúmulo de Conhecimento
O conteúdo de `<Knowledge_Accumulation>` será anexado ao arquivo `docs/technical/AI_KNOWLEDGE_BASE.md`. O conhecimento deve ser somado, nunca substituído, criando uma memória imunológica contra retrabalho.

---
**Assinatura:** MesaFlow Kernel L6.
