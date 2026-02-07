import { Order } from '../store/orders.store';

/**
 * SLA_LIMITS (em segundos): Tempo máximo permitido em cada status.
 */
const SLA_LIMITS: Record<string, number> = {
  'pending': 300,   // 5 min
  'preparing': 600, // 10 min
  'ready': 180,     // 3 min
  'default': 600
};

export type SLAStatus = 'OK' | 'WARNING' | 'CRITICAL' | 'BREACHED';

export interface SLAMetrics {
  elapsedSeconds: number;
  remainingSeconds: number;
  status: SLAStatus;
  priorityScore: number;
}

export const OrdersSLAService = {
  /**
   * Calcula as métricas de SLA para um pedido baseado no timestamp atual.
   */
  calculateMetrics(order: Order, currentTimestamp: number): SLAMetrics {
    const createdTime = new Date(order.created_at).getTime();
    const elapsedSeconds = Math.floor((currentTimestamp - createdTime) / 1000);
    
    const limitSeconds = SLA_LIMITS[order.status] || SLA_LIMITS.default;
    const remainingSeconds = limitSeconds - elapsedSeconds;
    
    const percentLeft = (remainingSeconds / limitSeconds) * 100;

    let status: SLAStatus = 'OK';
    if (remainingSeconds <= 0) status = 'BREACHED';
    else if (percentLeft <= 20) status = 'CRITICAL';
    else if (percentLeft <= 50) status = 'WARNING';

    /**
     * Priority Score:
     * Quanto menor o tempo restante, maior a pontuação.
     * Pedidos BREACHED ganham bônus de prioridade fixo.
     */
    const priorityScore = (status === 'BREACHED') 
      ? 10000 + Math.abs(remainingSeconds) 
      : (limitSeconds - remainingSeconds);

    return {
      elapsedSeconds,
      remainingSeconds,
      status,
      priorityScore
    };
  }
};
