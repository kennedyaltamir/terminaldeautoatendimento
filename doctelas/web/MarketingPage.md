# 📱 MarketingPage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/marketing`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Estrutura e Layout
**Containers:** div

## 3. Elementos Interativos
- **BUTTON**: N/A — *Ação: onClick*
- **INPUT**: N/A — *Ação: onChange* (type:number)
- **BUTTON**: Salvar Configuração — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **A**: Configurar — *Ação: navigation*
- **INPUT**: Ex: Desconto de Verão — *Ação: onChange*
- **INPUT**: VERAO10 — *Ação: onChange*
- **SELECT**: N/A — *Ação: onChange*
- **INPUT**: 10 — *Ação: onChange* (type:number)
- **INPUT**: N/A — *Ação: onChange* (type:number)
- **INPUT**: Ilimitado — *Ação: onChange* (type:number)
- **BUTTON**: Criar Promoção — *Ação: onClick*

## 4. Estados e Comportamentos
**Estados Detectados:** interactive, loading, error, empty

## 5. Fluxos de Navegação
1. Executar -> handleTrainAI
1. Executar -> loyalty
1. Executar -> handleSaveLoyalty
1. Navegar -> settings
1. Executar -> promoForm.name
1. Executar -> promoForm.code
1. Executar -> promoForm.discount_type
1. Executar -> promoForm.discount_value
1. Executar -> promoForm.min_order_value
1. Executar -> promoForm.usage_limit
1. Executar -> handleCreatePromo

## 6. Observações Críticas
Nenhuma observação crítica registrada automaticamente.

---
*Gerado automaticamente em 2026-01-18T08:27:18.863146*
