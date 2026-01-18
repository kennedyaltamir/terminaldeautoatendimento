/**
 * MesaFlow OS - Global Type Registry (Barrel File)
 * Fragmentado para reduzir o Blast Radius (v6.0.0)
 * 
 * Este arquivo centraliza as exportações para manter compatibilidade 
 * com imports do tipo: import { Order } from '@/types'
 */

export * from './auth';
export * from './company';
export * from './menu';
export * from './orders';
export * from './tables';
export * from './marketing';

/**
 * Tipos Utilitários Globais
 * Padronizados para o Protocolo SGCS/1.4
 */
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface PaginationParams {
  page: number;
  limit: number;
  total: number;
}