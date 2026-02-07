/**
 * DOMAIN: FRONTEND
 * OBJECTIVE: Utilitários Globais de Formatação e Estilização.
 * FIX: Correção de Imports (clsx, tailwind-merge) e tipagem.
 */
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Combina classes Tailwind de forma inteligente, resolvendo conflitos de especificidade.
 * @param inputs - Lista de classes, condicionais ou objetos de classe.
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

/**
 * Formata um valor em centavos (Inteiro) para moeda BRL (String).
 * Ex: 1050 -> "R$ 10,50"
 * @param valueInCents - Valor inteiro representando centavos.
 * @param showSymbol - Define se o prefixo "R$" deve ser exibido.
 */
export function formatCurrency(
  valueInCents: number | undefined | null,
  showSymbol: boolean = true
): string {
  if (valueInCents === undefined || valueInCents === null) {
    return showSymbol ? "R$ 0,00" : "0,00";
  }
  const formatter = new Intl.NumberFormat('pt-BR', {
    style: showSymbol ? 'currency' : 'decimal',
    currency: 'BRL',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
  return formatter.format(valueInCents / 100);
}

/**
 * Converte uma string de input monetário (ex: "R$ 1.250,50") para centavos inteiros (125050).
 * Protege contra erros de ponto flutuante usando arredondamento matemático.
 * @param value - String ou número vindo de inputs.
 */
export function parseCurrencyInput(value: string | number): number {
  if (!value) return 0;
  // Converte para string e remove tudo que não for dígito ou separador decimal
  let cleanValue = String(value).replace(/[^\d,.-]/g, '');
  // Normaliza: substitui vírgula por ponto para conversão float
  cleanValue = cleanValue.replace(',', '.');
  const floatVal = parseFloat(cleanValue);
  if (isNaN(floatVal)) return 0;
  // Multiplica por 100 e arredonda para o inteiro mais próximo (centavo real)
  return Math.round(floatVal * 100);
}

/**
 * Converte centavos (1050) para string de input compatível com HTML (ex: "10.50").
 * @param valueInCents - Valor vindo do banco de dados.
 */
export function centsToInput(valueInCents: number | undefined | null): string {
  if (valueInCents === undefined || valueInCents === null) return "";
  return (valueInCents / 100).toFixed(2);
}
