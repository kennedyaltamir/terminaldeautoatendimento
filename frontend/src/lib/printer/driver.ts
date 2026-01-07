import { buildOrderReceipt, buildTestReceipt, EscPosBuilder } from "./builder";
import { generateSticker } from "./stickers";
import { Order, OrderItemResponse } from "@/types";

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

export function printSticker(order: Order, item: OrderItemResponse, index: number, totalItems: number, companyName: string) {
  try {
    const zplCode = generateSticker(order, item, index, totalItems, companyName);
    // ZPL é texto puro, mas o RawBT aceita base64 também.
    // Para ZPL, o RawBT prefere que enviemos como texto ou base64.
    // Vamos enviar base64 para manter consistência.
    const base64Data = window.btoa(zplCode);
    sendToRawBT(base64Data);
  } catch (e) {
    console.error("Erro na etiqueta:", e);
    alert("Erro ao gerar etiqueta.");
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

export function openCashDrawer() {
  try {
    const builder = new EscPosBuilder();
    builder.openDrawer();
    const base64 = builder.getBase64();
    sendToRawBT(base64);
  } catch (e) {
    console.error("Erro ao abrir gaveta:", e);
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
    // Em desktop não temos como abrir gaveta via browser sem WebSerial/USB
    // Mas o log ajuda no debug
  }
}
