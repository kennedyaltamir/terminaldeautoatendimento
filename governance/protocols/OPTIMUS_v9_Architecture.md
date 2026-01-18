# DOMAIN: GOVERNANCE
# TASK_TYPE: ARCHITECTURE_DEFINITION
# STATUS: ACTIVE
# VERSION: 9.1 (Neuro Evolution Extended)

# 🧠 ANEXO — ARQUITETURA DO OPTIMUS v9.1 (Neuro Evolution System Extended)

Este documento constitui a especificação técnica definitiva, nível industrial, do sistema **OPTIMUS v9.1**. Ele detalha os algoritmos, fluxos de dados, modelos cognitivos e a infraestrutura de autoaprendizagem que governa a automação de QA do MesaFlow.

---

## 1. 🧠 Arquitetura Cognitiva Completa

O OPTIMUS v9.1 não é um script linear; é um sistema cibernético de feedback fechado. A informação flui ciclicamente entre percepção, decisão, ação e aprendizado.

### 1.1. Fluxo de Dados Macro
```mermaid
graph TD
    A[Percepção (DOM Scan)] -->|Elementos| B(Neuro Evolution Engine)
    B -->|Consulta Histórico| C{Genoma Evolutivo}
    C -->|Estratégia Dominante| B
    B -->|Comando| D[Hyper Reactive Click Engine]
    D -->|Ação Física| E[Interface (Browser)]
    E -->|Reação/Mutação| F[Evidence 2.0]
    F -->|Dados Forenses| G[Auditoria Cognitiva]
    G -->|Feedback de Sucesso/Falha| H[Neuro Learning]
    H -->|Atualização de Pesos| C
```

### 1.2. Comunicação Inter-Módulo
1.  **Falhas → Genoma:** Quando uma interação falha, o erro é classificado e registrado no nó específico do elemento no JSON do Genoma.
2.  **Genoma → Neuro-Evolution:** Ao encontrar um elemento conhecido, o motor carrega os pesos das estratégias anteriores para decidir a próxima ação (Exploit vs Explore).
3.  **Neuro → Click Engine:** O cérebro envia um pacote de instrução contendo: `TargetLocator`, `StrategyType`, `ForceLevel`, `ExpectedReaction`.
4.  **Evidence → Auditoria:** Screenshots e logs de diff de DOM são enviados para o módulo de auditoria para calcular o Score de Estabilidade.

---

## 2. ⚡ Hyper Reactive Click Engine (HRCE)

O braço mecânico do sistema. Responsável pela execução física e recuperação de falhas de interação em milissegundos.

### 2.1. Definição Formal
*   **Input:** `Locator`, `Intention`, `StrategyConfig`
*   **Output:** `InteractionResult` (Success/Fail, ReactionTime, DOMDiffHash)
*   **Side Effects:** Eventos de Mouse/Teclado, Injeção de JS, Scroll.

### 2.2. Algoritmo de Execução (Pseudocódigo)
```python
def execute_interaction(element, strategy):
    # 1. Preparação Cognitiva
    if strategy.clear_overlays:
        ModalHunter.scan_and_destroy()
    
    # 2. Cálculo de BoundingBox Cognitivo (Visível + Seguro)
    box = element.bounding_box()
    safe_point = calculate_safe_click_point(box, strategy.offset_vector)
    
    # 3. Execução Física
    try:
        if strategy.type == 'standard':
            mouse.move(safe_point)
            mouse.click()
        elif strategy.type == 'force':
            element.dispatch_event('click')
        elif strategy.type == 'human_jitter':
            mouse.move_with_noise(safe_point)
            mouse.click()
            
        # 4. Verificação Pós-Ação (Immediate Feedback)
        t0 = get_dom_hash()
        wait(strategy.reaction_timeout)
        t1 = get_dom_hash()
        
        if t0 == t1:
            raise GhostClickError("UI did not react")
            
        return Success(reaction_time=t1-t0)
        
    except Exception as e:
        return Failure(reason=e, context=capture_context())
```

### 2.3. Matriz de Fallback (Reatividade)
| Erro Detectado | Estratégia de Recuperação | Penalidade no Genoma |
| :--- | :--- | :--- |
| `TimeoutError` | Aumentar `timeout` + Scroll Element to Center | -0.1 |
| `InterceptedError` | Acionar `ModalHunter` + Retry | -0.2 |
| `GhostClick` | Mutação para `ForceClick (JS)` | -0.5 |
| `DetachedError` | Re-query no DOM (Stale Element Refresh) | 0.0 (Neutro) |

---

## 3. 📸 Evidence 2.0 (Forensic Visual System)

Sistema de documentação visual que prova a execução e facilita o debug humano.

### 3.1. Pipeline Interno
1.  **Pre-Action:**
    *   Captura coordenadas do elemento.
    *   Injeta CSS: `outline: 3px solid #ea580c; box-shadow: 0 0 15px #ea580c;`.
    *   Screenshot `_before.png`.
2.  **Action:**
    *   Gravação de vídeo com injeção de `div#laser-pointer` nas coordenadas do mouse.
    *   Animação de "Ripple" no clique.
3.  **Post-Action:**
    *   Remove CSS.
    *   Screenshot `_after.png`.
    *   Geração de `_zoom.png` (Crop 300x300px centrado no elemento).

### 3.2. Metadados (EXIF/JSON)
Cada imagem salva é acompanhada de um arquivo `.meta.json` contendo:
*   `timestamp`: ISO 8601.
*   `selector`: Caminho CSS único.
*   `strategy_used`: Qual método do HRCE foi usado.
*   `coordinates`: {x, y}.
*   `viewport`: {width, height}.

---

## 4. 🧭 Nielsen Heuristic Engine

Motor de análise estática e dinâmica baseado nas 10 Heurísticas de Usabilidade.

### 4.1. Tabelas Formais de Análise
| Heurística | Fórmula de Detecção | Exemplo de Falha | Registro |
| :--- | :--- | :--- | :--- |
| **Visibilidade do Status** | `if action_duration > 500ms AND no_spinner_detected` | Clique em "Salvar" congela a tela sem feedback. | `UX_FAIL_H1` |
| **Prevenção de Erros** | `if input_type == 'email' AND no_validation_on_blur` | Campo de e-mail aceita texto sem @. | `UX_FAIL_H5` |
| **Reconhecimento** | `if button_has_icon AND no_aria_label AND no_text` | Botão apenas com ícone sem descrição. | `UX_FAIL_H6` |
| **Estética Minimalista** | `if text_density > 80% OR contrast_ratio < 4.5` | Texto cinza claro em fundo branco. | `UX_FAIL_H8` |

---

## 5. 🔁 Ciclos Adaptativos

O sistema de resiliência que impede que o teste falhe por instabilidades transientes.

### 5.1. Modelo Decisório Ponderado
Quando uma interação falha, o sistema calcula o "Custo de Adaptação":
$$ Custo = (TentativasAtuais \times 1.5) + RiscoDaEstratégia $$

Se $Custo < LimiteGlobal$, uma mutação é tentada.

### 5.2. Catálogo de Mutações
1.  **Mutação Temporal:** Adicionar `wait(500ms)` antes da ação.
2.  **Mutação Espacial:** Aplicar `offset(x=5, y=5)` no clique.
3.  **Mutação Estrutural:** Buscar elemento pelo `parent` ou `xpath` alternativo.
4.  **Mutação de Evento:** Disparar `focus()` antes de `click()`.

---

## 6. 🧬 Genoma Evolutivo

O banco de dados de conhecimento persistente do OPTIMUS.

### 6.1. Estrutura do DNA (`genoma_ui.json`)
Para cada elemento único (identificado por hash de seletor + contexto), o sistema armazena:
*   **ID Genético:** Hash único.
*   **Histórico de Falhas:** Contador de erros por tipo.
*   **Estratégia Dominante:** O método de interação que teve maior taxa de sucesso nas últimas 10 execuções.
*   **Perfil de Latência:** Tempo médio de resposta esperado.

### 6.2. Evolução Entre Execuções
Ao iniciar uma nova bateria de testes (Run), o OPTIMUS carrega o Genoma.
*   Se um elemento tem histórico de falha com clique padrão, o sistema já inicia usando a **Estratégia Dominante** (ex: JS Force), pulando a tentativa ingênua.

---

## 7. 🧠 Neuro Evolution Engine

O cérebro central que coordena a aprendizagem.

### 7.1. Lógica de Reforço (Reinforcement Learning)
Para cada interação $i$ usando estratégia $s$:
*   Se **Sucesso**: $Peso(s) = Peso(s) + (1 - Peso(s)) \times TaxaAprendizado$
*   Se **Falha**: $Peso(s) = Peso(s) \times (1 - TaxaPunição)$

*Parâmetros:* `TaxaAprendizado = 0.1`, `TaxaPunição = 0.3` (O sistema pune falhas mais severamente do que premia sucessos).

### 7.2. Diagrama de Fluxo Neural
```text
[Situação: Botão Login falhou com Standard]
       ⬇
[Consulta Genoma: Próxima melhor estratégia?]
       ⬇
[Seleção: Force Click (Peso 0.6)]
       ⬇
[Execução: Sucesso]
       ⬇
[Neuro Update: Standard(Peso ↓), Force(Peso ↑)]
       ⬇
[Nova Estratégia Dominante para Login: Force Click]
```

---

## 8. 🗂 Integração com Testes Visuais

### 8.1. Estrutura de Diretórios
O sistema gera automaticamente:
```text
testesvisuais/
├── _global/
│   ├── genoma_ui.json (O Cérebro)
│   ├── relatorio_global.md
│   └── inventario_full.json
└── run_YYYYMMDD_HHMMSS/
    ├── [nome_da_pagina]/
    │   ├── docs/ (Relatórios MD)
    │   ├── imgs/ (Prints Before/After/Full)
    │   │   └── elements/ (Prints Zoom)
    │   └── videos/ (WebM com Laser)
```

### 8.2. Indexação
Cada evidência recebe um ID único (`run_id` + `element_hash`) que é linkado no Relatório Markdown, permitindo rastreabilidade total.

---

## 9. 🔧 Parâmetros Ajustáveis (Configuração)

O OPTIMUS v9.1 expõe knobs de controle para ajuste fino.

| Parâmetro | Default | Descrição |
| :--- | :--- | :--- |
| `SLOW_MO` | 300ms | Delay artificial entre ações para visibilidade humana. |
| `MAX_RETRIES` | 3 | Número máximo de ciclos adaptativos por elemento. |
| `INTERACTION_DELAY` | 500ms | Tempo de espera pós-ação para estabilização do DOM. |
| `GHOST_CHECK_INTERVAL` | 150ms | Tempo para verificar mudança de hash do DOM. |
| `DESTRUCTIVE_MODE` | False | Se True, executa cliques em botões de "Excluir". |
| `LEARNING_RATE` | 0.1 | Fator de ajuste de pesos do Neuro Engine. |

### Modos de Execução (CLI)
*   **A (Preciso):** `SLOW_MO=100`, `MAX_RETRIES=1`. Foco em velocidade e precisão.
*   **B (Explorador):** Tenta caminhos randômicos.
*   **C (Cognitivo):** `SLOW_MO=500`. Simula leitura humana.
*   **D (Brutal):** `DESTRUCTIVE=True`. Testa resiliência a erros.
*   **E (Híbrido):** Ajusta parâmetros dinamicamente baseado na complexidade da página.

---

## 10. 🧨 Casos de Erro Detalhados

### 10.1. Clique Fantasma (Ghost Click)
*   **Causa:** Event listener não atrelado ou bloqueado por lógica de JS.
*   **Diagnóstico:** Clique ocorre, sem erro, mas DOM Hash não muda.
*   **Recuperação:** Tentar `Force Click` -> Tentar `DispatchEvent`.
*   **Genoma:** Marca elemento como "Low Responsiveness".

### 10.2. Interceptação (Overlay)
*   **Causa:** Modal, Toast ou Backdrop cobrindo o elemento.
*   **Diagnóstico:** Erro do Playwright `element is not clickable`.
*   **Recuperação:** Acionar `ModalHunter` (busca e fecha overlays conhecidos) -> Retry.

### 10.3. Mutação de DOM (Stale Element)
*   **Causa:** React re-renderizou o componente entre a detecção e o clique.
*   **Diagnóstico:** `StaleElementReferenceError`.
*   **Recuperação:** Re-query do seletor no DOM atual -> Retry.

---

## 11. 📊 Painéis Globais

### 11.1. Estabilidade (Stability Score)
$$ Score = 100 - (FalhasCriticas \times 10) - (Retries \times 2) - (UXWarnings \times 1) $$

### 11.2. Complexidade
$$ Complexidade = (NumElementos \times 0.5) + (ProfundidadeDOM \times 0.2) $$

### 11.3. Regressão
Compara o `Stability Score` da execução atual com a média móvel das últimas 5 execuções no Genoma. Queda > 10% dispara alerta vermelho.

---

**OPTIMUS v9.1 — Arquitetura Cognitiva Completa Registrada.**