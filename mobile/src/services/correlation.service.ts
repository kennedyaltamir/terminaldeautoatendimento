
/**
 * CorrelationService: Gera e mantém o ID único da sessão.
 * Essencial para rastreabilidade SRE L4.
 */
class CorrelationService {
  private static instance: CorrelationService;
  private readonly sessionId: string;

  private constructor() {
    this.sessionId = Math.random().toString(36).substring(2, 15) + 
                     Math.random().toString(36).substring(2, 15);
  }

  public static getInstance(): CorrelationService {
    if (!CorrelationService.instance) {
      CorrelationService.instance = new CorrelationService();
    }
    return CorrelationService.instance;
  }

  public getCorrelationId(): string {
    return this.sessionId;
  }
}

export const correlationService = CorrelationService.getInstance();

