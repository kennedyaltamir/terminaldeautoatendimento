# 🔄 Plano de Gerenciamento de Mudanças

> **Objetivo:** Controlar o escopo do projeto, evitando o "Scope Creep" (aumento descontrolado) e garantindo que alterações sejam avaliadas quanto a impacto, custo e risco.

## 1. Fluxo de Solicitação de Mudança (Change Request - CR)

Qualquer alteração significativa no escopo (novas features não planejadas, mudança de arquitetura) deve seguir este fluxo:

1.  **Origem:** Stakeholder ou Time identifica a necessidade.
2.  **Registro:** Criação de uma Issue/Ticket com a tag `[CHANGE REQUEST]`.
3.  **Análise de Impacto (Tech Lead):**
    *   Quais arquivos serão afetados?
    *   Qual o risco de regressão?
    *   Afeta o cronograma ou orçamento?
4.  **Aprovação (CCB - Change Control Board):** PM + Tech Lead decidem (Go / No-Go).
5.  **Execução:** Se aprovado, entra no Backlog da Sprint.
6.  **Comunicação:** Atualização do `ROADMAP.md` e notificação aos envolvidos.

## 2. Critérios de Aprovação
Uma mudança só é aprovada se:
- For crítica para o negócio (Legal/Financeiro).
- Tiver ROI claro (Aumenta receita ou reduz custo drasticamente).
- Não colocar em risco a estabilidade do sistema em produção.

## 3. Classificação de Mudanças

| Tipo | Exemplo | Processo |
| :--- | :--- | :--- |
| **Padrão (Standard)** | Ajuste de CSS, Texto, Bugfix leve. | Aprovação do Tech Lead (Code Review). |
| **Normal** | Nova Feature, Integração nova. | Fluxo completo de CR (Análise + Aprovação). |
| **Emergencial** | Fix de segurança, Queda de serviço. | "Fix First, Document Later" (Aprovação pós-incidente). |

## 4. Log de Mudanças (Exemplo)
*Este log deve ser mantido no `CHANGELOG.md` do projeto.*

- **[CR-001]** Migração de WebSockets para Redis (Aprovado - Motivo: Escala).
- **[CR-002]** Adição de suporte a Bitcoin (Rejeitado - Motivo: Baixa demanda/Alto risco).