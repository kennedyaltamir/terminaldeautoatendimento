import { COMMANDS, LF } from "./commands";
import { Order } from "@/types";

export class EscPosBuilder {
  private buffer: number[] = [];
  private width: number;

  // 32 colunas = 58mm (Fonte A)
  // 48 colunas = 80mm (Fonte A)
  constructor(paperWidth: 58 | 80 = 58) {
    this.add(COMMANDS.INIT);
    this.width = paperWidth === 58 ? 32 : 48;
  }

  private add(bytes: number[]) {
    this.buffer.push(...bytes);
  }

  private addString(str: string) {
    const cleanStr = str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    for (let i = 0; i < cleanStr.length; i++) {
      const code = cleanStr.charCodeAt(i);
      if ((code >= 32 && code <= 126) || code === LF) {
        this.buffer.push(code);
      } else {
        this.buffer.push(0x3F);
      }
    }
  }

  text(str: string): this {
    this.addString(str);
    return this;
  }

  line(str: string = ""): this {
    this.addString(str);
    this.buffer.push(LF);
    return this;
  }

  feed(lines: number = 1): this {
    for (let i = 0; i < lines; i++) {
      this.buffer.push(LF);
    }
    return this;
  }

  align(mode: 'LEFT' | 'CENTER' | 'RIGHT'): this {
    this.add(COMMANDS.ALIGN[mode]);
    return this;
  }

  bold(enabled: boolean): this {
    this.add(enabled ? COMMANDS.TXT_BOLD_ON : COMMANDS.TXT_BOLD_OFF);
    return this;
  }

  style(mode: 'NORMAL' | 'LARGE'): this {
    this.add(mode === 'LARGE' ? COMMANDS.TXT_SIZE.QUAD : COMMANDS.TXT_SIZE.NORMAL);
    return this;
  }

  row(left: string, right: string): this {
    const leftClean = left.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    const rightClean = right.normalize("NFD").replace(/[\u0300-\u036f]/g, "");

    const maxLeft = this.width - rightClean.length - 1;
    const leftTrunc = leftClean.substring(0, maxLeft);

    const spaceLen = this.width - leftTrunc.length - rightClean.length;
    const spaces = spaceLen > 0 ? " ".repeat(spaceLen) : " ";

    this.line(`${leftTrunc}${spaces}${rightClean}`);
    return this;
  }

  qrCode(data: string): this {
    if (!data) return this;
    this.add(COMMANDS.QR.MODEL);
    this.add(COMMANDS.QR.SIZE);
    this.add(COMMANDS.QR.ERROR);
    const len = data.length + 3;
    const pL = len % 256;
    const pH = Math.floor(len / 256);
    this.add(COMMANDS.QR.STORE);
    this.add([pL, pH, 0x31, 0x50, 0x30]);
    this.addString(data);
    this.add(COMMANDS.QR.PRINT);
    return this;
  }

  cut(): this {
    this.feed(3);
    this.add(COMMANDS.CUT);
    return this;
  }

  getBase64(): string {
    const uint8 = new Uint8Array(this.buffer);
    let binary = "";
    const len = uint8.byteLength;
    for (let i = 0; i < len; i++) {
      binary += String.fromCharCode(uint8[i]);
    }
    return window.btoa(binary);
  }
}

export function buildOrderReceipt(order: Order, companyName: string, width: 58 | 80 = 58): string {
  const printer = new EscPosBuilder(width);

  printer
    .align('CENTER')
    .bold(true).line(companyName.toUpperCase()).bold(false)
    .line("-".repeat(width))
    .align('LEFT')
    .line(`PEDIDO: #${order.id.slice(0, 6)}`)
    .line(`DATA: ${new Date(order.created_at).toLocaleTimeString('pt-BR')}`)
    .line("-".repeat(width))
    .style('LARGE')
    .align('CENTER')
    .line(order.order_type === 'delivery' ? "DELIVERY" : `MESA ${order.table?.table_number || 'BALCAO'}`)
    .style('NORMAL')
    .align('LEFT')
    .line(`CLIENTE: ${order.customer_name || 'Nao Informado'}`)
    .line("-".repeat(width))
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
    .line("-".repeat(width))
    .align('RIGHT')
    .style('LARGE').line(`TOTAL: R$ ${Number(order.total_amount).toFixed(2)}`).style('NORMAL')
    .align('LEFT')
    .line(`PAGAMENTO: ${order.payment_method.toUpperCase()}`)
    .line(`STATUS: ${order.payment_status.toUpperCase()}`)
    .align('CENTER')
    .feed(1);

  if (order.payment_method === 'online' && order.payment_status === 'pending' && order.mp_qr_code) {
    printer
      .line("PAGUE COM PIX:")
      .qrCode(order.mp_qr_code)
      .feed(1);
  }

  printer
    .line("MesaFlow Tecnologia")
    .cut();

  return printer.getBase64();
}

export function buildTestReceipt(width: 58 | 80 = 58): string {
  const printer = new EscPosBuilder(width);
  const line = "-".repeat(width);

  printer
    .align('CENTER')
    .style('LARGE').line("TESTE DE IMPRESSAO").style('NORMAL')
    .line("MesaFlow Tecnologia")
    .feed(1)
    .align('LEFT')
    .line(`Largura Configurada: ${width}mm`)
    .line(`Colunas: ${width === 58 ? 32 : 48} chars`)
    .line(line)
    .bold(true).line("TESTE DE ALINHAMENTO").bold(false)
    .align('LEFT').line("Esquerda")
    .align('CENTER').line("Centro")
    .align('RIGHT').line("Direita")
    .align('LEFT')
    .line(line)
    .bold(true).line("TESTE DE TABULACAO").bold(false)
    .row("Item Esquerda", "R$ 10,00")
    .row("Item Longo Quebra Linha Automaticamente", "R$ 99,90")
    .line(line)
    .align('CENTER')
    .qrCode("https://mesaflow.com.br")
    .line("QR Code Teste")
    .feed(2)
    .cut();

  return printer.getBase64();
}
