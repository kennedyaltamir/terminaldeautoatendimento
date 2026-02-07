
import { Order } from './orders';

/**
 * MesaFlow OS - Domain: Tables & Service Sessions
 * Updated: v12.0 (Crisis Ready)
 */
export interface Table {
  id: number;
  table_number: number;
  qr_token: string;
  is_active: boolean;
  position_x: number;
  position_y: number;
  capacity: number; // Novo campo: Capacidade física
}

export interface TableDashboard extends Table {
  // Novos status: 'preparing' (cliente sentou)
  status: 'free' | 'preparing' | 'occupied' | 'alert' | 'payment';
  active_session?: {
    id: number;
    customer_name: string;
    total_spent: number;
    start_time: string;
    access_pin: string;
    people_count?: number; // Estimativa de ocupação atual
  } | null;
  service_request?: string | null;
}

export interface TableSession {
  id: number;
  customer_name: string;
  is_active: boolean;
  created_at: string;
  orders: Order[];
  total_spent: number;
  access_pin: string;
  session_token: string;
}

export interface ServiceRequest {
  id: number;
  table_number: number;
  service_type: string;
  notes?: string;
  status: string;
  created_at: string;
}
