# ⏪ Rollback Protocol (RP)

> **Versão:** 1.0
> **Classificação:** DISASTER_RECOVERY

## 1. Objetivo
Garantir a reversibilidade de qualquer ação executada pelas IAs, protegendo a integridade do projeto contra alucinações, erros de lógica ou corrupção de arquivos.

---

## 2. Gatilhos de Rollback (Quando reverter?)

O Rollback deve ser acionado imediatamente se:
1. O Executor violar um arquivo protegido (`atualizar.py`).
2. O código gerado quebrar o build de forma impeditiva (Blocker).
3. Houver perda de dados não intencional (ex: Drop table sem backup).
4. A IA entrar em loop de erro (3 tentativas falhas de correção).

## 3. Estratégia de Reversão

### Nível 1: Reversão de Arquivo (Local)
O script `atualizar.py` cria backups automáticos na pasta `Copy/` antes de sobrescrever qualquer arquivo.
- **Ação:** Restaurar o arquivo da pasta `Copy/` para a origem.

### Nível 2: Reversão de Transação (Git)
Se a mudança envolveu múltiplos arquivos e o estado ficou inconsistente.
- **Ação:** `git reset --hard HEAD` (ou commit anterior estável).

### Nível 3: Reversão de Banco de Dados
- **Ação:** Restaurar o último dump ou rodar `seed.py` (em ambiente de dev).

## 4. Registro de Incidente
Todo rollback deve gerar um registro em `docs/reports/INCIDENTS.md` contendo:
- Data/Hora.
- Missão que falhou.
- Causa raiz (Alucinação, Erro de Lógica, Violação de Escopo).
- Ação corretiva tomada.
