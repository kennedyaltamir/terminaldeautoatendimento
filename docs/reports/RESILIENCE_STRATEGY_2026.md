
# 🛡️ Estratégia de Resiliência Enterprise 2026

## 1. Camada de Dados (RLS)
O isolamento não é mais lógico (Python), mas físico (PostgreSQL Engine). 
- **Falha Protegida:** Se um desenvolvedor esquecer o `filter(company_id)`, o banco retornará vazio.

## 2. Camada de IA (RFC-011)
O motor de IA é tratado como um "cidadão de segunda classe" em termos de prioridade de recursos.
- **Timeout:** 30s.
- **Memory:** Dataset limitado a 10k linhas.
- **Fallback:** Se a predição falhar, o sistema assume a média móvel dos últimos 7 dias.

## 3. Observabilidade
Todo disparo de fallback de IA deve gerar um log de severidade `WARN` para auditoria de precisão do modelo.

