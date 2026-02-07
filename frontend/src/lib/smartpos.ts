export type PaymentScheme = 'stone' | 'pagseguro' | 'cielo' | 'generic';

export interface SmartPosOptions {
  scheme: PaymentScheme;
  amount: number; // Valor em Reais (ex: 10.50)
  type: 'credit' | 'debit' | 'voucher';
  orderId: string;
  installments?: number;
}

/**
 * Gera a URI (Deep Link) para invocar o app de pagamento nativo do Android.
 */
export function generatePaymentIntent({ scheme, amount, type, orderId, installments = 1 }: SmartPosOptions): string {
  const amountCents = Math.round(amount * 100);
  const returnScheme = "mesaflow"; // Scheme configurado no AndroidManifest (se fosse app nativo) ou URL de callback

  // Stone (Stone Smart SDK)
  if (scheme === 'stone') {
    const transType = type === 'debit' ? 'DEBIT' : type === 'voucher' ? 'VOUCHER' : 'CREDIT';
    return `stone://payment?amount=${amountCents}&transaction_type=${transType}&order_id=${orderId}&editable_amount=0&installments=${installments}&return_scheme=${returnScheme}`;
  }

  // PagSeguro (PlugPag)
  if (scheme === 'pagseguro') {
    const transType = type === 'credit' ? 1 : type === 'debit' ? 2 : 3;
    return `plugpag://payment?amount=${amountCents}&type=${transType}&installment=${installments}&userReference=${orderId}&returnScheme=${returnScheme}`;
  }

  return '';
}

/**
 * Detecta se o sistema está rodando dentro de um Smart POS via User Agent.
 */
export function detectSmartPOS(): PaymentScheme | null {
  if (typeof navigator === 'undefined') return null;
  const ua = navigator.userAgent.toLowerCase();
  
  if (ua.includes('stone') || ua.includes('pos')) return 'stone';
  if (ua.includes('pagseguro') || ua.includes('minizinha')) return 'pagseguro';
  
  // Fallback para testes manuais no Chrome (Simulação)
  if ((window as any).__MOCK_SMART_POS__) return 'stone';

  return null;
}

