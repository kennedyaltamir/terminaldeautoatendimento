import { SLAStatus } from '../orders.sla.service';

/**
 * AlertsPolicy: Define as regras de negócio para interrupção do operador.
 * O tempo (now) é injetado para garantir determinismo e testabilidade.
 */
export const AlertsPolicy = {
  BREACHED_COOLDOWN_MS: 60000, 

  shouldAlert(
    status: SLAStatus, 
    now: number,
    lastAlertedStatus?: SLAStatus, 
    lastAlertedAt?: number
  ): boolean {
    // Regra 1: Transição para CRITICAL (Alerta Único)
    if (status === 'CRITICAL' && lastAlertedStatus !== 'CRITICAL') {
      return true;
    }

    // Regra 2: Estado BREACHED (Alerta Recorrente)
    if (status === 'BREACHED') {
      // Se nunca alertou BREACHED antes, dispara
      if (lastAlertedStatus !== 'BREACHED') return true;
      
      // Se já alertou, respeita o cooldown
      if (lastAlertedAt && (now - lastAlertedAt) >= this.BREACHED_COOLDOWN_MS) {
        return true;
      }
    }

    return false;
  }
};
