/**
 * DOMAIN: OBSERVABILITY
 * OBJECTIVE: Structured JSON Logging for KDS Operations.
 */
export type KdsEventDomain = 'FSM' | 'NETWORK' | 'AUDIO' | 'USER_ACTION' | 'SYSTEM';

export interface KdsLogPayload {
  domain: KdsEventDomain;
  action: string;
  orderId?: string;
  meta?: Record<string, any>;
  severity?: 'INFO' | 'WARN' | 'ERROR' | 'CRITICAL';
}

export const kdsLogger = {
  log: (payload: KdsLogPayload) => {
    const entry = {
      timestamp: new Date().toISOString(),
      environment: process.env.NODE_ENV,
      ...payload
    };
    
    // Em produção, isso iria para um ingestor (Datadog/Sentry)
    // Em dev, mantemos legível mas estruturado
    if (payload.severity === 'ERROR' || payload.severity === 'CRITICAL') {
      console.error('🚨 [KDS_AUDIT]', JSON.stringify(entry));
    } else {
      console.info('📝 [KDS_AUDIT]', JSON.stringify(entry));
    }
  }
};

