# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-10 18:50:00
# 🤖 Task: Enterprise UI Crawler & Documentation Suite
## Objetivo
Criar uma suíte de automação que mapeie, teste e documente visualmente toda a interface do MesaFlow, gerando artefatos de nível executivo para apresentação comercial e auditoria técnica.
## Componentes
1.  **Map Routes (`map_routes.py`):** Analisa estaticamente a estrutura do Next.js para descobrir todas as páginas possíveis.
2.  **Enterprise Explorer (`enterprise_ui_explorer.py`):** Robô inteligente que navega, interage (hover/click), grava vídeo e tira screenshots de cada elemento interativo.
3.  **Auto Fix Reporter (`auto_fix_reporter.py`):** Gera scripts de correção baseados nas falhas encontradas.
## Artefatos Gerados
- `testesvisuais/run_{ID}/fotos/`: Screenshots de cada botão com highlight.
- `testesvisuais/run_{ID}/videos/`: Gravação da sessão de teste.
- `testesvisuais/run_{ID}/fotos/todososbotoeseclicaveis.md`: Relatório executivo em tabela.
## Como Executar
```bash
# 1. Mapear Rotas
python scripts/automation/map_routes.py
# 2. Executar Explorador (Gera Vídeos e Relatório)
python scripts/automation/enterprise_ui_explorer.py
# 3. Gerar Sugestão de Correção
python scripts/automation/auto_fix_reporter.py
```
