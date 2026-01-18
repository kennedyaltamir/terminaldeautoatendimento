import { Order } from './orders';

/**
 * MesaFlow OS - Domain: Tables & Service Sessions
 */
export interface Table {
  id: number;
  table_number: number;
  qr_token: string;
  is_active: boolean;
  position_x: number;
  position_y: number;
}

export interface TableDashboard extends Table {
  status: 'free' | 'occupied' | 'alert';
  active_session?: {
    id: number;
    customer_name: string;
    total_spent: number;
    start_time: string;
    access_pin: string;
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
}

export interface ServiceRequest {
  id: number;
  table_number: number;
  service_type: string;
  notes?: string;
  status: string;
  created_at: string;
}

