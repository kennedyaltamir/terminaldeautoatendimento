/**
 * GlobalClockService: O "Metrônomo" do sistema MesaFlow.
 * Garante que todo o aplicativo opere sob o mesmo carimbo de tempo,
 * evitando discrepâncias entre componentes e economizando recursos de CPU.
 */
type ClockSubscriber = (timestamp: number) => void;

class GlobalClockService {
  private static instance: GlobalClockService;
  private intervalId: NodeJS.Timeout | null = null;
  private subscribers: Set<ClockSubscriber> = new Set();
  private TICK_RATE = 5000; // 5 segundos para equilíbrio entre precisão e bateria

  private constructor() {}

  public static getInstance(): GlobalClockService {
    if (!GlobalClockService.instance) {
      GlobalClockService.instance = new GlobalClockService();
    }
    return GlobalClockService.instance;
  }

  /**
   * Inicia o pulso global.
   */
  public start() {
    if (this.intervalId) return;
    console.log('[Clock] Iniciando pulso global...');
    this.intervalId = setInterval(() => {
      const now = Date.now();
      this.subscribers.forEach(sub => sub(now));
    }, this.TICK_RATE);
  }

  /**
   * Encerra o pulso (ex: em logout).
   */
  public stop() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
      console.log('[Clock] Pulso global encerrado.');
    }
  }

  /**
   * Assina o evento de tempo.
   */
  public subscribe(callback: ClockSubscriber) {
    this.subscribers.add(callback);
    // Emite o valor atual imediatamente para o novo assinante
    callback(Date.now());
    return () => this.subscribers.delete(callback);
  }
}

export const clockService = GlobalClockService.getInstance();
