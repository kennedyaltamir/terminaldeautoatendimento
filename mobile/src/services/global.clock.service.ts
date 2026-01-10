import { AppState, AppStateStatus } from 'react-native';
import { useOrdersStore } from '../store/orders.store';

class GlobalClockService {
  private intervalId: NodeJS.Timeout | null = null;
  private readonly TICK_RATE = 5000; // 5 segundos
  private appStateSubscription: any = null;

  init() {
    if (this.intervalId) return;

    console.log('[GlobalClock] Inicializando serviço de tempo...');
    this.startTimer();

    // Monitora o estado do App (Foreground/Background)
    this.appStateSubscription = AppState.addEventListener('change', this.handleAppStateChange);
  }

  private startTimer() {
    if (this.intervalId) return;
    
    console.log('[GlobalClock] Timer iniciado.');
    // Executa imediatamente
    this.tick();
    // Agenda o intervalo
    this.intervalId = setInterval(() => this.tick(), this.TICK_RATE);
  }

  private stopTimer() {
    if (this.intervalId) {
      console.log('[GlobalClock] Timer pausado (Economia de Energia).');
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }

  private handleAppStateChange = (nextAppState: AppStateStatus) => {
    if (nextAppState === 'active') {
      console.log('[GlobalClock] App voltou para o primeiro plano. Sincronizando...');
      this.startTimer();
    } else if (nextAppState === 'background' || nextAppState === 'inactive') {
      this.stopTimer();
    }
  };

  private tick() {
    // Dispara a atualização de SLAs na Store
    useOrdersStore.getState().updateSLAs();
  }

  dispose() {
    this.stopTimer();
    if (this.appStateSubscription) {
      this.appStateSubscription.remove();
    }
  }
}

export default new GlobalClockService();
