// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 03:50:00
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Utilitário para combinar classes Tailwind de forma inteligente.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Formata um valor em centavos (Inteiro) para moeda BRL (String).
 * Ex: 1050 -> "R$ 10,50"
 */
export function formatCurrency(valueInCents: number | undefined | null): string {
  if (valueInCents === undefined || valueInCents === null) return "R$ 0,00";
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(valueInCents / 100);
}

/**
 * Converte uma string de input monetário (ex: "10,50" ou "10.50") para centavos (1050).
 * Usado antes de enviar para a API.
 */
export function parseCurrencyInput(value: string | number): number {
  if (!value) return 0;
  
  const stringValue = String(value);
  
  // Remove tudo que não é dígito, ponto ou vírgula
  // Substitui vírgula por ponto para padronizar
  const cleanValue = stringValue.replace(/[^0-9.,]/g, '').replace(',', '.');
  
  const floatVal = parseFloat(cleanValue);
  if (isNaN(floatVal)) return 0;
  
  // Multiplica por 100 e arredonda para evitar erros de float (ex: 10.50 * 100 = 1050.0000001)
  return Math.round(floatVal * 100);
}

/**
 * Converte centavos (1050) para string de input (ex: "10.50").
 * Usado para preencher formulários de edição.
 */
export function centsToInput(valueInCents: number | undefined | null): string {
  if (valueInCents === undefined || valueInCents === null) return "";
  return (valueInCents / 100).toFixed(2);
}
