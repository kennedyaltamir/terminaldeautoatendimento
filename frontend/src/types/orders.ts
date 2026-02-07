/**
 * Author: MESAFLOW_AI
 * Version: 13.2.0 (GPS Support)
 * DNA_ID: MF-TYPES-ORDERS-V13-2
 */
import { Product, Option } from './menu';

export type OrderStatus = 'pending' | 'accepted' | 'preparing' | 'ready' | 'delivering' | 'delivered' | 'canceled';

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
  unit_price: number;
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
  origin?: 'mesaflow' | 'ifood' | 'rappi' | 'kiosk' | 'admin' | 'waiter';
  customer_name: string | null;
  customer_phone: string | null;
  delivery_address: string | null;
  
  // 🛰️ SUPORTE A GPS
  delivery_lat: number | null;
  delivery_lng: number | null;
  
  driver_id: number | null;
  total_amount: number;
  status: OrderStatus;
  payment_method: string;
  payment_status: string;
  created_at: string;
  delivery_code: string | null;
 items: OrderItemResponse[];
  mp_qr_code?: string;
  mp_qr_code_base64?: string;
  fiscal_status?: string;
  nfe_url_pdf?: string;
  feedback?: FeedbackResponse;
  pickup_note?: string | null;
  external_order_id?: string | null;
}
