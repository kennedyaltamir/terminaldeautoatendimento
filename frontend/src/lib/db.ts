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

export class MesaFlowDB extends Dexie {
  pendingOrders!: Table<PendingOrder>;

  constructor() {
    super('MesaFlowDB');
    this.version(1).stores({
      pendingOrders: '++id, slug, status, createdAt'
    });
  }
}

export const db = new MesaFlowDB();