import { OrdersSLAService } from '../orders.sla.service';

/**
 * Teste Unitário: Validação da lógica de SLA e Prioridade.
 * Garante que o "cérebro" do KDS não falhe em cálculos matemáticos.
 */
describe('OrdersSLAService', () => {
  const mockOrder: any = {
    id: '1',
    status: 'pending',
    created_at: new Date(Date.now() - 10 * 60 * 1000).toISOString(), // Criado há 10 min
  };

  it('deve classificar como BREACHED se o tempo exceder o limite', () => {
    const now = Date.now();
    const metrics = OrdersSLAService.calculateMetrics(mockOrder, now);
    
    // Para 'pending', o limite é 5 min. 10 min decorridos = BREACHED.
    expect(metrics.status).toBe('BREACHED');
    expect(metrics.priorityScore).toBeGreaterThan(10000);
  });

  it('deve calcular corretamente o tempo restante em segundos', () => {
    const createdNow = new Date().toISOString();
    const orderNow = { ...mockOrder, created_at: createdNow, status: 'pending' };
    
    const metrics = OrdersSLAService.calculateMetrics(orderNow, Date.now());
    expect(metrics.remainingSeconds).toBeCloseTo(300, 0); // 5 min = 300s
    expect(metrics.status).toBe('OK');
  });
});
