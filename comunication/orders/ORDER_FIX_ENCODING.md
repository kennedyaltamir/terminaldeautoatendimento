
# ORDEM DE SERVIÇO: CORREÇÃO DE COMPATIBILIDADE WINDOWS
**ID:** ORD-001
**Prioridade:** IMEDIATA
**Alvo:** Scripts Python de Manutenção e Validação

## Contexto
A execução em ambiente Windows falha devido à tentativa de imprimir caracteres Unicode (Emojis) em um terminal configurado com `cp1252`.

## Diretriz Técnica
Todos os scripts Python devem ser robustos quanto ao encoding do terminal.

## Ação Requerida
Aplicar o seguinte padrão de correção no início de todos os scripts suscetíveis (`system_integrity_check.py`, `master_readiness_check.py`, etc.):

```python
import sys
import io

# Forçar UTF-8 no stdout para compatibilidade Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

Alternativamente, remover caracteres não-ASCII de logs críticos se a reconfiguração do stdout não for viável ou segura para o contexto.

## Critério de Aceite
O comando `python scripts/maintenance/system_integrity_check.py` deve executar até o fim no terminal Windows sem levantar `UnicodeEncodeError`.

