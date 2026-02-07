
# ⚖️ TRUTH HIERARCHY PROTOCOL (THP) v1.0
**Status:** ENFORCED
**Authority:** KERNEL L6
Este protocolo define a precedência de evidências em caso de conflito de diagnóstico.
## 1. Níveis de Autoridade
### 🥇 L0: Realidade Física (Inquestionável)
Fatos binários do sistema operacional e compiladores.
- **Exit Code do `tsc` (TypeScript Compiler).**
- **Exit Code do `pytest`.**
- **Conectividade de Socket (TCP Handshake).**
- **Existência de Arquivo (`os.path.exists`).**
> *Regra:* Se L0 falhar, o sistema está **BROKEN**, não importa o que L1, L2 ou L3 digam.
### 🥈 L1: Auditores de Realidade (Verificadores)
Scripts que executam ferramentas L0 e interpretam a saída bruta.
- `meta_audit_l6.py` (Supremo)
- `verify_frontend_compilation.py`
- `verify_production_ready.py`
> *Regra:* Devem repassar o erro L0 sem "amaciar". Proibido `try/except` silencioso.
### 🥉 L2: Auditores de Consistência (Lógicos)
Scripts que verificam regras de negócio ou integridade relacional.
- `systemic_truth_engine.py`
- `sec_01_rls_integrity.py`
> *Regra:* Só são válidos se L0 e L1 estiverem verdes.
### 🗑️ L3: Auditores Cosméticos (Estruturais)
Scripts que verificam presença de arquivos, nomes ou padrões de texto.
- `audit_systemic_entropy.py`
- `gov_01_xml_presence_audit.py`
> *Regra:* Informativos apenas. Nunca bloqueiam um deploy se L0 passar, e nunca aprovam um deploy se L0 falhar.
## 2. Resolução de Conflitos
**Cenário:** `audit_systemic_entropy.py` diz "SUCCESS" (L3), mas `tsc` diz "ERROR" (L0).
**Veredito:** **FALHA CRÍTICA (L0 prevalece).** O relatório L3 deve ser descartado como "Falso Negativo".
---
*MesaFlow Kernel — Truth Division*

