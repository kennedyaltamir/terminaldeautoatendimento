/**
 * @file realtime.reconnect.policy.ts
 * @description Gerencia a estratégia de reconexão exponencial para WebSockets.
 * Evita retry storm e protege a infraestrutura do backend.
 */

const MAX_RETRIES = 10;
const BASE_DELAY_MS = 2000;
const MAX_DELAY_MS = 30000;

export const ReconnectPolicy = {
  retryCount: 0,

  /**
   * Calcula o próximo delay baseado em crescimento exponencial.
   * Fórmula: min(BASE * 2^retry, MAX)
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

  /**
   * Reseta o contador de tentativas.
   * Deve ser chamado quando uma conexão é estabelecida com sucesso.
   */
  reset() {
    this.retryCount = 0;
  },

  get canRetry(): boolean {
    return this.retryCount < MAX_RETRIES;
  }
};
