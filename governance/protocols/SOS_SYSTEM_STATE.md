# 🆘 SOS System State Protocol
**Status:** ACTIVE
**Version:** 1.0

Este protocolo define o comportamento do sistema em caso de falha catastrófica ou corrupção de integridade.

## 1. Gatilhos de Estado SOS
O sistema entra em modo SOS se:
1.  O `Stability Score` do Optimizer cair abaixo de 50/100.
2.  Ocorrerem 3 falhas consecutivas de `KIE-02` (Hash Mismatch).
3.  Arquivos críticos do Kernel (`atualizar.py`, `gerartxt.py`) forem deletados ou corrompidos.

## 2. Procedimentos de Recuperação
### Nível 1: Auto-Cura (Self-Healing)
- O Kernel tenta restaurar o último Snapshot válido (`backups/snapshot_latest.zip`).
- O Optimizer gera uma Task de Emergência (`[AUTO-OPT | CRITICAL] Restore System Integrity`).

### Nível 2: Intervenção Humana
- O sistema bloqueia novas escritas automáticas.
- Exibe mensagem de alerta no terminal: `⚠️ SYSTEM IN SOS MODE. MANUAL INTERVENTION REQUIRED.`
- Solicita execução do script de diagnóstico: `python scripts/maintenance/system_integrity_check.py`.

## 3. Saída do Modo SOS
O sistema retorna ao modo normal apenas quando:
1.  O script de integridade retornar `SUCCESS`.
2.  O `Stability Score` retornar para > 70.
