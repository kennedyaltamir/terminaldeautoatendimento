# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-09 22:45:00
# 🧠 Context Generation Protocol (CGP)

**Versão:** 2.1
**Classificação:** COGNITIVE_INFRASTRUCTURE
**Arquivo Crítico:** `gerartxt.py`
**Dependência:** `GOVERNANCE_CHANGE_PROTOCOL.md`

---

## 1. Objetivo
Este protocolo define a estrutura rígida da "Memória de Curto Prazo" da IA. O arquivo `todososarquivos.txt` não é um dump aleatório; é uma **narrativa técnica estruturada** para garantir o alinhamento da personalidade e do contexto.
O script `gerartxt.py` é considerado **infraestrutura cognitiva crítica**. Ele é a "retina" da IA. Qualquer erro, ruído excessivo ou omissão indevida neste script causa:
- **Alucinação de IA:** A IA inventa código porque não vê o existente.
- **Sobrecarga Cognitiva:** A IA perde o foco lendo arquivos inúteis (ex: lockfiles).
- **Decisões Arquiteturais Incorretas:** A IA duplica lógica por desconhecer utilitários existentes.

---

## 2. Estrutura de Concatenação (A Narrativa)

O script `gerartxt.py` deve montar o arquivo final seguindo estritamente esta ordem de blocos:

### Bloco 1: A Mente (Governança e Persona)
*Prioridade Absoluta. Define quem a IA é e as leis que ela obedece.*
1. `docs/governance/AI_STARTUP_SEQUENCE.xml`
2. `docs/governance/CONTEXT_PRIORITY_PROTOCOL.md`
3. `docs/Prompts/System_Persona.xml`
4. `docs/governance/AI_ROLE_PROTOCOL.md`
5. `docs/governance/FAIL_FAST_PROTOCOL.md`
6. `docs/governance/UPDATE_EXECUTION_PROTOCOL.md`
7. `docs/governance/ERROR_RESPONSE_MAPPING_PROTOCOL.md`
8. `docs/TASKS.md`
9. `docs/ROADMAP.md`

### Bloco 2: O Corpo (Código Fonte)
*A ordem deve seguir a lógica de dependência: Infra -> Backend -> Frontend -> Mobile.*
1. Arquivos de Configuração (`.json`, `.yaml`)
2. Backend (`app/`)
3. Frontend (`frontend/`)
4. Mobile (`mobile/`)

### Bloco 3: O Conhecimento (Docs e Scripts)
*A ordem de ingestão deve seguir a lógica: Definição -> Operação -> Validação.*

#### 3.1 Especificações Técnicas (`docs/technical/`)
- **Prioridade:** Alta.
- **Conteúdo:** `DATABASE_SCHEMA.md`, `API_REFERENCE.md`, `ARCHITECTURE.md`.
- **Objetivo:** Fornecer a verdade estrutural do sistema antes das ferramentas.

#### 3.2 Automação de Infraestrutura (`scripts/setup/` & `scripts/maintenance/`)
- **Prioridade:** Média-Alta.
- **Conteúdo:** Scripts de seed, migração, limpeza e configuração de ambiente.
- **Objetivo:** Ensinar a IA como manipular o ambiente.

#### 3.3 Garantia de Qualidade (`scripts/validation/` & `scripts/tests/`)
- **Prioridade:** Média.
- **Conteúdo:** Scripts de `verify_TASK-XXX.py` e testes unitários.
- **Objetivo:** Fornecer os critérios de sucesso para novas implementações.

#### 3.4 Relatórios e Logs (`docs/reports/`)
- **Prioridade:** Baixa (Contexto Histórico).
- **Conteúdo:** Incidentes passados e auditorias.
- **Objetivo:** Evitar regressão de erros conhecidos.

---

## 3. Regras de Exclusão e Menção (Anti-Ruído)

### 3.1 A Regra do Lockfile
Arquivos de travamento de dependência (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`) são **estritamente proibidos** na categoria `INCLUDE`.
- **Motivo:** Alta densidade de tokens, baixa densidade de informação semântica.
- **Tratamento:** Devem ser classificados como `MENTION`. A IA deve saber que eles existem, mas não precisa ler seu conteúdo.

### 3.2 A Regra de Assets
Arquivos de mídia (`.png`, `.jpg`, `.mp3`, `.pdf`) e builds (`.apk`, `.bundle`) devem ser classificados como `MENTION` ou `SKIP`.
- **Exceção:** Scripts geradores de assets (ex: `generate_mobile_placeholders.py`) são `INCLUDE`.

### 3.3 Lista Negra (Blocklist)
- Arquivos de Lock (`package-lock.json`, `yarn.lock`, `poetry.lock`)
- Diretórios de Build (`dist`, `build`, `.next`, `__pycache__`)
- Assets Binários (`.png`, `.jpg`, `.ico`, `.pdf`, `.exe`)
- Arquivos de Sistema (`.DS_Store`, `Thumbs.db`)
- Arquivos Temporários do Pipeline (`resposta.txt`, `copy/`)

---

## 4. Metadados de Arquivo
Todo arquivo incluído deve ser precedido por um cabeçalho padronizado para que a IA entenda a recência e o domínio:

```text
[[MESAFLOW_BEGIN:caminho/do/arquivo.ext]]
# DOMAIN: [BACKEND|FRONTEND|MOBILE|GOVERNANCE]
# LAST_MODIFIED: YYYY-MM-DD HH:MM:SS
...conteúdo...
[[MESAFLOW_END]]
