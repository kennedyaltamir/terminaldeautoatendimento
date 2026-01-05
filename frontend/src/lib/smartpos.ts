export type PaymentScheme = 'stone' | 'pagseguro' | 'cielo' | 'generic';

export interface SmartPosOptions {
  scheme: PaymentScheme;
  amount: number; // Valor em Reais (ex: 10.50)
  type: 'credit' | 'debit' | 'voucher';
  orderId: string;
  installments?: number;
}

export function generatePaymentIntent({ scheme, amount, type, orderId, installments = 1 }: SmartPosOptions): string {
  const amountCents = Math.round(amount * 100);
  
  // Stone (Stone Smart SDK)
  if (scheme === 'stone') {
    const transType = type === 'debit' ? 'DEBIT' : type === 'voucher' ? 'VOUCHER' : 'CREDIT';
    // Esquema de URL padrão da Stone para deep linking simples
    return `stone://payment?amount=${amountCents}&transaction_type=${transType}&order_id=${orderId}&editable_amount=0&installments=${installments}`;
  }
  
  // PagSeguro (PlugPag)
  if (scheme === 'pagseguro') {
    // 1=Crédito, 2=Débito, 3=Voucher
    const transType = type === 'credit' ? 1 : type === 'debit' ? 2 : 3;
    return `plugpag://payment?amount=${amountCents}&type=${transType}&installment=${installments}&userReference=${orderId}`;
  }

  // Cielo (Lio) - Exemplo genérico, varia conforme versão da Lio
  if (scheme === 'cielo') {
    return `cielo://payment?amount=${amountCents}&order=${orderId}`;
  }

  return '';
}

export function detectSmartPOS(): PaymentScheme | null {
  if (typeof navigator === 'undefined') return null;
  const ua = navigator.userAgent.toLowerCase();
  
  if (ua.includes('stone') || ua.includes('pos')) return 'stone';
  if (ua.includes('pagseguro') || ua.includes('minizinha')) return 'pagseguro';
  if (ua.includes('cielo') || ua.includes('lio')) return 'cielo';
  
  // Fallback para Android genérico se quiser forçar teste
  if (ua.includes('android')) return 'stone'; // Default para Stone em Android genérico para testes
  
  return null;
}