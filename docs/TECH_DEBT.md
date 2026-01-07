# 📋 Dívida Técnica Global: MesaFlow (Atualizada)

## 📱 Domínio Mobile

### Operação e Alertas
- **Silent Mode:** Atualmente, os alertas operacionais (vibração) são obrigatórios e não podem ser desativados ou silenciados por períodos determinados.
- **Alert Customization:** Os limites de cooldown e padrões de vibração estão fixos nos serviços, impossibilitando ajustes por perfil de estabelecimento (ex: ambientes barulhentos vs silenciosos).

### Lógica de Negócio e Domínio
- **SLA de Transição:** O cálculo ainda depende apenas de `created_at`.
- **Sorting Jitter:** Reordenação por score a cada tick (5s) pode causar desconforto visual se o operador estiver prestes a interagir com um card.

---
*Última atualização: 07 de Janeiro de 2026*
