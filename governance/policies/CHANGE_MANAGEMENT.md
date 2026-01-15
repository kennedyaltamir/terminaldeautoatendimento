
# 🔄 Política de Gerenciamento de Mudanças

## 1. Fluxo INDA
Todas as alterações de código aplicadas por IA ou humanos devem seguir:
- **Inspection:** Auditoria do estado atual.
- **Normalization:** Alinhamento com padrões de diretório.
- **Decision:** Aprovação técnica baseada em risco.
- **Action:** Aplicação via `atualizar.py` com backup automático.

## 2. Versionamento
- O sistema segue Semantic Versioning (SemVer).
- Alterações de banco exigem migrações via Alembic.

