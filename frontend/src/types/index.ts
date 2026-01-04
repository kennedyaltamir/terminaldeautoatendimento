export interface Company {
  name: string;
  is_active: boolean;
  logo_url?: string;
  primary_color: string;
  banner_url?: string;
  opens_at?: string;
  closes_at?: string;
  owner_email?: string;
  pix_key?: string;
  loyalty_percentage?: number;
  segment?: 'gastro' | 'event' | 'hotel' | 'corp';
  plan_tier: 'free' | 'pro' | 'enterprise';
  stripe_subscription_id?: string;
  subscription_status?: string;
  fixed_delivery_fee?: number; // NOVO
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
    name: string;
    image_url: string | null;
    price: number;
    station: 'kitchen' | 'bar' | 'dessert' | 'other';
  };
  selected_options: OrderItemOptionResponse[];
}

export interface Order {
  id: string;
  table?: {
    table_number: number;
  };
  order_type: 'dine_in' | 'delivery' | 'takeout';
  delivery_address?: string;
  customer_phone?: string;
  
  subtotal?: number;
  discount_amount?: number;
  cashback_earned?: number;
  
  customer_name: string | null;
  total_amount: number;
  status: 'pending' | 'accepted' | 'preparing' | 'ready' | 'delivering' | 'delivered' | 'canceled';
  payment_method: 'pix' | 'card' | 'cash' | 'online';
  payment_status: 'pending' | 'paid';
  created_at: string;
  finished_at?: string;
  items: OrderItemResponse[];
  mp_qr_code?: string;
  mp_qr_code_base64?: string;
  driver_id?: number;
  
  // Novos campos de Logística
  delivery_code?: string;
  delivery_fee?: number;
  service_fee?: number;
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

export interface CheckTableResponse {
  status: 'free' | 'active' | 'blocked';
  customer_name?: string;
  session_token?: string;
  requires_pin?: boolean;
}

export interface Employee {
  id: number;
  name: string;
  email: string;
  role: "kitchen" | "cashier" | "manager" | "driver";
  is_active: boolean;
}