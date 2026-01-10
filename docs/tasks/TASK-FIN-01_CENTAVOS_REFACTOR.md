# DOMAIN: FRONTEND
# TASK_TYPE: KERNEL_INDA
# STATUS: OPEN

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-FIN-01
TITLE: Refatorar Trânsito Financeiro para Centavos (Inteiros)
OWNER: Executor Kernel
PRIORITY: ALTA
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O Frontend (React/Next.js) recebe e processa valores monetários utilizando o tipo `number` (ponto flutuante de 64 bits).
- Cálculos de soma de carrinho e descontos apresentam imprecisões matemáticas (ex: 0.1 + 0.2 = 0.30000000000000004).
- O Backend utiliza `Decimal` para precisão, mas a serialização JSON converte para float ou string, perdendo a garantia de integridade no transporte.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Todos os campos de preço (`price`, `total_amount`, `discount`) trafegam na API como números inteiros representando centavos (ex: R$ 10,50 vira `1050`).
- O `CartContext.tsx` realiza todas as operações matemáticas utilizando apenas inteiros.
- A conversão para formato decimal amigável (R$) ocorre exclusivamente na camada de apresentação (componentes de UI) através de uma função utilitária `formatCurrency(value / 100)`.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Atualização dos Schemas Pydantic no Backend para converter `Decimal` em `int` na saída.
- Refatoração completa da lógica de cálculo do `CartContext.tsx`.
- Atualização de todos os componentes que exibem preços no cardápio e admin.
### EXCLUI
- Alteração do tipo de dado no PostgreSQL (Postgres continuará armazenando como `Numeric` para compatibilidade com relatórios SQL externos).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Linguagem: TypeScript e Python.
- Proibido: Uso de `parseFloat` ou `toFixed` para cálculos de negócio.
- Alterar arquitetura: NÃO.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- Arquivo `app/schemas.py`.
- Arquivo `frontend/src/context/CartContext.tsx`.
- Arquivo `frontend/src/types/index.ts`.

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- Arquivos de Schema e Contexto atualizados.
- Script de validação `scripts/validation/verify_TASK-FIN-01.py`.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [ ] O payload de criação de pedido envia o total como inteiro.
- [ ] O componente de carrinho exibe o valor correto formatado.
- [ ] Testes unitários de soma de itens com centavos complexos (ex: .33 + .67) resultam em inteiros exatos.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `npm test frontend/src/context/__tests__/CartContext.test.ts`
RESULTADO_ESPERADO: Sucesso em todos os casos de teste financeiro.

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Reverter Schemas para `float` ou `Decimal`.
- Reverter lógica do `CartContext`.

🔒 11. PROIBIÇÕES EXPLÍCITAS
## PROIBIÇÕES
- É PROIBIDO realizar divisões que resultem em floats antes da etapa final de exibição.
