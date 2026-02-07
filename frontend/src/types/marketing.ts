/**
 * MesaFlow OS - Domain: Marketing & Promotions
 */
export interface Promotion {
  id: string;
  name: string;
  code: string | null;
  discount_type: 'percentage' | 'fixed' | 'shipping';
  discount_value: number;
  min_order_value: number;
  usage_limit: number | null;
  current_usage: number;
  is_active: boolean;
}

export interface CouponValidationResponse {
  valid: boolean;
  discount_amount: number;
  final_total: number;
  message: string;
  promotion_id?: string;
}

