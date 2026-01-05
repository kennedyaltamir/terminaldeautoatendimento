import { buildOrderReceipt, buildTestReceipt } from "./builder";
import { Order } from "@/types";

// Recupera a configuração salva ou usa padrão 58mm
function getPrinterWidth(): 58 | 80 {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem("mesaflow_printer_width");
    return saved === "80" ? 80 : 58;
  }
  return 58;
}

export function printOrder(order: Order, companyName: string) {
  try {
    const width = getPrinterWidth();
    const base64Data = buildOrderReceipt(order, companyName, width);
    sendToRawBT(base64Data);
  } catch (e) {
    console.error("Erro na impressão:", e);
    alert("Erro ao gerar cupom de impressão.");
  }
}

export function printTest() {
  try {
    const width = getPrinterWidth();
    const base64Data = buildTestReceipt(width);
    sendToRawBT(base64Data);
  } catch (e) {
    console.error("Erro no teste:", e);
    alert("Erro ao gerar teste.");
  }
}

function sendToRawBT(base64Data: string) {
  const isAndroid = /Android/i.test(navigator.userAgent);
  if (isAndroid) {
    const intentUrl = `rawbt:base64,${base64Data}`;
    window.location.href = intentUrl;
  } else {
    console.log("Ambiente Desktop. Simulando envio RawBT (Base64 no console).");
    console.log(base64Data);
    alert("Impressão Nativa (RawBT) funciona apenas no Android. No PC, use o driver do sistema.");
  }
}
