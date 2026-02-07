import { useOrdersStore } from '../orders.store';
import { OrdersService } from '../../services/orders.service';

// Mock do Service para evitar chamadas de rede reais
jest.mock('../../services/orders.service');

describe('OrdersStore Logic', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    useOrdersStore.setState({ 
      orders: [], 
      isSocketConnected: true,
      isHydrated: true 
    });
  });

  it('deve adicionar um novo pedido e manter a ordem de prioridade', () => {
    const oldOrder: any = { id: '1', status: 'pending', created_at: new Date(Date.now() - 10000).toISOString(), items: [] };
    const newOrder: any = { id: '2', status: 'pending', created_at: new Date().toISOString(), items: [] };

    useOrdersStore.getState().addOrUpdateOrder(oldOrder);
    useOrdersStore.getState().addOrUpdateOrder(newOrder);

    const state = useOrdersStore.getState();
    expect(state.orders.length).toBe(2);
    // O pedido mais antigo (id: 1) deve ter prioridade maior (aparecer primeiro)
    expect(state.orders[0].id).toBe('1');
  });

  it('deve realizar o avanço de status otimista e chamar o service', async () => {
    const order: any = { id: '123', status: 'pending', items: [] };
    useOrdersStore.setState({ orders: [order] });
    
    (OrdersService.updateStatus as jest.Mock).mockResolvedValue({ success: true });

    await useOrdersStore.getState().advanceStatus('123', 'pending', 'slug-teste');

    const updatedOrder = useOrdersStore.getState().orders.find(o => o.id === '123');
    expect(updatedOrder?.status).toBe('preparing');
    expect(OrdersService.updateStatus).toHaveBeenCalledWith('123', 'preparing');
  });
});
