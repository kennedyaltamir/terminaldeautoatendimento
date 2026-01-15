# 🧬 Task: Optimus v8.1 — Hyper Reactive Mode
## Objetivo
Implementar a versão definitiva do auditor de QA, capaz de adaptar sua estratégia de interação em tempo real e gerar evidências forenses detalhadas.
## Novidades da v8.1
1.  **Hyper Reactive Click Engine:** Se um clique falhar, o sistema tenta estratégias alternativas (Offset, Force, JS) automaticamente.
2.  **Evidence 2.0:** Screenshots com highlight (círculo/borda) no elemento focado e zoom crop simulado.
3.  **Laser Pointer Tracking:** Injeção de um elemento visual no DOM que segue o mouse do robô, tornando os vídeos de auditoria compreensíveis para humanos.
4.  **Modos de Execução:** CLI com suporte a 5 modos (A-E) para diferentes níveis de agressividade e precisão.
## Como Executar
```bash
# Modo Híbrido (Recomendado)
python scripts/automation/optimus_v8_1.py --mode E

# Modo Brutal (Testa deletes)
python scripts/automation/optimus_v8_1.py --mode D
```
## Artefatos
- `testesvisuais/run_ID/[pagina]/imgs/`: Prints com highlight.
- `testesvisuais/run_ID/[pagina]/videos/`: Vídeo com laser pointer.
- `testesvisuais/_global/relatorio_global.md`: Genoma do sistema.
