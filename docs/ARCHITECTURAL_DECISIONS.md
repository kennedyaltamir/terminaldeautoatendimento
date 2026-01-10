## ADR-004 — Manter Governança Atual Temporariamente

**Decisão:**  
Não simplificar o Kernel, protocolos XML ou camadas de governança neste momento.

**Motivo:**  
- Sistema ainda não hardened em RLS
- Integrações externas não escaláveis
- Segurança e isolamento são prioridade absoluta

**Riscos Aceitos:**  
- Overhead cognitivo
- Consumo maior de tokens

**Revisão prevista:**  
Após conclusão de TD-002 e TD-003
