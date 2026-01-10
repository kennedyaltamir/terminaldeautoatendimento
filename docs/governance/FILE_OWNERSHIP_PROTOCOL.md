# 📂 File Ownership Protocol (FOP)

> **Versão:** 1.0
> **Classificação:** ACCESS_CONTROL

## 1. Objetivo
Definir a matriz de responsabilidade sobre os arquivos do projeto. Quem pode ler e quem pode escrever em cada diretório.

---

## 2. Matriz de Permissões (R=Read, W=Write)

| Diretório / Arquivo | Architect | Executor | Didactic | Reviewer |
| :--- | :---: | :---: | :---: | :---: |
| `app/` (Backend) | R | **R/W** | R | R |
| `frontend/` (Web) | R | **R/W** | R | R |
| `mobile/` (Native) | R | **R/W** | R | R |
| `docs/architecture/` | **R/W** | R | R | R |
| `docs/tasks/` | **R/W** | **R/W** | R | R |
| `scripts/` | R | **R/W** | R | **R/W** |
| `atualizar.py` | R | **R** (Proibido W) | R | R |
| `gerartxt.py` | R | **R** (Proibido W) | R | R |
| `.env` | R | **R** (Proibido W) | R | R |

---

## 3. Arquivos Protegidos (Immutable Core)

Os seguintes arquivos constituem o **Kernel do Sistema de Governança** e NUNCA devem ser alterados por uma IA em operação normal, apenas via Missão de Governança específica (Nível Architect Sênior):

1. `atualizar.py` (O braço mecânico do sistema).
2. `gerartxt.py` (O olho do sistema).
3. `docs/governance/*.md` (A constituição do sistema).
4. `.gitignore` (A fronteira do repositório).

## 4. Violação de Propriedade
Se o Executor tentar escrever em `docs/architecture/` ou o Architect tentar escrever em `app/main.py`:
- A ação é bloqueada.
- Um incidente de **Violação de Escopo** é registrado.
