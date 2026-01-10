# DOMAIN: FRONTEND
# TASK_TYPE: KERNEL_INDA
# STATUS: IN_PROGRESS

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-UX-01
TITLE: Voice Ordering Interface para KDS (Web Speech API)
OWNER: Executor Kernel
PRIORITY: MÉDIA
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O KDS (Kitchen Display System) é operado exclusivamente via toque na tela.
- Em ambientes de cozinha, as mãos dos operadores estão frequentemente ocupadas ou sujas, dificultando a interação física.
- Não existe suporte a comandos de voz.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- O KDS Web (`/admin/[slug]/kitchen`) escuta comandos de voz simples.
- Comandos suportados:
    - "Pedido [Número] Pronto" -> Avança status para Ready.
    - "Pedido [Número] Entregue" -> Avança status para Delivered.
- Feedback visual quando o microfone está ativo e quando um comando é reconhecido.
- Utilização da **Web Speech API** nativa do navegador (sem dependências pesadas de nuvem).

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Criação do hook `frontend/src/hooks/useVoiceControl.ts`.
- Integração do hook na página `frontend/src/app/admin/[slug]/kitchen/page.tsx`.
- Indicador de UI (Microfone) no header do KDS.
- Script de validação estática (verificação de código).

### EXCLUI
- Suporte a navegadores que não implementam Web Speech API (ex: Firefox Desktop padrão).
- Processamento de linguagem natural complexo (apenas regex simples).
- Versão Mobile Nativa (React Native Voice) nesta task.

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- API: `window.SpeechRecognition` ou `window.webkitSpeechRecognition`.
- Idioma: `pt-BR`.
- UX: O reconhecimento deve ser contínuo ou ativado por "Wake Word" (simplificado para botão de toggle por enquanto para evitar ruído).

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- `frontend/src/app/admin/[slug]/kitchen/page.tsx`

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `frontend/src/hooks/useVoiceControl.ts`
- `frontend/src/app/admin/[slug]/kitchen/page.tsx` (Atualizado)
- `scripts/validation/verify_TASK-UX-01.py`

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [ ] Hook detecta suporte do navegador.
- [ ] Hook retorna transcrição em tempo real.
- [ ] KDS processa comando "Pedido X Pronto" e chama a função de update.
- [ ] UI mostra estado do microfone (Ouvindo/Pausado).

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/validation/verify_TASK-UX-01.py`
