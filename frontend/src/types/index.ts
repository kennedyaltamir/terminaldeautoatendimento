// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 16:15:00
export interface Company {
  name: string;
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
}

export interface Option {
  id: number;
  name: string;
  price: number;
  is_available: boolean;
}

export interface OptionGroup {
  id: number;
  name: string;
  min_selection: number;
  max_selection: number;
  options: Option[];
}

export interface Ingredient {
  id: number;
  name: string;
  unit: 'kg' | 'g' | 'l' | 'ml' | 'un';
  current_stock: number;
  min_stock_alert: number;
  cost_per_unit: number;
}

export interface RecipeItem {
  id?: number;
  ingredient_id: number;
  quantity_required: number;
  ingredient?: Ingredient;
}

export interface Product {
  id: number;
  name: string;
  description: string | null;
  price: number;
  image_url: string | null;
  is_available: boolean;
  track_stock: boolean;
  stock_quantity: number;
  station: 'kitchen' | 'bar' | 'dessert' | 'other';
  tags: string[];
  short_code?: string;
  external_id?: string;
  option_groups: OptionGroup[];
  recommendations?: Product[];
  recipe_items?: RecipeItem[];
}

export interface Category {
  id: number;
  name: string;
  products: Product[];
}

export interface MenuResponse {
  company: Company;
  categories: Category[];
}

export interface CartItem {
  product: Product;
  quantity: number;
  notes?: string;
  selectedOptions: Option[];
}

export interface OrderItemOptionResponse {
  name: string;
  price: number;
}

export interface OrderItemResponse {
  id: number;
  quantity: number;
  notes: string | null;
  product: {
    id: number;
    name: string;
    image_url: string | null;
    price: number;
    station: 'kitchen' | 'bar' | 'dessert' | 'other';
  };
  selected_options: OrderItemOptionResponse[];
}

export interface OrderFeedback {
  score: number;
  comment: string | null;
  created_at: string;
}

export interface Order {
  id: string;
  table?: {
    table_number: number;
  };
  order_type: 'dine_in' | 'delivery' | 'takeout';
  origin?: 'mesaflow' | 'ifood' | 'rappi';
  external_order_id?: string;
  delivery_address?: string;
  delivery_lat?: number;
  delivery_lng?: number;
  customer_phone?: string;
  subtotal?: number;
  discount_amount?: number;
  cashback_earned?: number;
  customer_name: string | null;
  total_amount: number;
  status: 'pending' | 'accepted' | 'preparing' | 'ready' | 'delivering' | 'delivered' | 'canceled';
  payment_method: 'pix' | 'card' | 'cash' | 'online';
  payment_status: 'pending' | 'paid' | 'failed';
  created_at: string;
  finished_at?: string;
  items: OrderItemResponse[];
  mp_qr_code?: string;
  mp_qr_code_base64?: string;
  driver_id?: number;
  delivery_code?: string;
  delivery_fee?: number;
  service_fee?: number;
  fiscal_status?: 'pending' | 'processing' | 'emitted' | 'error' | 'canceled';
  nfe_url_pdf?: string;
  nfe_url_xml?: string;
  feedback?: OrderFeedback | null; 
}

export interface Table {
  id: number;
  table_number: number;
  qr_token: string;
  is_active: boolean;
}

export interface ServiceRequest {
  id: number;
  table_number: number;
  service_type: 'help' | 'cleaning' | 'bill' | 'other';
  notes?: string;
  status: string;
  created_at: string;
}

export interface TableSession {
  id: number;
  customer_name: string;
  is_active: boolean;
  created_at: string;
  orders: Order[];
  total_spent: number;
  access_pin: string;
}

