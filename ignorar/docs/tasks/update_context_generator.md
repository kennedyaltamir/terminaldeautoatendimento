# Task: Atualização do Gerador de Contexto (v7.0)

## Contexto
Melhoria da ferramenta de handover para suportar exclusões customizadas e garantir um arquivo de contexto limpo para a próxima fase do projeto.

## Decisões Técnicas
- **Pasta `ignore_context`:** Implementada como diretório de exclusão física. Qualquer arquivo movido para lá é ignorado pelo script.
- **Filtros de Mídia:** Adicionada exclusão automática para pastas de screenshots e sons gerados.
- **Handover Optimization:** A `PRIORITY_ORDER` foi ajustada para colocar os documentos de arquitetura mobile e o contexto mestre no topo do arquivo.

## Arquivos Afetados
- `gerartxt.py`

## Política de Testes
[TEST_EXEMPT: Script de infraestrutura validado por execução direta. O sucesso é confirmado pela geração correta do arquivo `todososarquivos.txt` sem os arquivos ignorados.]
