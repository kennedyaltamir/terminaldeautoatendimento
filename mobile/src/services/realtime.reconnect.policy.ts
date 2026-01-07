/**
 * RealtimeReconnectPolicy: Gerencia a estratégia de reconexão exponencial.
 * Evita retry agressivo e protege a infraestrutura do backend.
 */
const MAX_RETRIES = 10;
const BASE_DELAY_MS = 2000;
const MAX_DELAY_MS = 30000;

export const ReconnectPolicy = {
  retryCount: 0,

  /**
   * Calcula o próximo delay baseado em crescimento exponencial.
   */
  getNextDelay(): number | null {
    if (this.retryCount >= MAX_RETRIES) return null;
    
    const delay = Math.min(
      BASE_DELAY_MS * Math.pow(2, this.retryCount),
      MAX_DELAY_MS
    );
    
    this.retryCount++;
    return delay;
  },

  reset() {
    this.retryCount = 0;
  },

  get canRetry(): boolean {
    return this.retryCount < MAX_RETRIES;
  }
};
