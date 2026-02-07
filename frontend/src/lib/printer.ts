/**
 * DOMAIN: FRONTEND
 * OBJECTIVE: Gerador de comandos ESC/POS e ZPL para impressão térmica.
 * FIX: Tipagem explícita no loop de opções para resolver TS7006.
 */
import { Order } from "@/types";

const ESC = "\x1B";
const GS = "\x1D";
const LF = "\x0A";

const COMMANDS = {
  INIT: ESC + "@",
  ALIGN_LEFT: ESC + "a" + "\x00",
  ALIGN_CENTER: ESC + "a" + "\x01",
  ALIGN_RIGHT: ESC + "a" + "\x02",
  BOLD_ON: ESC + "E" + "\x01",
  BOLD_OFF: ESC + "E" + "\x00",
  TEXT_NORMAL: GS + "!" + "\x00",
  TEXT_DOUBLE_HEIGHT: GS + "!" + "\x01",
  TEXT_DOUBLE_WIDTH: GS + "!" + "\x10",
  TEXT_QUAD: GS + "!" + "\x11",
  CUT_FULL: GS + "V" + "\x41" + "\x00",
  CUT_PARTIAL: GS + "V" + "\x42" + "\x00",
};

function removeAccents(str: string): string {
  return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

export class EscPosBuilder {
  private buffer: string = "";

  constructor() {
    this.buffer += COMMANDS.INIT;
  }

  align(align: 'left' | 'center' | 'right') {
    const map = { left: COMMANDS.ALIGN_LEFT, center: COMMANDS.ALIGN_CENTER, right: COMMANDS.ALIGN_RIGHT };
    this.buffer += map[align];
    return this;
  }

  style(style: 'normal' | 'bold' | 'large') {
    if (style === 'bold') this.buffer += COMMANDS.BOLD_ON;
    else if (style === 'large') this.buffer += COMMANDS.TEXT_QUAD;
    else {
      this.buffer += COMMANDS.BOLD_OFF;
      this.buffer += COMMANDS.TEXT_NORMAL;
    }
    return this;
  }

  text(content: string) {
    this.buffer += removeAccents(content);
    return this;
  }

  line(content: string = "") {
    this.text(content + LF);
    return this;
  }

  feed(lines: number = 1) {
    this.buffer += LF.repeat(lines);
    return this;
  }

  cut() {
    this.feed(3);
    this.buffer += COMMANDS.CUT_PARTIAL;
    return this;
  }

  separator() {
    return this.line("-".repeat(32));
  }

  kv(key: string, value: string) {
    const k = removeAccents(key).substring(0, 12).padEnd(12);
    const v = removeAccents(value).substring(0, 20).padStart(20);
    return this.line(`${k}${v}`);
  }

  getBase64(): string {
    const binaryString = Array.from(this.buffer, (c) => c.charCodeAt(0).toString(16).padStart(2, "0")).join("");
    
    // Conversão segura de Hex para Base64
    const match = binaryString.match(/.{1,2}/g);
    if (!match) return "";
    
    const uint8 = new Uint8Array(match.map((byte) => parseInt(byte, 16)));
    let binary = "";
    const len = uint8.byteLength;
    for (let i = 0; i < len; i++) {
      binary += String.fromCharCode(uint8[i]);
    }
    return window.btoa(binary);
  }
}

export function generateReceipt(order: Order, companyName: string): string {
  const p = new EscPosBuilder();

  // Cabeçalho
  p.align('center').style('bold').line(companyName.toUpperCase()).style('normal');
  p.line(new Date(order.created_at).toLocaleString('pt-BR'));
  p.separator();

  // Info Principal
  p.align('left').style('large');
  if (order.order_type === 'delivery') {
    p.line("DELIVERY");
  } else {
    p.line(`MESA ${order.table?.table_number || 'BALCAO'}`);
  }
  p.style('normal');
  
  p.line(`CLIENTE: ${order.customer_name || 'Nao Informado'}`);
  p.line(`PEDIDO: #${order.id.slice(0, 6)}`);
  p.separator();

  // Itens
  p.align('left').style('bold').line("QTD ITEM             TOTAL").style('normal');
  
  order.items.forEach(item => {
    const total = Number(item.product.price) * item.quantity;
    const qty = `${item.quantity}x`.padEnd(3);
    const name = removeAccents(item.product.name).substring(0, 18).padEnd(18);
    const price = total.toFixed(2).padStart(11);
    
    p.line(`${qty}${name}${price}`);

    if (item.selected_options?.length) {
      // FIX: Tipagem explícita para resolver erro TS7006
      item.selected_options.forEach((opt: { name: string }) => {
        p.line(`   + ${opt.name.substring(0, 25)}`);
      });
    }
    
    if (item.notes) {
      p.line(`   (OBS: ${item.notes.substring(0, 25)})`);
    }
  });

  p.separator();

  // Totais
  p.align('right').style('large');
  p.line(`TOTAL: R$ ${Number(order.total_amount).toFixed(2)}`);
  p.style('normal').align('left');
  
  p.kv("PAGAMENTO:", order.payment_method.toUpperCase());
  p.kv("STATUS:", order.payment_status.toUpperCase());

  // Rodapé
  p.feed(1).align('center');
  p.line("MesaFlow Tecnologia");
  p.cut();

  return p.getBase64();
}

export function printViaRawBT(order: Order, companyName: string) {
  try {
    const base64 = generateReceipt(order, companyName);
    const url = `rawbt:base64,${base64}`;
    window.location.href = url;
  } catch (e) {
    console.error("Erro ao gerar impressão:", e);
    alert("Erro ao gerar comando de impressão.");
  }
}
