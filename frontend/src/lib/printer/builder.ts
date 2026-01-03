import { COMMANDS, LF } from "./commands";
import { Order } from "@/types";

const PAPER_WIDTH = 32; // Padrão 58mm (Seguro). Para 80mm seria 48.

export class EscPosBuilder {
  private buffer: string = "";

  constructor() {
    this.buffer = COMMANDS.INIT;
  }

  private removeAccents(str: string): string {
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  }

  text(str: string): this {
    this.buffer += this.removeAccents(str);
    return this;
  }

  line(str: string = ""): this {
    this.text(str + LF);
    return this;
  }

  align(mode: 'LEFT' | 'CENTER' | 'RIGHT'): this {
    const cmd = mode === 'CENTER' ? COMMANDS.ALIGN_CENTER : mode === 'RIGHT' ? COMMANDS.ALIGN_RIGHT : COMMANDS.ALIGN_LEFT;
    this.buffer += cmd;
    return this;
  }

  bold(enabled: boolean): this {
    this.buffer += enabled ? COMMANDS.TXT_BOLD_ON : COMMANDS.TXT_BOLD_OFF;
    return this;
  }

  style(mode: 'NORMAL' | 'LARGE'): this {
    this.buffer += mode === 'LARGE' ? COMMANDS.TXT_QUAD : COMMANDS.TXT_NORMAL;
    return this;
  }

  // Imprime "Item ........ R$ 10,00" com espaçamento calculado
  row(left: string, right: string): this {
    const leftSanitized = this.removeAccents(left).substring(0, PAPER_WIDTH); 
    const rightSanitized = this.removeAccents(right);
    
    const spaceLen = PAPER_WIDTH - leftSanitized.length - rightSanitized.length;
    const spaces = spaceLen > 0 ? " ".repeat(spaceLen) : " ";
    
    this.buffer += leftSanitized + spaces + rightSanitized + LF;
    return this;
  }

  cut(): this {
    this.buffer += LF + LF + LF + COMMANDS.CUT;
    return this;
  }

  getRaw(): string {
    return this.buffer;
  }
  
  getBase64(): string {
    // Conversão segura de string binária para Base64 no browser
    const binaryString = Array.from(this.buffer, (c) => c.charCodeAt(0).toString(16).padStart(2, "0")).join("");
    
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

export function buildOrderReceipt(order: Order, companyName: string): string {
  const printer = new EscPosBuilder();

  printer
    .align('CENTER')
    .bold(true).line(companyName.toUpperCase()).bold(false)
    .line("--------------------------------")
    .align('LEFT')
    .line(`PEDIDO: #${order.id.slice(0, 6)}`)
    .line(`DATA: ${new Date(order.created_at).toLocaleTimeString('pt-BR')}`)
    .line("--------------------------------")
    .style('LARGE')
    .line(order.order_type === 'delivery' ? "DELIVERY" : `MESA ${order.table?.table_number || 'BALCAO'}`)
    .style('NORMAL')
    .line(`CLIENTE: ${order.customer_name || 'Nao Informado'}`)
    .line("--------------------------------")
    .bold(true).row("ITEM", "TOTAL").bold(false);

  order.items.forEach(item => {
    const total = item.quantity * Number(item.product.price);
    printer.row(
      `${item.quantity}x ${item.product.name}`,
      total.toFixed(2)
    );
    
    if (item.selected_options && item.selected_options.length > 0) {
      item.selected_options.forEach(opt => {
        printer.line(`  + ${opt.name}`);
      });
    }

    if (item.notes) printer.line(`  (Obs: ${item.notes})`);
  });

  printer
    .line("--------------------------------")
    .align('RIGHT')
    .style('LARGE').line(`TOTAL: R$ ${Number(order.total_amount).toFixed(2)}`).style('NORMAL')
    .align('LEFT')
    .line(`PAGAMENTO: ${order.payment_method.toUpperCase()}`)
    .line(`STATUS: ${order.payment_status.toUpperCase()}`)
    .align('CENTER')
    .line(LF)
    .line("MesaFlow Tecnologia")
    .cut();

  return printer.getBase64();
}