import { Order } from '../../store/orders.store';
import { AlertsPolicy } from './alerts.policy';
import { SLAStatus } from '../orders.sla.service';

export interface AlertDecision {
  orderId: string;
  status: SLAStatus;
}

/**
 * AlertsEngineService: Motor de decisão de alertas (Puro).
 * Decide QUEM alertar, mas nunca executa o efeito físico.
 */
export const AlertsEngineService = {
  /**
   * Analisa a lista de pedidos e retorna uma lista de decisões de alerta.
   */
  decide(orders: Order[], currentTime: number): AlertDecision[] {
    const decisions: AlertDecision[] = [];

    orders.forEach(order => {
      if (!order.slaStatus) return;

      const needsAlert = AlertsPolicy.shouldAlert(
        order.slaStatus,
        currentTime,
        order.lastAlertedStatus,
        order.lastAlertedAt
      );

      if (needsAlert) {
        decisions.push({ orderId: order.id, status: order.slaStatus });
      }
    });

    return decisions;
  }
};
