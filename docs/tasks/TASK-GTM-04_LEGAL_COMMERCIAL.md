# DOMAIN: FRONTEND
# TASK_TYPE: KERNEL_INDA
# STATUS: OPEN

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-GTM-04
TITLE: Compliance Legal & Comercial
OWNER: Executor Kernel
PRIORITY: MÉDIA (GTM)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O site não possui páginas públicas de "Termos de Uso" e "Política de Privacidade".
- Não há link visível para suporte ou contato comercial direto no rodapé.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Rotas `/terms` e `/privacy` criadas no Frontend (Next.js).
- Conteúdo jurídico genérico (template SaaS) inserido.
- Rodapé atualizado com links legais e CNPJ.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Criação de `frontend/src/app/terms/page.tsx`.
- Criação de `frontend/src/app/privacy/page.tsx`.
- Atualização de `frontend/src/components/landing/Footer.tsx`.

### EXCLUI
- Consultoria jurídica real (usaremos texto padrão de mercado).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Framework: Next.js 14 (App Router).
- Estilo: Tailwind CSS (Prose/Typography).

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- `frontend/src/components/landing/Footer.tsx`

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- Páginas legais criadas.
- Footer atualizado.
- Script de validação de rotas.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [ ] Rota `/terms` retorna 200 OK e contém texto "Termos de Uso".
- [ ] Rota `/privacy` retorna 200 OK e contém texto "Política de Privacidade".
- [ ] Footer contém links funcionais para ambas as páginas.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/validation/verify_TASK-GTM-04.py`
RESULTADO_ESPERADO: "Legal routes accessible."

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Deletar pastas `frontend/src/app/terms` e `frontend/src/app/privacy`.
- Reverter `Footer.tsx`.
