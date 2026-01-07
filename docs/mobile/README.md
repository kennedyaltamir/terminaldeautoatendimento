# 📱 MesaFlow Mobile - Documentação Mestre

Este diretório centraliza toda a inteligência, histórico e especificações do aplicativo nativo MesaFlow (React Native / Expo).

## 1. Princípio de Isolamento Documental
O domínio Mobile é tratado formalmente como um cliente externo independente e autocontido. Para manter a escalabilidade e a clareza de ownership no monorepo, toda a documentação técnica, operacional e de progresso do App deve residir exclusivamente em `docs/mobile/`.

## 2. Regras BLOCKER (Proibição Absoluta)
É terminantemente proibido registrar documentação, itens de backlog ou roadmaps do domínio Mobile nos seguintes locais:
- `docs/tasks/` (Diretório legado reservado para Web/Backend)
- `docs/ROADMAP.md` (Documento legado reservado para Web/Backend)
- `docs/frontend/`
- `docs/backend/`
- Qualquer diretório ou arquivo fora de `docs/mobile/`

## 3. Obrigatoriedade de Registro
Toda task Mobile concluída **DEVE** gerar exatamente um arquivo `.md` em `docs/mobile/tasks/`, nomeado de acordo com a missão executada (ex: `2026-01-06-setup-foundation.md`). Este arquivo deve conter o contexto, decisões técnicas e arquivos afetados.

## 4. Classificação de Documentos
A estrutura de pastas segue a seguinte taxonomia:

- **`tasks/`**: Histórico cronológico de execução, entregas e logs de progresso.
- **`decisions/`**: Architectural Decision Records (ADRs) específicos do ambiente nativo e mobile-first.
- **`setup/`**: Guias de configuração de ambiente de desenvolvimento, emuladores, certificados e infraestrutura de build (EAS).
- **`architecture/`**: Definição de padrões, diagramas de fluxo, navegação e contratos de consumo de API/WebSockets.

## 5. Recomendações de Nomenclatura (Opcional)
Para facilitar a rastreabilidade em históricos extensos e missões paralelas, recomenda-se opcionalmente o uso de nomenclatura semântica e versionada para arquivos em `tasks/`.

### Benefícios:
- Identificação imediata da fase e missão (ex: Fase 10, Missão 1).
- Ordenação lógica superior à cronológica em ambientes de desenvolvimento acelerado.
- Facilidade de referência cruzada com Roadmaps internos do Mobile.

### Exemplos Recomendados:
- `mobile_10_1_setup_foundation.md`
- `mobile_10_2_assets_placeholders.md`
- `mobile_11_auth_infra.md`
- `mobile_12_offline_sync_strategy.md`

**Nota:** Esta padronização é uma sugestão de boa prática e **NÃO** invalida o uso do padrão cronológico simples (`2026-01-06-nome.md`), que permanece válido e suportado.

## 6. Diretriz de Futuro
A partir da **Missão 11 (Auth Mobile)**, toda e qualquer documentação, log de decisão ou registro de progresso relacionado ao domínio Mobile deve ser alocado exclusivamente dentro deste diretório (`docs/mobile/`), preferencialmente na subpasta `tasks/`.

---
*Diretriz de Governança v1.1 — Janeiro de 2026*

---
*Diretriz de Governança v1.0 — Janeiro de 2026*
# 📱 MesaFlow Mobile - Documentação Mestre

## 1. Status Atual: Fase 10 (KDS Nativo)
O aplicativo mobile evoluiu de um protótipo para um **Terminal de Operação Ativa**. 

### Marcos Alcançados:
- **Infraestrutura:** Autenticação semântica, interceptores de refresh e barreira de renderização (AuthGate).
- **Realtime:** Sincronização via WebSocket com reconciliação de estado.
- **Inteligência:** Motor de SLA determinístico e Engine de Alertas Sensoriais (Vibração) com controle de cooldown.
- **Identidade:** Bootstrap de sessão dinâmico baseado em claims de JWT.

## 2. Arquitetura de Atenção (Missão 21/22)
O app utiliza um **Global Clock** (pulso de 5s) para orquestrar:
1. Atualização de timers de pedidos.
2. Re-cálculo de status de SLA (OK, WARNING, CRITICAL, BREACHED).
3. Re-ordenação da fila por prioridade.
4. Disparo de alertas físicos (Vibração) conforme a política de interrupção.

## 3. Backlog de Missões Pendentes
- **Missão 23:** Controles do Operador (Silent Mode).
- **Missão 24:** Resiliência de Rede (Exponential Backoff & Re-sync).
- **Missão 25:** Gestão de Erros Operacionais.
- **Missão 26:** Observabilidade (Logs estruturados).
- **Missão 27:** Polimento de UX e Release.

---
*Versão 1.5 — Janeiro de 2026*
# 📱 MesaFlow Mobile - Documentação Mestre

## 1. Status Atual: Fase 10 (KDS Nativo)
O aplicativo mobile evoluiu de um protótipo para um **Terminal de Operação Ativa**. 

### Marcos Alcançados:
- **Infraestrutura:** Autenticação semântica, interceptores de refresh e barreira de renderização (AuthGate).
- **Realtime:** Sincronização via WebSocket com reconciliação de estado.
- **Inteligência:** Motor de SLA determinístico e Engine de Alertas Sensoriais (Vibração) com controle de cooldown.
- **Identidade:** Bootstrap de sessão dinâmico baseado em claims de JWT.

## 2. Arquitetura de Atenção (Missão 21/22)
O app utiliza um **Global Clock** (pulso de 5s) para orquestrar:
1. Atualização de timers de pedidos.
2. Re-cálculo de status de SLA (OK, WARNING, CRITICAL, BREACHED).
3. Re-ordenação da fila por prioridade.
4. Disparo de alertas físicos (Vibração) conforme a política de interrupção.

## 3. Backlog de Missões Pendentes
- **Missão 23:** Controles do Operador (Silent Mode).
- **Missão 24:** Resiliência de Rede (Exponential Backoff & Re-sync).
- **Missão 25:** Gestão de Erros Operacionais.
- **Missão 26:** Observabilidade (Logs estruturados).
- **Missão 27:** Polimento de UX e Release.

---
*Versão 1.5 — Janeiro de 2026*
