# 🛡️ Tela: Trust Center (Segurança & Status)
**Rota:** `/trust` | `/trust/status` | `/trust/security`
**Domínio:** PUBLIC / TRANSPARENCY

## 1. Especificação Visual
- **Status Cards:** Indicadores em tempo real (Verde/Vermelho) para API, Banco e Real-time.
- **Uptime Graph:** Histórico de disponibilidade dos últimos 90 dias.
- **Security Badges:** LGPD, PCI-DSS, Encryption 256-bit.

## 2. Elementos Interagíveis
- **Botão "Reportar Incidente":** Link para suporte de segurança.
- **Links de Política:** Acesso aos termos de uso e privacidade.

## 3. Comportamento Esperado
- **Live Data:** O status deve ser consumido do endpoint `/api/health` sem cache agressivo.
- **Transparência:** Exibir a data e hora da última verificação de integridade sistêmica.

## 4. APIs Consumidas
- `GET /api/health`: Status real dos serviços de infraestrutura.
