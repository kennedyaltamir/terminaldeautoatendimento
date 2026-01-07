# Task: Atualização do Gerador de Contexto (v7.1)

## Contexto
Endurecimento da ferramenta de handover para garantir robustez em ambientes enterprise e suporte a transferências cognitivas de alta fidelidade.

## Decisões Técnicas
- **Implementação do `--changed`:** Agora utiliza `git status --porcelain` para identificar deltas reais.
- **Root Freeze:** O script agora fixa o diretório de trabalho na raiz do projeto para evitar caminhos inconsistentes.
- **Isolamento de Pastas:** Lógica de ignore corrigida para validar o caminho relativo completo, impedindo vazamento de pastas aninhadas.
- **Metadados de Governança:** Injeção de Domínio por arquivo e Hash SHA-256 global para validação de integridade.
- **Heurística de Tokens:** Ajustada para 3.5 chars/token para melhor precisão em blocos de código.

## Arquivos Afetados
- `gerartxt.py`

## Política de Testes
[TEST_EXEMPT: Script de infraestrutura validado por execução direta. O sucesso é confirmado pela geração do arquivo `todososarquivos.txt` com o novo header de governança e hash final.]
