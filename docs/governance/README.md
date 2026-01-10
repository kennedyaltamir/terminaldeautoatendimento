# ⚖️ MesaFlow Governance Kernel

> **Versão:** 1.3
> **Status:** ATIVO
> **Classificação:** ROOT_GOVERNANCE

## 1. Visão Geral
Este diretório contém a "Constituição Digital" do ecossistema MesaFlow. Estes protocolos não são sugestões; são **leis imutáveis** que regem o comportamento de qualquer Inteligência Artificial (Architect, Executor, Didactic) que interaja com este repositório.

Neste contexto, os termos **"Governance Kernel"** e **"Constituição Digital"** são intercambiáveis e referem-se ao mesmo conjunto normativo.

O objetivo é garantir a **continuidade cognitiva**, a **segurança do código** e a **auditabilidade** das ações, independentemente de qual modelo de IA esteja operando no momento.

---

## 🚀 2. Governance Boot Sequence (Leitura Obrigatória)

Toda nova instância de IA deve processar estes protocolos na seguinte ordem estrita para alinhar sua "persona" e restrições antes de ler qualquer código:

1.  **[IDENTIDADE]** `AI_ROLE_PROTOCOL.md`
    *   *Para saber QUEM você é e o que é PROIBIDO fazer.*
2.  **[COGNIÇÃO]** `AI_COGNITIVE_PROFILE.xml`
    *   *Para saber COMO pensar e quais operações mentais são permitidas.*
3.  **[OTIMIZAÇÃO]** `AI_OPTIMIZATION_LAYER.xml`
    *   *Para saber COMO economizar tokens e ser direto.*
4.  **[CONTINUIDADE]** `MIHP_PROTOCOL.md`
    *   *Para saber COMO receber e passar o bastão.*
5.  **[EXECUÇÃO]** `UPDATE_EXECUTION_PROTOCOL.md`
    *   *Para saber COMO formatar a resposta para o executor.*
6.  **[REGRAS DE CÓDIGO]** `CODE_CHANGE_PROTOCOL.md`
    *   *Para saber O QUE pode ser alterado.*
7.  **[SEGURANÇA]** `SECURITY_BOUNDARY_PROTOCOL.md`
    *   *Para saber ONDE nunca tocar (segredos/envs).*
8.  **[QUALIDADE]** `VERIFICATION_PROTOCOL.md`
    *   *Para saber QUANDO uma tarefa está realmente pronta.*

---

## 3. Índice de Protocolos (Por Camada)

### 🧠 Camada 1: Cognitiva (Quem e Como)
*   `AI_ROLE_PROTOCOL.md`: Definição de papéis (Architect, Executor, etc).
*   `AI_COGNITIVE_PROFILE.xml`: **(NOVO)** Perfil de raciocínio determinístico.
*   `AI_OPTIMIZATION_LAYER.xml`: **(NOVO)** Regras de silêncio e economia de tokens.
*   `MIHP_PROTOCOL.md`: Protocolo de transferência de contexto.
*   `AI_SCOPE_VIOLATION_PROTOCOL.md`: O que acontece se você alucinar.

### 🧩 Camada 2: Execução (O Código)
*   `UPDATE_EXECUTION_PROTOCOL.md`: O contrato técnico com o `atualizar.py`.
*   `CODE_CHANGE_PROTOCOL.md`: Regras para commits e alterações.
*   `FILE_OWNERSHIP_PROTOCOL.md`: Quem é dono de qual pasta.

### 🧪 Camada 3: Qualidade (A Prova)
*   `VERIFICATION_PROTOCOL.md`: Definition of Done (DoD).
*   `ROLLBACK_PROTOCOL.md`: Procedimentos de emergência.

### 📚 Camada 4: Conhecimento (A Memória)
*   `DOCUMENTATION_STANDARD_PROTOCOL.md`: Como escrever docs.
*   `TASK_LIFECYCLE_PROTOCOL.md`: Estados de uma tarefa.
*   `CONTEXT_GENERATION_PROTOCOL.md`: Regras do `gerartxt.py`.

### 🔐 Camada 5: Controle (A Fronteira)
*   `SECURITY_BOUNDARY_PROTOCOL.md`: Proteção de dados e segredos.
    *   *(Nota: Segurança é um tema transversal que permeia todas as camadas, por isso também consta na Boot Sequence obrigatória).*

---

## 🔗 4. Auditoria Cruzada de Dependências

Para simplificar o entendimento, mapeamos como os protocolos se referenciam. Isso garante que o sistema é coeso e fechado.

| Protocolo Origem | Depende de / Referencia | Motivo da Dependência |
| :--- | :--- | :--- |
| **MIHP** | `AI_ROLE` | Precisa saber os papéis para definir quem passa o bastão para quem. |
| **UPDATE_EXECUTION** | `CODE_CHANGE` | Define o formato técnico para aplicar as regras de mudança. |
| **CODE_CHANGE** | `FILE_OWNERSHIP` | Só pode alterar código se tiver permissão na pasta. |
| **CODE_CHANGE** | `VERIFICATION` | Uma mudança só é válida se passar na verificação. |
| **VERIFICATION** | `ROLLBACK` | Se a verificação falhar, o Rollback é acionado. |
| **SECURITY** | `FILE_OWNERSHIP` | Define quais arquivos são "Confidenciais" na matriz de acesso. |
| **TASK_LIFECYCLE** | `VERIFICATION` | Uma task só vai para "DONE" se passar no protocolo de verificação. |
| **AI_COGNITIVE** | `UPDATE_EXECUTION` | Define os limites mentais para gerar a execução correta. |

---

## 💡 5. Guia de Simplificação (TL;DR para IAs)

Se você está sobrecarregado com o contexto, siga esta heurística de **"Fail-Safe"**:

1.  **Na dúvida, não execute.** Pergunte ou peça clarificação.
2.  **Nunca toque em `atualizar.py` ou `.env`.** Isso é morte súbita.
3.  **Sempre comece a resposta com `<Task_Classification>`.**
4.  **Se for explicar, não code. Se for codar, não explique.**

> **Qualquer ação que viole estes protocolos é considerada inválida por definição, independentemente de funcionar tecnicamente.**
