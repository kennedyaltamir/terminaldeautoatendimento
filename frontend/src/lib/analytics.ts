/**
 * Author: MESAFLOW_AI
 * Version: 11.4 (Cleaned)
 * DNA_ID: analytics-sovereign-v11-4
 * Objective: Expanded event contracts for Team Search & Profile Management.
 */
export type EventName = 
  // Core / Menu
  | 'view_menu' 
  | 'add_to_cart' 
  | 'view_cart'
  | 'start_checkout' 
  | 'select_payment_method'
  | 'view_pix'
  | 'finish_order'
  | 'survey_interaction'
  // Kiosk / Auth
  | 'kiosk_reset'
  | 'auth_recovery_telemetry'
  // Dashboard / Governance
  | 'decision_under_low_confidence'
  | 'confidence_recovery_latency'
  | 'simulation_disclaimer_ack'
  | 'sovereign_decision_event'
  // Team Management
  | 'view_team_management'
  | 'limit_reached_trigger'
  | 'employee_role_updated'
  | 'employee_created'
  | 'employee_creation_failed'
  | 'auth_revocation_success'
  | 'auth_revocation_failed'
  | 'employee_search';

interface AnalyticsContext {
  company_id?: string;
  origin?: 'kiosk' | 'mobile' | 'waiter' | 'admin';
  table_id?: number | null;
  session_id?: string | null;
  [key: string]: any;
}

interface AnalyticsEvent {
  name: EventName;
  properties?: Record<string, any>;
  timestamp: string;
}

const MAX_QUEUE_SIZE = 100;

class AnalyticsEngine {
  private queue: AnalyticsEvent[] = [];
  private isProcessing = false;
  private context: AnalyticsContext = {};
  private debug = process.env.NODE_ENV === 'development';

  constructor() {
    if (typeof window !== 'undefined') {
      const savedContext = sessionStorage.getItem('mesaflow_analytics_context');
      if (savedContext) {
        try { this.context = JSON.parse(savedContext); } catch {}
      }
    }
  }

  public setContext(data: AnalyticsContext) {
    this.context = { ...this.context, ...data };
    if (typeof window !== 'undefined') {
      sessionStorage.setItem('mesaflow_analytics_context', JSON.stringify(this.context));
    }
  }

  public track(name: EventName, properties: Record<string, any> = {}) {
    if (this.queue.length >= MAX_QUEUE_SIZE) {
      if (this.debug) console.warn('[Analytics] Queue overflow. Dropping oldest event.');
      this.queue.shift();
    }

    const event: AnalyticsEvent = {
      name,
      properties: {
        ...this.context,
        ...properties,
        url: typeof window !== 'undefined' ? window.location.pathname : '',
      },
      timestamp: new Date().toISOString(),
    };

    this.queue.push(event);
    this.processQueue();

    if (this.debug) {
      // 🛡️ FIX: console.log -> console.debug
      console.debug(`📊 [Analytics] ${name}`, event.properties);
    }
  }

  private async processQueue() {
    if (this.isProcessing || this.queue.length === 0) return;

    this.isProcessing = true;
    const batch = [...this.queue];
    this.queue = [];

    try {
      // Simulação de ingestão (L8: Implementar endpoint real no futuro)
      await new Promise(resolve => setTimeout(resolve, 20)); 
    } catch (error) {
      const spaceLeft = MAX_QUEUE_SIZE - this.queue.length;
      if (spaceLeft > 0) {
        this.queue.unshift(...batch.slice(0, spaceLeft));
      }
    } finally {
      this.isProcessing = false;
      if (this.queue.length > 0) {
        setTimeout(() => this.processQueue(), 1000); // Throttle de retry
      }
    }
  }
}

export const analytics = new AnalyticsEngine();
