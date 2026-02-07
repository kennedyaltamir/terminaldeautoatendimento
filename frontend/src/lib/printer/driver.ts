/**
 * DOMAIN: FRONTEND
 * OBJECTIVE: Driver de Impressão Unificado (L6 Standard).
 * FIX: Remoção de código UI colado acidentalmente e limpeza de logs.
 */
import { buildOrderReceipt, buildTestReceipt, EscPosBuilder } from "./builder";
import { generateSticker } from "./stickers";
import { Order, OrderItemResponse } from "@/types";

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
  }
}

export function printSticker(order: Order, item: OrderItemResponse, index: number, totalItems: number, companyName: string) {
  try {
    const zplCode = generateSticker(order, item, index, totalItems, companyName);
    const base64Data = window.btoa(zplCode);
    sendToRawBT(base64Data);
  } catch (e) {
    console.error("Erro na etiqueta:", e);
  }
}

export function printTest() {
  try {
    const width = getPrinterWidth();
    const base64Data = buildTestReceipt(width);
    sendToRawBT(base64Data);
  } catch (e) {
    console.error("Erro no teste:", e);
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
    // 🛡️ FIX: console.log -> console.info/debug para simulação desktop
    console.info("Ambiente Desktop. Simulando envio RawBT (Base64 no console).");
    console.debug(base64Data);
  }
}
