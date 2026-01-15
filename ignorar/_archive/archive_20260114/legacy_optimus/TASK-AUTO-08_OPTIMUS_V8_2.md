# 🛡️ Task: Optimus v8.2 — Modal Resilient Edition
## Objetivo
Corrigir a falha crítica onde modais (Lead Capture, Joyride, Cookies) bloqueavam a execução do teste, causando timeouts em cascata.
## Melhorias Implementadas
1.  **Modal Hunter:** Um método `clear_overlays()` que busca ativamente por seletores de bloqueio conhecidos (`.react-joyride__overlay`, botões de fechar, backdrops) e os remove antes de interagir com a página.
2.  **Interception Recovery:** O motor de clique (`smart_click`) agora captura erros de "intercepts pointer events". Se isso ocorrer, ele aciona o Modal Hunter e tenta o clique novamente.
3.  **Pre-Flight Cleanup:** Ao carregar uma página e ao voltar de uma navegação, o script executa uma limpeza preventiva de popups.
## Como Executar
```bash
python scripts/automation/optimus_v8_2.py --mode E
```
## Resultado Esperado
O script deve ser capaz de fechar o popup de "Lead Capture" ou o tour de "Onboarding" e continuar testando os botões abaixo deles sem travar.
