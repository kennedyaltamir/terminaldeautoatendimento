import { buildOrderReceipt } from "./builder";
import { Order } from "@/types";

export function printOrder(order: Order, companyName: string) {
  try {
    const base64Data = buildOrderReceipt(order, companyName);
    
    // Detecta se é Android pelo User Agent
    const isAndroid = /Android/i.test(navigator.userAgent);

    if (isAndroid) {
      // Deep Link para RawBT (Protocolo Nativo)
      const intentUrl = `rawbt:base64,${base64Data}`;
      window.location.href = intentUrl;
    } else {
      // Fallback para PC (Browser Print)
      // Em um cenário real, aqui poderíamos chamar uma API local ou QZ Tray
      console.log("Ambiente Desktop detectado. Usando window.print() como fallback.");
      window.print();
    }
  } catch (e) {
    console.error("Erro na impressão:", e);
    alert("Erro ao gerar cupom de impressão.");
  }
}