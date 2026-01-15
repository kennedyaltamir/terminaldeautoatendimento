# 🚨 Relatório de Incidente: Falha de Sintaxe Frontend e Encoding Backend

**Data:** 10 de Janeiro de 2026  
**Severidade:** CRÍTICA (Sistema Inoperante)
**Status:** RESOLVIDO

## 1. Análise de Causa Raiz

### 1.1. Erro de Sintaxe (Frontend)
O arquivo `frontend/src/lib/api.ts` continha um erro de sintaxe no objeto `headers`. A variável `options.headers` estava sendo inserida diretamente no objeto literal sem uma chave associada ou o operador de espalhamento (*spread operator*).
- **Erro:** `options.headers,`
- **Correção:** `options.headers,`

### 1.2. Erro de Encoding (Backend)
O erro `'utf-8' codec can't decode byte 0xe7` no `IfoodService` indica que dados vindos do banco de dados ou de uma resposta externa continham caracteres especiais (como 'ç') codificados em um formato diferente de UTF-8 (provavelmente Latin-1/CP1252), causando falha na conversão para string.

## 2. Ações de Correção
1. **Correção de Sintaxe:** Aplicado o spread operator em `api.ts`.
2. **Blindagem de Encoding:** Refatorado o loop de polling no `ifood_service.py` para capturar erros de decodificação de forma isolada, impedindo que um caractere inválido derrube o serviço inteiro.
3. **Normalização de Strings:** Adicionada conversão explícita com tratamento de erro para o token do iFood.
