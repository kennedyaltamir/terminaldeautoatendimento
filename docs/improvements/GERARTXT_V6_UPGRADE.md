# 🚀 Upgrade Report: gerartxt.py v6.0 (Ultra-Architect)

**Data:** 05 de Janeiro de 2026  
**Versão:** 6.0  
**Status:** Produção - Handover Inteligente

## 🌟 Novas Funcionalidades

1.  **Git Delta (--changed):** Agora você pode gerar contexto apenas dos arquivos que modificou. Perfeito para correções rápidas.
2.  **Dependency Graph:** O script mapeia quem importa quem, ajudando a IA a entender a hierarquia de chamadas.
3.  **Smart Chunking:** Se o projeto crescer demais, o script divide o arquivo em partes de 450k tokens automaticamente.
4.  **Props Extractor:** Gera um resumo de todas as interfaces de componentes React no final do arquivo.
5.  **Captura Paralela:** Playwright agora abre múltiplas abas simultaneamente para screenshots mais rápidas.
6.  **Dead Code Detection:** Identifica arquivos que não estão sendo usados (não importados).
7.  **Latency Snapshot:** Registra o tempo de carregamento de cada tela para análise de performance.
8.  **Auto-Redact:** Remove chaves de API e segredos automaticamente antes de salvar.
9.  **Markdown Optimized:** Saída formatada para máxima legibilidade em LLMs.
10. **Rich Progress:** Interface visual moderna com barra de progresso e tabelas de resumo.

## 📖 Como usar?
- `python gerartxt.py` (Completo)
- `python gerartxt.py --changed` (Apenas o que mudou)
- `python gerartxt.py --no-img` (Apenas texto, ultra rápido)
