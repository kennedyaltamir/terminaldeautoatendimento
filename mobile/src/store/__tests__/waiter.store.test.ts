import { useWaiterStore } from '../waiter.store';

describe('WaiterStore Realtime Logic', () => {
  beforeEach(() => {
    useWaiterStore.setState({ 
      lastTableUpdate: 0,
      serviceRequests: []
    });
  });

  it('deve atualizar o timestamp de lastTableUpdate ao disparar triggerRefresh', () => {
    const initialTime = useWaiterStore.getState().lastTableUpdate;
    
    // Simula a chegada de um evento WebSocket
    useWaiterStore.getState().triggerRefresh();
    
    const finalTime = useWaiterStore.getState().lastTableUpdate;
    expect(finalTime).toBeGreaterThan(initialTime);
  });

  it('deve adicionar chamados de mesa sem duplicidade', () => {
    const event = { id: 1, table: 5, service_type: 'bill', notes: 'PIX' };
    
    useWaiterStore.getState().addServiceRequest(event);
    useWaiterStore.getState().addServiceRequest(event); // Duplicado

    expect(useWaiterStore.getState().serviceRequests.length).toBe(1);
  });
});
