import { EscPosEncoder } from '../lib/escpos.encoder';
import { bluetoothService } from './bluetooth.service';
import { logger } from './logger.service';

/**
 * PrinterService: Orquestrador de formatação e despacho de recibos.
 */

const TAG = 'PrinterService';

export const PrinterService = {
  /**
   * Gera o buffer binário e envia para o hardware Bluetooth.
   */
  async printOrder(order: any, companyName: string, printerId: string): Promise<boolean> {
    try {
      // 1. Gerar Buffer
      const buffer = this.generateOrderReceipt(order, companyName);
      
      // 2. Garantir Conexão
      const connected = await bluetoothService.connect(printerId);
      if (!connected) return false;

      // 3. Despachar
      return await bluetoothService.write(buffer);
    } catch (e) {
      logger.error(TAG, 'Falha no fluxo de impressão', e);
      return false;
    }
  },

  /**
   * Formata o recibo (Lógica de 30A preservada e refinada).
   */
  generateOrderReceipt(order: any, companyName: string): Uint8Array {
    const encoder = new EscPosEncoder();

    encoder
      .align('CENTER')
      .size('LARGE')
      .line(companyName.toUpperCase())
      .size('NORMAL')
      .line('--------------------------------')
      .align('LEFT')
      .bold(true).line(`PEDIDO: #${order.id.slice(0, 6)}`).bold(false)
      .line(`DATA: ${new Date().toLocaleString('pt-BR')}`)
      .line(`MESA: ${order.table_number || 'BALCAO'}`)
      .line('--------------------------------')
      .bold(true).line('QTD  ITEM                TOTAL').bold(false);

    order.items.forEach((item: any) => {
      const qty = item.quantity.toString().padEnd(4);
      const name = item.name || 'Item';
      const price = (item.price * item.quantity).toFixed(2);
      encoder.line(`${qty} ${name.substring(0, 15).padEnd(15)} ${price.padStart(8)}`);
    });

    encoder
      .line('--------------------------------')
      .align('RIGHT')
      .size('LARGE')
      .bold(true).line(`TOTAL: R$ ${order.total_amount.toFixed(2)}`)
      .size('NORMAL')
      .bold(false)
      .feed(2)
      .align('CENTER')
      .line('MesaFlow - Mobile POS')
      .cut();

    return encoder.getBuffer();
  }
};
