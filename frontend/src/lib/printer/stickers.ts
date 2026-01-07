import { Order, OrderItemResponse } from "@/types";

function removeAccents(str: string): string {
  return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

export class ZplBuilder {
  private buffer: string = "";

  constructor() {
    this.buffer += "^XA"; // Start Format
    this.buffer += "^CI28"; // UTF-8 Encoding (Tentativa, mas ZPL puro prefere ASCII)
    this.buffer += "^PW400"; // Print Width (40mm aprox em 203dpi)
    this.buffer += "^LL300"; // Label Length (30mm aprox)
    this.buffer += "^PON"; // Print Orientation Normal
  }

  text(x: number, y: number, content: string, fontSize: number = 30, bold: boolean = false) {
    // ^FO: Field Origin
    // ^A0: Font 0 (Scalable)
    // ^FD: Field Data
    // ^FS: Field Separator
    const cleanContent = removeAccents(content);
    this.buffer += `^FO${x},${y}^A0N,${fontSize},${fontSize}^FD${cleanContent}^FS`;
    return this;
  }

  box(x: number, y: number, w: number, h: number, thickness: number = 2) {
    this.buffer += `^FO${x},${y}^GB${w},${h},${thickness}^FS`;
    return this;
  }

  line(x: number, y: number, w: number) {
    return this.box(x, y, w, 2);
  }

  end() {
    this.buffer += "^XZ"; // End Format
    return this.buffer;
  }
}

export function generateSticker(order: Order, item: OrderItemResponse, index: number, totalItems: number, companyName: string): string {
  const zpl = new ZplBuilder();
  
  // Cabeçalho
  zpl.text(20, 20, companyName.substring(0, 20), 25);
  zpl.text(250, 20, `#${order.id.slice(0, 4)}`, 25);
  zpl.line(10, 50, 380);

  // Item Principal
  zpl.text(20, 70, `${item.quantity}x ${item.product.name}`.substring(0, 25), 35);

  let currentY = 110;

  // Opcionais
  if (item.selected_options && item.selected_options.length > 0) {
    item.selected_options.forEach(opt => {
      zpl.text(40, currentY, `+ ${opt.name}`.substring(0, 30), 25);
      currentY += 30;
    });
  }

  // Observações (Destaque)
  if (item.notes) {
    currentY += 10;
    zpl.box(15, currentY - 5, 370, 40, 2); // Caixa ao redor da obs
    zpl.text(25, currentY, `OBS: ${item.notes}`.substring(0, 25), 25);
    currentY += 50;
  }

  // Rodapé
  zpl.line(10, 250, 380);
  zpl.text(20, 260, order.customer_name?.substring(0, 15) || "Cliente", 25);
  zpl.text(250, 260, `Item ${index + 1}/${totalItems}`, 25);

  return zpl.end();
}
