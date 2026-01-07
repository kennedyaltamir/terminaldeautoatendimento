import { decode as atob } from 'base-64';

/**
 * @file jwt.ts
 * @description Utilitário para decodificação segura de tokens JWT no ambiente Mobile.
 * Utiliza a biblioteca base-64 para compatibilidade com React Native.
 */
export function decodeJwtPayload(token: string): { impersonator?: boolean; [key: string]: any } {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return {};

    const payloadBase64Url = parts[1];
    // Converte Base64Url para Base64 padrão
    const base64 = payloadBase64Url.replace(/-/g, '+').replace(/_/g, '/');
    
    // Decodifica a string Base64
    const decoded = atob(base64);

    // Trata caracteres especiais (Unicode) para evitar erros de parse JSON
    const jsonPayload = decoded
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('');

    return JSON.parse(decodeURIComponent(jsonPayload));
  } catch (error) {
    console.error("🚨 Falha crítica na decodificação do JWT Mobile:", error);
    return {}; // Retorno vazio garante isImpersonator = false (Fail Secure)
  }
}
