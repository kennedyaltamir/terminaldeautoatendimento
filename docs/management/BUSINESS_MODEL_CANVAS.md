# 👥 Matriz de Responsabilidades (RACI)

Define quem faz o que no projeto MesaFlow.

**Legenda:**
- **(R) Responsible:** Quem executa a tarefa.
- **(A) Accountable:** Quem aprova e responde pelo resultado (apenas um por linha).
- **(C) Consulted:** Quem deve ser consultado antes da decisão/ação.
- **(I) Informed:** Quem deve ser avisado após a conclusão.

| Processo / Atividade | Product Manager | Tech Lead / Architect | Dev Team (Backend/Front) | DevOps / SRE | Stakeholders / Cliente |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Definição de Roadmap** | **A** | C | I | I | C |
| **Especificação de Feature (PRD)** | **R** | A | C | I | C |
| **Arquitetura de Solução (SDS)** | I | **A** | R | C | - |
| **Desenvolvimento de Código** | - | C | **R** | I | - |
| **Code Review (Merge Request)** | - | **A** | R | C | - |
| **Deploy em Produção** | I | C | I | **A/R** | I |
| **Gestão de Incidentes (Crise)** | C | A | R | **R** | I |
| **Homologação Fiscal** | I | A | **R** | C | C |
| **Aprovação de Design (UI/UX)** | **A** | C | R | - | C |
| **Priorização de Bugs** | **A** | C | I | I | I |

## Regras de Governança
1.  **O "A" tem poder de veto.** Se o Architect (A) não aprovar o Code Review, o código não sobe, mesmo que o PM queira.
2.  **O "R" é quem põe a mão na massa.** Não espere que o PM escreva código ou que o Architect configure o pipeline dia-a-dia.
3.  **Consultar (C) é obrigatório.** Ignorar o DevOps na arquitetura gera dívida técnica.