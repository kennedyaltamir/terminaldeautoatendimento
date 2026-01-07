import Dexie, { Table } from 'dexie';

export interface PendingOrder {
  id?: number;
  slug: string;
  payload: any;
  createdAt: Date;
  status: 'pending' | 'error';
  errorMessage?: string;
  retryCount: number;
}

export interface FiscalQueueItem {
  id?: number;
  orderId: string;
  slug: string;
  status: 'pending' | 'error';
  createdAt: Date;
  retryCount: number;
  errorMessage?: string;
}

export class MesaFlowDB extends Dexie {
  pendingOrders!: Table<PendingOrder>;
  fiscalQueue!: Table<FiscalQueueItem>; // Nova tabela para contingência fiscal

  constructor() {
    super('MesaFlowDB');
    this.version(2).stores({ // Incrementado para v2
      pendingOrders: '++id, slug, status, createdAt',
      fiscalQueue: '++id, orderId, slug, status, createdAt'
    });
  }
}

export const db = new MesaFlowDB();
