# 📱 DashboardPage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/dashboard`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Visão tática da operação. Decisões baseadas em dados em tempo real.

## 2. Estrutura e Layout
**Containers:** div

## 3. Elementos Interativos
- **BUTTON**: Tentar novamente — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*

## 4. Estados e Comportamentos
**Estados Detectados:** interactive, loading, error

## 5. Fluxos de Navegação
1. Executar -> fetchMetrics
1. Executar -> p
1. Executar -> handleExport

## 6. Observações Críticas
Dados pesados devem ser carregados via Promise.all. Cache de SWR/React Query recomendado.

---
*Gerado automaticamente em 2026-01-18T08:27:18.861292*
