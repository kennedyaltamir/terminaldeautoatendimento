/**
 * DOMAIN: UI / UX
 * COMPONENT: ModalManager
 * OBJECTIVE: Fila de modais com prioridade e persistência.
 */
import React, { createContext, useContext, useState, useEffect } from 'react';

type ModalType = 'INCIDENT' | 'COMMUNICATION' | 'CONFIRMATION' | 'INFO';

interface ModalItem {
  id: string;
  type: ModalType;
  content: React.ReactNode;
  priority: number; // 0 (High) - 10 (Low)
}

const ModalContext = createContext<any>(null);

export function ModalProvider({ children }: { children: React.ReactNode }) {
  const [modalQueue, setModalQueue] = useState<ModalItem[]>([]);

  // 1. Inserção com Ordenação
  const openModal = (item: Omit<ModalItem, 'id'>) => {
    const id = Math.random().toString(36).substr(2, 9);
    const priorityMap: Record<ModalType, number> = {
      'INCIDENT': 0,
      'COMMUNICATION': 1,
      'CONFIRMATION': 2,
      'INFO': 3
    };
    
    const newItem = { ...item, id, priority: priorityMap[item.type] };

    setModalQueue(prev => {
      const newQueue = [...prev, newItem].sort((a, b) => a.priority - b.priority);
      // Persistência para recuperação de crash
      sessionStorage.setItem('mf_modal_queue', JSON.stringify(newQueue));
      return newQueue;
    });
  };

  const closeModal = () => {
    setModalQueue(prev => {
      const newQueue = prev.slice(1); // Remove o primeiro (ativo)
      sessionStorage.setItem('mf_modal_queue', JSON.stringify(newQueue));
      return newQueue;
    });
  };

  // 2. Recuperação de Crash (Hydration)
  useEffect(() => {
    const saved = sessionStorage.getItem('mf_modal_queue');
    if (saved) {
      try {
        // Nota: React Nodes não serializam bem, aqui recuperaríamos apenas os IDs/Tipos
        // e reconstruiríamos o conteúdo. Simplificado para o exemplo.
        // setModalQueue(JSON.parse(saved)); 
      } catch (e) {}
    }
  }, []);

  const activeModal = modalQueue[0]; // Sempre exibe o de maior prioridade

  return (
    <ModalContext.Provider value={{ openModal, closeModal }}>
      {children}
      {activeModal && (
        <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/80">
           {/* Renderização do Modal Ativo */}
           {activeModal.content}
        </div>
      )}
    </ModalContext.Provider>
  );
}