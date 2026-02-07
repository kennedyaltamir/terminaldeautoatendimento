/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 13.3.0 (Evolution API Integration)
 * DNA_ID: MF-TYPES-COMPANY-V13-3
 */
export type PlanTier = 'free' | 'pro' | 'enterprise';
export type CompanySegment = 'gastro' | 'event' | 'hotel' | 'corp';
export type PaymentProvider = 'mercadopago' | 'efi' | 'stripe' | 'pagarme' | 'none';

export interface Company {
  id: string;
  name: string;
  slug: string;
  custom_domain?: string | null;
  is_active: boolean;
  segment: CompanySegment;
  created_at: string;
  owner_email: string;
  owner_phone?: string | null;
  owner_role?: string | null;
  logo_url?: string | null;
  banner_url?: string | null;
  primary_color: string;
  background_color?: string | null;
  text_color?: string | null;
  accent_color?: string | null;
  stone_merchant_id?: string | null;
  stone_terminal_id?: string | null;
  opens_at?: string | null;
  closes_at?: string | null;
  qr_config?: {
    show_wifi: boolean;
    show_instagram: boolean;
    show_steps: boolean;
    show_logo: boolean;
    dark_mode: boolean;
    custom_color: string | null;
  };
  wifi_ssid?: string | null;
  wifi_password?: string | null;
  instagram_url?: string | null;
  whatsapp_number?: string | null;
  whatsapp_api_url?: string | null;
  whatsapp_instance?: string | null;
  whatsapp_token?: string | null;
  payment_provider: PaymentProvider;
  payment_credentials?: any;
  pix_key?: string | null;
  mp_access_token?: string | null;
  mp_user_id?: string | null;
  marketplace_fee_percentage?: number;
  service_fee_percentage?: number;
  fixed_delivery_fee?: number;
  loyalty_percentage?: number;
  stripe_customer_id?: string | null;
  stripe_subscription_id?: string | null;
  subscription_status?: string | null;
  plan_tier: PlanTier;
  cnpj?: string | null;
  inscricao_estadual?: string | null;
  fiscal_token?: string | null;
  csc_token?: string | null;
  csc_id?: string | null;
  kiosk_password_set?: boolean;
  kiosk_password?: string;
}

/**
 * Representa um registro imutável de ação no sistema.
 */
export interface AuditLog {
  id: number;
  user_name: string;
  user_role: string;
  action: string;
  resource: string;
  resource_id: string;
  details: any;
  ip_address: string;
  created_at: string;
}

/**
 * Representa uma assinatura de evento externo.
 */
export interface WebhookResponse {
  id: number;
  target_url: string;
  events: string[];
  secret: string;
  is_active: boolean;
  created_at: string;
}