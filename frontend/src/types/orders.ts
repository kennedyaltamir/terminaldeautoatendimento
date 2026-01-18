import { Product, Option } from './menu';

/**
 * MesaFlow OS - Domain: Orders, Cart & Feedback
 */
export interface FeedbackResponse {
  score: number;
  comment?: string | null;
  created_at: string;
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

export interface Order {
  id: string;
  table?: { table_number: number };
  order_type: 'dine_in' | 'delivery' | 'takeout';
  origin?: 'mesaflow' | 'ifood' | 'rappi';
  customer_name: string | null;
  customer_phone: string | null;
  delivery_address: string | null;
  delivery_lat: number | null;
  delivery_lng: number | null;
  driver_id: number | null;
  external_order_id: string | null;
  total_amount: number;
  status: string;
  payment_method: string;
  payment_status: string;
  created_at: string;
  items: OrderItemResponse[];
  mp_qr_code?: string;
  mp_qr_code_base64?: string;
  fiscal_status?: string;
  nfe_url_pdf?: string;
  feedback?: FeedbackResponse;
}

