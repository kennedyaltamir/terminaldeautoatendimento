/**
 * MESAFLOW RECOVERY CONTRACTS (L8.6)
 * -----------------------------------------------------------------------------
 * DOMAIN: SECURITY INFRASTRUCTURE
 * OBJECTIVE: Centralizar ritos de recuperação com entropia criptográfica real.
 */

import { analytics } from "@/lib/analytics";

/** 🧬 Gera um UUID com entropia criptográfica (CSPRNG) */
export const generateSovereignUUID = (): string => {
  if (typeof window !== 'undefined' && window.crypto && window.crypto.randomUUID) {
    return window.crypto.randomUUID();
  }

  const buffer = new Uint8Array(16);
  window.crypto.getRandomValues(buffer);
  
  buffer[6] = (buffer[6] & 0x0f) | 0x40;
  buffer[8] = (buffer[8] & 0x3f) | 0x80;

  const hex = Array.from(buffer).map(b => b.toString(16).padStart(2, '0')).join('');
  return `${hex.slice(0,8)}-${hex.slice(8,12)}-${hex.slice(12,16)}-${hex.slice(16,20)}-${hex.slice(20)}`;
};

/** 🛡️ Garante que a UI nunca revele o estado real da base de dados */
export const enforceSilentHandshake = (setter: (val: boolean) => void) => {
  setter(true);
};

/** 
 * 🔭 Telemetria Sensível (Classificação: Operational/Sensitive)
 * @notes: Em L9, implementar delay artificial e sampling para evitar fingerprinting temporal.
 */
export const trackRecoveryStage = (intentId: string, stage: 'client_initiated' | 'server_acknowledged' | 'network_fail') => {
  // FIX: Agora o tipo 'auth_recovery_telemetry' é aceito pelo motor de analytics
  analytics.track('auth_recovery_telemetry', { 
    intent_id: intentId,
    intent_stage: stage,
    timestamp: new Date().toISOString() 
  });
};

/** 🛑 Garante que builds de produção NUNCA apontem para endpoints locais */
const assertProductionEndpoint = (url?: string): string => {
  if (!url || url.includes("localhost") || url.includes("127.0.0.1")) {
    throw new Error("CRITICAL_SECURITY_VIOLATION: Production endpoint must be a valid remote sovereign URL.");
  }
  return url;
};

/** 🛠️ Resolve endpoint para ambiente de desenvolvimento */
const resolveDevEndpoint = (url?: string): string => {
  return url || "http://localhost:8000/api";
};

export const getSovereignEndpoint = (url?: string): string => {
  return process.env.NODE_ENV === "production" 
    ? assertProductionEndpoint(url) 
    : resolveDevEndpoint(url);
};

/** 🕒 Janela de validade do Intent (Documentação de Risco) */
export const INTENT_REPLAY_WINDOW_MS = 1000 * 60 * 15; // 15 minutos