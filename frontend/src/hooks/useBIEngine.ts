/**
 * DOMAIN: FRONTEND
 * OBJECTIVE: Motor de BI Prescritivo e Simulador de Cenários.
 */
import { useMemo } from 'react';

export interface SimulationState {
  ticketMultiplier: number;
  volumeMultiplier: number;
  deliveryShare: number;
}

export function useBIEngine(metrics: any, simulation: SimulationState) {
  return useMemo(() => {
    if (!metrics) return null;

    const baseRevenue = metrics.total_revenue;
    const baseOrders = metrics.total_orders;

    // Simulação Dinâmica
    const simulatedRevenue = baseRevenue * simulation.ticketMultiplier * simulation.volumeMultiplier;
    const simulatedOrders = baseOrders * simulation.volumeMultiplier;
    
    const monthlyGoal = 500000; // R$ 5.000,00
    const currentProgress = (simulatedRevenue / monthlyGoal) * 100;

    const channelData = metrics.sales_chart.map((d: any) => {
      const val = d.value * simulation.ticketMultiplier * simulation.volumeMultiplier;
      return {
        ...d,
        simulatedValue: val,
        Delivery: val * simulation.deliveryShare,
        Balcao: val * (1 - simulation.deliveryShare) * 0.7,
        App: val * (1 - simulation.deliveryShare) * 0.3,
      };
    });

    const alerts = [];
    if (metrics.average_ticket < 2500) {
      alerts.push({ id: 1, cat: 'Receita', type: 'critical', msg: 'Ticket médio abaixo da meta.' });
    }
    if (simulation.deliveryShare > 0.8) {
      alerts.push({ id: 2, cat: 'Operação', type: 'attention', msg: 'Dependência alta de delivery.' });
    }

    return {
      simulatedRevenue,
      simulatedOrders,
      progress: currentProgress,
      channelData,
      alerts,
      peakHour: metrics.sales_by_hour[0]
    };
  }, [metrics, simulation]);
}
