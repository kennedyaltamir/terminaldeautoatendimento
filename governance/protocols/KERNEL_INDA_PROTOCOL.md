# ⚖️ Governança Kernel & Protocolo INDA
> **Framework de Execução e Qualidade para o Ecossistema MesaFlow**

## 1. O Conceito de "Kernel"
No contexto do MesaFlow, o **Kernel** não é apenas o núcleo do software, mas a **Entidade Central de Governança**.
*   **Autoridade:** O Kernel define as regras que não podem ser quebradas (ex: "Nenhum código sobe sem teste", "Nenhum pagamento ocorre sem log").
*   **Agentes:** Cada profissional (Dev, QA, DevOps) atua como um "Agente do Kernel", com permissões e responsabilidades limitadas pelo protocolo.

## 2. Protocolo INDA
O ciclo de vida de qualquer tarefa ou feature deve seguir estritamente as quatro fases do INDA:

### I - INSPECTION (Inspeção)
Antes de agir, o agente deve analisar o estado atual.
*   *Exemplo:* O Dev verifica se a tabela de banco já existe antes de criar uma migration.
*   *Artefato:* Relatório de Diagnóstico.

### N - NORMALIZATION (Normalização)
O agente deve padronizar o ambiente para garantir que a ação seja determinística.
*   *Exemplo:* O QA reseta o banco de dados para um estado conhecido antes de rodar os testes.
*   *Artefato:* Scripts de Setup/Seed.

### D - DECISION (Decisão)
Baseado na inspeção, o agente escolhe o caminho de execução aprovado.
*   *Exemplo:* O Arquiteto decide usar Redis em vez de Memória RAM para suportar múltiplos workers.
*   *Artefato:* ADR (Architecture Decision Record).

### A - ACTION (Ação)
A execução técnica propriamente dita, que deve ser atômica e reversível.
*   *Exemplo:* O DevOps aplica o deploy.
*   *Artefato:* Logs de Execução e Rollback Plan.

## 3. Agentes e Responsabilidades
Cada papel profissional é mapeado como um Agente no sistema de governança:
*   **Agente Architect:** Define as regras do Kernel.
*   **Agente Builder (Dev):** Expande o Kernel seguindo as regras.
*   **Agente Guardian (QA/SRE):** Verifica se o Kernel está sendo respeitado.