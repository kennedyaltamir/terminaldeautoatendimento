# 🛡️ Upgrade Report: gerartxt.py v5.1 (Ironclad)

**Data:** 05 de Janeiro de 2026  
**Versão:** 5.1  
**Status:** Crítico - Correção de Vazamento de Binários

## 🛠️ O que foi corrigido?

1.  **Bloqueio de Binários (Ironclad Filtering):**
    - Implementada verificação de extensão antes da leitura. Arquivos `.wav`, `.mp3`, `.png` e outros binários não são mais incluídos no texto.
    - **Resultado:** Redução de ruído e economia de tokens.

2.  **Restauração da Árvore Estrutural:**
    - O script agora gera um mapa ASCII completo do projeto no topo do arquivo.
    - **Benefício:** A IA receptora entende a hierarquia de pastas instantaneamente.

3.  **Auditoria Visual Sistêmica:**
    - O motor Playwright agora percorre **todas as abas** de configuração do Admin.
    - **Cobertura:** Geral, Marketing, Financeiro, Fiscal, Impressão e Plano.

4.  **Exclusão de Pastas de Assets:**
    - Pastas como `output_sounds` e `screenshots` são ignoradas na leitura de texto, mas mapeadas na árvore.

## 📖 Como usar?

1.  Garanta que o servidor está rodando (`python run.py`).
2.  Execute `python gerartxt.py`.
3.  O arquivo `todososarquivos.txt` conterá a árvore, o código limpo e as screenshots estarão na pasta `/screenshots`.
