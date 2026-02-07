/**
 * Utilitário para decodificação segura de tokens JWT no lado do cliente.
 */
export function decodeJwtPayload(token: string): { impersonator?: boolean; [key: string]: any } {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return {};

    const payloadBase64Url = parts[1];
    // Converte Base64Url para Base64 padrão
    const base64 = payloadBase64Url.replace(/-/g, '+').replace(/_/g, '/');
    
    // Decodifica tratando caracteres especiais (Unicode)
    const jsonPayload = decodeURIComponent(
      window.atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );

    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error("🚨 Falha crítica na decodificação do JWT:", error);
    return {}; // Retorno vazio garante isImpersonator = false
  }
}
