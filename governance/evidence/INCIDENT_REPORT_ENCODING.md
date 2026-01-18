# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-16 20:28:00
# 🩺 Relatório de Incidente: UnicodeDecodeError em Scripts de Diagnóstico

## 1. Descrição
O script `systemic_truth_engine.py` sofreu um crash fatal durante a fase de meta-auditoria ao tentar ler arquivos de script que continham caracteres UTF-8 não suportados pelo encoding padrão do Windows (`cp1252`).

## 2. Causa Raiz
Omissão do parâmetro `encoding='utf-8'` em chamadas de leitura de arquivo (`Path.read_text()`) e abertura de streams (`open()`). O Python 3.13 no Windows não assume UTF-8 como padrão para operações de arquivo, resultando em falha ao encontrar bytes como `0x8f`.

## 3. Impacto
- Interrupção do rito de auditoria de segunda ordem.
- Cegueira temporária sobre o estado real de compilação do sistema.

## 4. Ação Corretiva
- Refatoração do `SystemicTruthEngine` para forçar UTF-8 em todas as operações de IO.
- Implementação de `io.TextIOWrapper` para garantir que a saída do terminal também suporte caracteres especiais.

## 5. Veredito
Incidente resolvido via Hardening de IO. O sistema de diagnóstico agora é resiliente a ambientes Windows.

