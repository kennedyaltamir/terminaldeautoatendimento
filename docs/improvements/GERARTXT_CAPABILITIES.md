# 🛠️ Capacidades e Roadmap: gerartxt.py

Este documento cataloga as funcionalidades atuais da ferramenta de geração de contexto e as melhorias planejadas para as próximas versões.

## 🚀 Funcionalidades Atuais (v5.1 - Ironclad)

1.  **Auditoria Visual Exaustiva:** Navegação automatizada por todas as abas do Admin (Fiscal, Impressão, etc.) e interfaces operacionais (KDS/Mobile) gerando evidências em WebP.
2.  **Filtragem Binária Inteligente:** Bloqueio estrito de arquivos não-texto (.wav, .mp3, .png, .exe) para evitar corrupção do prompt.
3.  **Mapeamento Estrutural (Tree):** Geração de árvore ASCII completa para compreensão imediata da hierarquia do projeto.
4.  **Priorização de Contexto (Primacy Effect):** Ordenação lógica que coloca Models, Schemas e Roadmaps no início do arquivo.
5.  **Redação Automática de Segredos:** Identificação e máscara de chaves Stripe, MercadoPago e JWT via Regex.
6.  **Health Check Integrado:** Validação de disponibilidade do servidor local antes de iniciar capturas visuais.
7.  **Interface Rich CLI:** Feedback visual via tabelas, spinners e barras de progresso no terminal.
8.  **Minificação de Ruído:** Remoção de linhas em branco consecutivas e comentários redundantes.
9.  **Cálculo de Heurística de Tokens:** Estimativa em tempo real do volume de dados gerado.
10. **Isolamento de Assets:** Exclusão automática de pastas de lixo e caches (`.next`, `__pycache__`, `Copy`).

## 🔮 Roadmap de Melhorias (Top 10)

| ID | Funcionalidade | Impacto | Descrição |
|:---|:---|:---:|:---|
| 01 | **Git Delta (--changed)** | 🔥 Crítico | Incluir apenas arquivos modificados desde o último commit para tarefas rápidas. |
| 02 | **Grafo de Dependências** | 🧠 Alto | Gerar um mapa de "quem importa quem" no cabeçalho do arquivo. |
| 03 | **Smart Chunking** | 📦 Alto | Dividir o arquivo automaticamente se ultrapassar 500k tokens. |
| 04 | **Extrator de Props** | 🎨 Médio | Resumo automático das interfaces de componentes React (Storybook em texto). |
| 05 | **Captura Paralela** | ⚡ Médio | Executar capturas do Playwright em paralelo para reduzir tempo de execução. |
| 06 | **Detecção de Código Morto** | 🧹 Médio | Alertar sobre arquivos que não são importados por nenhum outro arquivo. |
| 07 | **Snapshot de Latência** | ⏱️ Baixo | Registrar o tempo de resposta de cada página durante a auditoria visual. |
| 08 | **Menu Interativo** | 🖱️ Baixo | Menu CLI para selecionar módulos específicos (ex: "Apenas Backend"). |
| 09 | **Image-to-Text (Alt)** | 👁️ Médio | Incluir descrições textuais das screenshots usando modelos de visão. |
| 10 | **Exportação para Markdown** | 📄 Baixo | Formatação otimizada para diferentes LLMs (ChatGPT vs Claude vs Gemini). |

## 📖 Como Usar
- **Completo:** `python gerartxt.py`
- **Sem Imagens:** `python gerartxt.py --no-img`
