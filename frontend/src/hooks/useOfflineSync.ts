/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 26.2.0 (Undefined Guard Fix)
 * DNA_ID: MF-HOOK-SYNC-V26-2
 * Objective: Prevent 'undefined' journey_id from crashing the API and tripping Circuit Breaker.
 */
"use client";

import { useEffect, useState, useCallback } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db, PendingDeliveryAction } from '@/lib/db';
import { toast } from 'sonner';

export function useOfflineSync() {
    const [isSyncing, setIsSyncing] = useState(false);
    const [dbReady, setDbReady] = useState(false);

    // 1. Database Connection Lifecycle
    useEffect(() => {
        const initDB = async () => {
            try {
                await db.safeOpen();
                setDbReady(true);
            } catch (error) {
                console.error("[IDB_FATAL] Falha ao abrir banco local:", error);
            }
        };
        initDB();
    }, []);

    // 2. Reactive Data Fetching
    const pendingActions = useLiveQuery(
        () => dbReady ? db.pendingActions.where('status').equals('pending').toArray() : Promise.resolve([] as PendingDeliveryAction[]),
        [dbReady]
    );

    const errorCountData = useLiveQuery(
        () => dbReady ? db.pendingActions.where('status').equals('error').count() : Promise.resolve(0),
        [dbReady]
    );

    const safePendingActions = pendingActions || [];
    const pendingCount = safePendingActions.length;
    const errorCount = errorCountData || 0;

    /**
     * Clear Queue (SRE Emergency Protocol)
     */
    const clearQueue = useCallback(async () => {
        if (!dbReady) return;
        try {
            await db.pendingActions.clear();
            toast.success("Fila de sincronização limpa.");
        } catch (e) {
            toast.error("Falha ao acessar banco local.");
        }
    }, [dbReady]);

    /**
     * Background Synchronization Sequence
     */
    const syncNow = useCallback(async () => {
        if (isSyncing || !navigator.onLine || !dbReady || pendingCount === 0) return;

        setIsSyncing(true);
        try {
            const token = localStorage.getItem('mesaflow_access_token');
            const apiBase = process.env.NEXT_PUBLIC_API_URL;

            for (const action of safePendingActions) {
                if (!action.id) continue;

                // 🛡️ GUARD: Impede envio de ID inválido que quebra o backend
                if (!action.journey_id || action.journey_id === 'undefined' || action.journey_id === 'null') {
                    console.warn(`[SYNC_SKIP] Ação ${action.id} possui journey_id inválido: ${action.journey_id}. Marcando como erro.`);
                    await db.pendingActions.update(action.id, { status: 'error', retryCount: 99 });
                    continue;
                }

                try {
                    const res = await fetch(`${apiBase}/mobile/logistics/journey/${action.journey_id}/status`, {
                        method: 'PATCH',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify(action.payload)
                    });

                    if (res.ok) {
                        await db.pendingActions.delete(action.id);
                        console.info(`[SYNC_SUCCESS] Evento ${action.id} transmitido.`);
                    } else {
                        // Se for 503, aborta o loop para não piorar o Circuit Breaker
                        if (res.status === 503) {
                            console.warn("[SYNC_PAUSE] Backend em proteção (503). Pausando sincronia.");
                            break;
                        }
                        
                        await db.pendingActions.update(action.id, { 
                            status: 'error',
                            retryCount: (action.retryCount || 0) + 1 
                        });
                    }
                } catch (fetchError) {
                    console.warn(`[SYNC_RETRY] Falha de transporte para ação ${action.id}.`);
                    break; 
                }
            }
        } finally {
            setIsSyncing(false);
        }
    }, [isSyncing, dbReady, safePendingActions, pendingCount]);

    // 🔄 Automatic Sync Trigger
    useEffect(() => {
        if (navigator.onLine && pendingCount > 0) {
            syncNow();
        }
    }, [pendingCount, syncNow]);

    return { 
        pendingCount, 
        errorCount, 
        isSyncing, 
        dbReady, 
        syncNow,
        clearQueue
    };
}
