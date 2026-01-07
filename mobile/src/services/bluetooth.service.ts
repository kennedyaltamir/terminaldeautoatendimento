import { logger } from './logger.service';

/**
 * BluetoothService: Interface de comunicação com hardware Bluetooth.
 */

const TAG = 'BluetoothService';

export interface BluetoothDevice {
  id: string;
  name: string;
  address: string;
}

class BluetoothService {
  private static instance: BluetoothService;
  private connectedDeviceId: string | null = null;

  private constructor() {}

  public static getInstance(): BluetoothService {
    if (!BluetoothService.instance) {
      BluetoothService.instance = new BluetoothService();
    }
    return BluetoothService.instance;
  }

  public async scanDevices(): Promise<BluetoothDevice[]> {
    logger.info(TAG, 'Iniciando busca por impressoras Bluetooth...');
    await new Promise(resolve => setTimeout(resolve, 1500));

    return [
      { id: '1', name: 'Impressora Térmica 58mm', address: '00:11:22:33:44:55' },
      { id: '2', name: 'MTP-II Portable', address: 'AA:BB:CC:DD:EE:FF' },
      { id: '3', name: 'Zebra ZQ320', address: '11:22:33:44:55:66' },
    ];
  }

  public async connect(deviceId: string): Promise<boolean> {
    logger.info(TAG, `Tentando conectar ao dispositivo ${deviceId}`);
    await new Promise(resolve => setTimeout(resolve, 1000));
    this.connectedDeviceId = deviceId;
    return true;
  }

  public async write(data: Uint8Array): Promise<boolean> {
    if (!this.connectedDeviceId) return false;
    logger.info(TAG, `Enviando ${data.length} bytes para a impressora...`);
    await new Promise(resolve => setTimeout(resolve, 500));
    return true;
  }

  public disconnect() {
    this.connectedDeviceId = null;
  }
}

export const bluetoothService = BluetoothService.getInstance();
