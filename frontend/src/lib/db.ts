import Dexie, { Table } from 'dexie';

// Interfaces de Tipo para as Tabelas
export interface PendingOrder {
    id?: number;
    slug: string;
    payload: any;
    status: 'pending' | 'synced' | 'error';
    errorMessage?: string;
    retryCount: number;
    createdAt: Date;
}

export interface TelemetryPoint {
    id?: number;
    journey_id: string;
    lat: number;
    lng: number;
    speed: number;
    accuracy: number;
    timestamp: number;
    ts: string;
    sync_status: 'pending' | 'synced';
    checksum: string; // Garantia de integridade
}

export interface PendingDeliveryAction {
    id?: number;
    journey_id: string;
    action_type: 'STATUS_UPDATE' | 'INCIDENT';
    payload: {
        status: string;
        pod_code?: string;
        reason?: string;
        tip_amount?: number;
    };
    status: 'pending' | 'synced' | 'error';
    createdAt: Date;
    retryCount: number;
}

export class MesaFlowDB extends Dexie {
    pendingOrders!: Table<PendingOrder>;
    telemetry!: Table<TelemetryPoint>;
    pendingActions!: Table<PendingDeliveryAction>;
    fiscalQueue!: Table<any>; 

    constructor() {
        super('MesaFlowDB');
        
        // Definição do Schema
        // Versionamento incrementado para 25 para garantir migration
        this.version(25).stores({
            pendingOrders: '++id, slug, status, createdAt',
            telemetry: '++id, journey_id, timestamp, sync_status', 
            pendingActions: '++id, journey_id, status, createdAt',
            fiscalQueue: '++id, orderId, status'
        });
    }

    async safeOpen() {
        try {
            if (this.isOpen()) return this;
            return await this.open();
        } catch (e: any) {
            console.error(`[DB_FATAL] ${e.message}`);
            if (e.name === 'VersionError') {
                console.warn("Recriando banco local devido a erro de versão.");
                await Dexie.delete('MesaFlowDB');
                return await this.open();
            }
            throw e;
        }
    }
}

export const db = new MesaFlowDB();
