# 🧬 Task: Optimus UI Genome Tester (v8.0)
## Objetivo
Criar a ferramenta definitiva de auditoria de interface, capaz de mapear, testar e documentar 100% dos elementos interativos do sistema sem limites artificiais.
## Diferenciais da v8.0 (Genome Edition)
1.  **Inventário Global:** Gera um relatório mestre (`RELATORIO_MESTRE_GENOMA.md`) que cruza dados de todas as páginas.
2.  **Sem Limites:** Itera sobre todos os elementos encontrados no DOM, usando estratégia de *Re-query* para evitar erros de elementos obsoletos (Stale Element).
3.  **Evidência Visual Rica:**
    - **Highlight:** Circula o elemento em laranja (`#ea580c`) antes do print.
    - **Full Scroll:** Captura a página inteira, garantindo que rodapés e lazy loads sejam registrados.
4.  **Heurística Contextual:** Preenche formulários com dados realistas baseados no contexto do input (Email, Senha, Telefone, Busca).
5.  **Resiliência:** Recupera o estado de navegação (Go Back) se um clique tirar o robô da página de teste.
## Como Executar
```bash
# Instalar dependências
pip install faker playwright

# Executar o Genoma
python scripts/automation/optimus_genome_tester_v8.py
```
## Artefatos Gerados
- `testesvisuais/genome_v8/RELATORIO_MESTRE_GENOMA_*.md`: O mapa completo do sistema.
- `testesvisuais/genome_v8/[pagina]/imgs/elements/`: Prints individuais de cada botão/input.
- `testesvisuais/genome_v8/[pagina]/videos/`: Vídeo completo da sessão de teste da página.
