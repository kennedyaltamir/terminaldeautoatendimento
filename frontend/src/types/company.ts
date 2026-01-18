/**
 * MesaFlow OS - Domain: Company & System Audit
 */
export interface Company {
  name: string;
  slug: string;
  is_active: boolean;
  logo_url?: string | null;
  primary_color: string;
  banner_url?: string | null;
  background_color?: string | null;
  text_color?: string | null;
  accent_color?: string | null;
  opens_at?: string | null;
  closes_at?: string | null;
  owner_email?: string;
  pix_key?: string | null;
  loyalty_percentage?: number;
  segment?: 'gastro' | 'event' | 'hotel' | 'corp';
  plan_tier: 'free' | 'pro' | 'enterprise';
  stripe_subscription_id?: string | null;
  subscription_status?: string | null;
  fixed_delivery_fee?: number;
  cnpj?: string | null;
  inscricao_estadual?: string | null;
  fiscal_token?: string | null;
  csc_token?: string | null;
  csc_id?: string | null;
  whatsapp_number?: string | null;
  whatsapp_api_url?: string | null;
  whatsapp_instance?: string | null;
  whatsapp_token?: string | null;
  ifood_merchant_id?: string | null;
  payment_provider?: 'mercadopago' | 'efi' | 'stripe' | 'pagarme' | 'none';
  payment_credentials?: any;
  kiosk_password_set?: boolean;
  kiosk_password?: string;
}

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

