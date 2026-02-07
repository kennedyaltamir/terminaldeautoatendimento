/**
 * RealtimeEvent: Definição centralizada do contrato de eventos 
 * entre o Backend MesaFlow e os Clientes Nativos.
 * Atualizado na Missão 32 para suportar chamados de mesa com ID.
 */
export type RealtimeEvent = 
  | { type: 'new_order'; order_id: string }
  | { type: 'order_update'; order_id: string; status: string }
  | { 
      type: 'waiter_call'; 
      id: number; 
      table: number; 
      service_type: string; 
      notes?: string 
    };
