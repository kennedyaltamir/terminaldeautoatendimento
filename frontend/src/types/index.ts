/**
 * Author: MESAFLOW_AI
 * Version: 11.7
 * DNA_ID: MF-TYPES-V11.7-TEAM
 * Objective: Standardize Role Configuration with High-Contrast metadata.
 */
import { LucideIcon } from "lucide-react";

export * from './auth';
export * from './company';
export * from './marketing';
export * from './menu';
export * from './orders';
export * from './tables';

export type DashboardMode = 'BUSINESS' | 'GOVERNANCE';

export interface RoleConfig {
  label: string;
  icon: LucideIcon;
  color: string; // Tailwind class para texto
  bg: string;    // Tailwind class para fundo
  contrastColor: string; // HEX para marcadores de alto contraste (Audit)
}

export interface AuditEvent {
  id: number;
  action: "create" | "update" | "delete";
  field: string;
  old: string | null;
  new: string;
  user: string;
  date: string;
}

export interface Metrics {
  business_kpis: {
    revenue_today: number;
    revenue_change_pct: number;
    orders_today: number;
    avg_ticket: number;
    prep_time_avg: number;
    best_seller: { name: string; quantity: number };
  };
  insights: { type: 'INFO' | 'WARNING' | 'OPPORTUNITY'; message: string }[];
  margin_confidence_index?: number;
  net_margin_value: number; 
  accumulated_sla_debt: number; 
  snapshot_id: string;
  kernel_time: string;
}
