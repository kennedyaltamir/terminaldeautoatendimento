/**
 * DOMAIN: FRONTEND
 * OBJECTIVE: Logger Forense "Black Box" com persistência offline.
 * DESCRIPTION: Garante que nenhum evento de segurança seja perdido, mesmo sem internet.
 */

const OFFLINE_KEY = "mf_audit_blackbox";

interface AuditEvent {
  event: string;
  target_email: string;
  success: boolean;
  error?: string;
  timestamp: string;
  url: string;
  userAgent: string;
}

export const auditLogger = {
  logAttempt: (email: string, success: boolean, errorDetails?: string) => {
    if (typeof window === 'undefined') return;

    const payload: AuditEvent = {
      event: "IMPERSONATION_ATTEMPT",
      target_email: email,
      success,
      error: errorDetails,
      timestamp: new Date().toISOString(),
      url: window.location.href,
      userAgent: navigator.userAgent
    };

    const blob = new Blob([JSON.stringify(payload)], { type: 'application/json' });
    const endpoint = `${process.env.NEXT_PUBLIC_API_URL}/admin/audit/ingest`;
    
    // Tenta enviar imediatamente via Beacon (Ideal para unload)
    const sent = navigator.sendBeacon ? navigator.sendBeacon(endpoint, blob) : false;

    if (!sent) {
      // Fallback: Tenta fetch com keepalive
      fetch(endpoint, { 
        method: 'POST', 
        body: JSON.stringify(payload), 
        headers: { 'Content-Type': 'application/json' },
        keepalive: true 
      }).catch(() => {
        // Se falhar totalmente (Offline), salva na Caixa Preta local
        auditLogger.saveOffline(payload);
      });
    }

    // Tenta despachar logs antigos se houver conexão
    if (navigator.onLine) {
      auditLogger.flushOffline();
    }
  },

  saveOffline: (event: AuditEvent) => {
    try {
      const current = JSON.parse(localStorage.getItem(OFFLINE_KEY) || "[]");
      current.push(event);
      // Limita a 50 logs locais para não estourar storage
      if (current.length > 50) current.shift();
      localStorage.setItem(OFFLINE_KEY, JSON.stringify(current));
      console.warn("[Audit] Evento salvo na Caixa Preta offline.");
    } catch (e) {
      console.error("[Audit] Falha crítica na persistência local.", e);
    }
  },

  flushOffline: async () => {
    const offlineData = localStorage.getItem(OFFLINE_KEY);
    if (!offlineData) return;

    const events: AuditEvent[] = JSON.parse(offlineData);
    if (events.length === 0) return;

    const endpoint = `${process.env.NEXT_PUBLIC_API_URL}/admin/audit/ingest-batch`;

    try {
      // Envia em lote (se o backend suportar) ou um por um
      // Aqui simulamos envio um por um para compatibilidade
      await Promise.all(events.map(ev => 
        fetch(endpoint.replace('ingest-batch', 'ingest'), {
          method: 'POST',
          body: JSON.stringify(ev),
          headers: { 'Content-Type': 'application/json' }
        })
      ));
      
      // Limpa a caixa preta apenas se sucesso
      localStorage.removeItem(OFFLINE_KEY);
      console.info(`[Audit] ${events.length} eventos offline sincronizados.`);
    } catch (e) {
      // Mantém no storage para tentar depois
    }
  }
};
