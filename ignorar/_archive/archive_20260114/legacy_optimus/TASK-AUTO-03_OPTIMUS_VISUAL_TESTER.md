# 🤖 Task: Optimus Visual Tester (v5.0)
## Objetivo
Substituir o antigo explorador de UI por um sistema robusto, orientado a evidências e com comportamento "humano" para geração de vídeos de auditoria.
## Melhorias Implementadas
1.  **Estrutura de Pastas Organizada:** `testesvisuais/[pagina]/[docs|imgs|videos]`.
2.  **Vídeos Individuais:** Cada página tem seu próprio vídeo de navegação, facilitando o debug.
3.  **Rolagem Suave:** O script rola a página suavemente para garantir que o vídeo capture todo o conteúdo e dispare lazy loads.
4.  **Interação Realista:** Preenchimento de formulários com dados falsos (Faker) baseados no tipo do input (email, telefone, senha).
5.  **Análise de Acessibilidade:** Heurísticas automáticas para detectar baixo contraste e falta de labels.
6.  **Relatório Rico:** Markdown detalhado com links para as evidências visuais.
## Como Executar
```bash
# 1. Instalar dependências novas
pip install faker playwright

# 2. Mapear rotas (se houver mudanças)
python scripts/automation/map_routes.py

# 3. Executar o Optimus Tester
python scripts/automation/optimus_visual_tester.py
```
## Artefatos
- Relatórios em `testesvisuais/`
- Logs de erro de console capturados.
- Screenshots de cada elemento interativo destacado.
