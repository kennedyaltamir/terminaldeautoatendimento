# Task: Correção da Validação de Setup Mobile

## Contexto
O script de validação de infraestrutura mobile (`verify_mobile_setup.py`) apresentava inconsistências com o setup inicial aprovado, exigindo a existência da pasta `mobile/assets` e validando caminhos incorretos no `.gitignore`.

## Decisões Técnicas
- **Remoção de `mobile/assets`:** O diretório foi removido da lista de caminhos críticos (`CRITICAL_PATHS`) para evitar falhas falsas, dado que pastas de conteúdo de UI não devem ser travas de infraestrutura no estágio de inicialização.
- **Ajuste de Paths no `.gitignore`:** As strings de busca foram alteradas para incluir o prefixo `mobile/`, garantindo que a validação ocorra sobre os caminhos reais do monorepo.
- **Encoding UTF-8:** Mantida a obrigatoriedade de abertura de arquivos com `encoding="utf-8"` para suportar caracteres Unicode em ambientes Windows.

## Arquivos Afetados
- `scripts/setup/verify_mobile_setup.py`

## Política de Testes
[TEST_EXEMPT: Script de infraestrutura validado por execução direta no terminal. O sucesso é confirmado pela saída: "Environment validation completed successfully."]
