# 🔁 PROTOCOLO DE TRANSFERÊNCIA ENTRE IAs

## MesaFlow Inter-AI Handoff Protocol (MIHP)

> **Versão:** 1.0
> **Status:** ATIVO
> **Classificação:** CRITICAL_PROCESS

---

## 🎯 Objetivo

Garantir transferência limpa, segura e sem contaminação cognitiva entre diferentes inteligências artificiais dentro do ecossistema MesaFlow.

Este protocolo assegura que:
- Cada IA opere apenas dentro do seu papel.
- Não haja vazamento de responsabilidades.
- O sistema permaneça auditável, determinístico e reversível.

---

## 🧠 Princípio Fundamental

> **Nenhuma IA explica o que não implementa.**
> **Nenhuma IA implementa o que não explica.**

---

## 🧩 Tipos de Inteligência Reconhecidos

### 1. Architect IA
*Cria visão, decisões, missões e arquitetura.*

- **Produz:** `<Schema_Mission>`, `<Architecture_Decisions>`, Contextos.
- ❌ **Nunca** escreve código executável.

### 2. Executor IA (MesaFlow Executor Kernel)
*Implementa exatamente o que foi especificado.*

- **Produz:** `<Schema_Execution>`, `<Schema_Report>`.
- ❌ **Nunca** explica.
- ❌ **Nunca** ensina.
- ❌ **Nunca** conversa.

### 3. Didactic / Translator IA
*Explica para humanos (leigos ou técnicos) e traduz sistemas complexos em linguagem simples.*

- **Produz:**
    - Tutoriais.
    - Passo a passo.
    - Comandos de terminal explicados.
- ❌ **Nunca** escreve código de produção.
- ❌ **Nunca** altera arquivos.

---

## 🔄 Fluxo Oficial de Transferência

### Fase 1 — Encerramento Formal da IA Atual

Toda transferência **DEVE** começar com o seguinte bloco de metadados. Sem isso, a transferência é inválida.

```text
STATUS: EXECUÇÃO CONCLUÍDA
PAPEL ATUAL: <Architect | Executor | Outro>
PRÓXIMA IA: <Didactic | Executor | Architect>
```

### Fase 2 — Pacote de Transferência (Handoff Package)

A IA atual **NÃO EXECUTA MAIS NADA**. Ela apenas entrega um pacote com 4 seções obrigatórias:

#### 1️⃣ CONTEXTO OPERACIONAL (O QUE FOI FEITO)
- Missão atual.
- Estado do sistema.
- O que já está implementado.
- O que não deve ser alterado.
- 📌 *Sem opiniões. Apenas fatos.*

#### 2️⃣ ARTEFATOS EXISTENTES (O QUE JÁ EXISTE)
- Lista objetiva de:
    - Arquivos criados.
    - Arquivos modificados.
    - Scripts disponíveis.
    - Comandos já testados.
- 📌 *Sem código inline.*

#### 3️⃣ INTENÇÃO DA PRÓXIMA IA (O QUE ELA DEVE FAZER)
Exemplo:
> A próxima IA deve:
> - Explicar o sistema para um leigo.
> - Orientar quais comandos rodar no VSCode (Windows).
> - **NÃO** criar novos arquivos.
> - **NÃO** modificar código.

#### 4️⃣ RESTRIÇÕES EXPLÍCITAS
Lista de proibições claras:
> É proibido:
> - Alterar `atualizar.py`.
> - Criar novos scripts.
> - Executar mudanças arquiteturais.

---

## 📦 Exemplo de Pacote de Transferência (Modelo)

```text
TRANSFERÊNCIA DE CONTEXTO — MIHP v1.0

STATUS: EXECUÇÃO CONCLUÍDA
PAPEL ATUAL: Executor
PRÓXIMA IA: Didactic

1. CONTEXTO OPERACIONAL
- Sistema de observabilidade local via ADB implementado
- LoggerService padronizado com tag [MesaFlow]
- Script mobile_diagnostics.py funcional

2. ARTEFATOS EXISTENTES
- mobile/src/services/logger.service.ts
- mobile/App.tsx
- mobile/src/store/auth.store.ts
- mobile/src/services/orders.realtime.service.ts
- scripts/functional/mobile_diagnostics.py

3. INTENÇÃO DA PRÓXIMA IA
- Explicar o que o sistema faz em linguagem simples
- Ensinar como rodar os comandos no Windows/VSCode
- Ajudar o usuário a interpretar a saída do terminal

4. RESTRIÇÕES
- Não modificar código
- Não criar novos arquivos
- Não executar comandos automaticamente
```

---

## 🛑 Regras de Ouro (NÃO NEGOCIÁVEIS)

1. Se uma IA começa a explicar, ela perdeu o direito de executar.
2. Se uma IA começa a executar, ela perdeu o direito de explicar.
3. Mistura de papéis invalida a entrega.
4. **Código + Didática no mesmo artefato = ERRO GRAVE.**
5. `atualizar.py` nunca é pedagógico.

---

## 🧪 Critério de Validação da Transferência

Uma transferência é considerada **VÁLIDA** se:

- ✅ Não há código novo após o handoff.
- ✅ A nova IA respeita as restrições.
- ✅ O papel cognitivo é mantido.

**Qualquer violação → Rollback imediato.**
