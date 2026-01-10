# 🎓 Relatório de Lições Aprendidas (Lessons Learned)

> **Ciclo:** Fases 1 a 8
> **Objetivo:** Registrar conhecimento empírico para evitar erros futuros.

## 1. O que funcionou bem? (Keep Doing)
- **Monolito Modular:** A decisão de não usar microserviços prematuramente salvou meses de configuração de DevOps e custos de infraestrutura.
- **Dexie.js para Offline:** A abstração do IndexedDB provou-se robusta para manter a operação de restaurantes em áreas de sombra.
- **FastAPI + Pydantic:** A validação de dados automática reduziu drasticamente bugs de runtime e erros de tipo.
- **Playwright E2E:** Os testes visuais pegaram regressões críticas de UI que testes unitários deixaram passar.

## 2. O que poderia ter sido melhor? (Improvements)
- **Gestão de Estado Mobile:** Inicialmente tentamos replicar a lógica Web no Mobile. Aprendemos que o ciclo de vida nativo exige stores mais persistentes e resilientes (Zustand + Persist).
- **WebSockets em Memória:** A primeira versão usava memória RAM. Quando escalamos para 2 workers no Render, a comunicação quebrou. A migração para Redis foi obrigatória e deveria ter sido feita antes.
- **Float para Dinheiro:** Tivemos problemas de arredondamento no início. A migração para `Decimal` foi dolorosa mas necessária. **Regra de Ouro:** Nunca usar Float para moeda.

## 3. Desafios Técnicos Superados
- **Integração iFood:** A complexidade de mapear produtos externos para internos foi resolvida com uma tabela de `external_ids` e um serviço de Polling robusto.
- **Impressão Bluetooth:** A fragmentação de drivers Android foi um pesadelo. A solução via protocolo `rawbt:` e geração de binário ESC/POS no backend unificou a experiência.

## 4. Recomendações para Próximas Fases
1.  **Mobile First:** Qualquer nova feature operacional deve ser desenhada primeiro para a tela do celular.
2.  **Observabilidade:** Logs estruturados são vitais. O `LoggerService` deve ser expandido.
3.  **Feature Flags:** Use para tudo. Deploy não é Release.
