"use client";

import { useState, useEffect } from "react";
import { X, Bike, User, Loader2 } from "lucide-react";
import Modal from "@/components/ui/Modal";
import { getDrivers, dispatchOrder } from "@/lib/api";
import { Employee } from "@/types";
import { toast } from "sonner";

interface DispatchModalProps {
  isOpen: boolean;
  onClose: () => void;
  orderId: string;
  onSuccess: () => void;
}

export default function DispatchModal({ isOpen, onClose, orderId, onSuccess }: DispatchModalProps) {
  const [drivers, setDrivers] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDriver, setSelectedDriver] = useState<number | null>(null);
  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      getDrivers()
        .then(setDrivers)
        .catch(() => toast.error("Erro ao carregar entregadores"))
        .finally(() => setLoading(false));
    }
  }, [isOpen]);

  const handleDispatch = async () => {
    setProcessing(true);
    try {
      await dispatchOrder(orderId, selectedDriver || undefined);
      toast.success("Pedido despachado com sucesso!");
      onSuccess();
      onClose();
    } catch (e) {
      toast.error("Erro ao despachar");
    } finally {
      setProcessing(false);
    }
  };

  if (!isOpen) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Despachar Pedido">
      <div className="space-y-4">
        <p className="text-sm text-gray-500">Selecione um entregador para levar este pedido:</p>

        <div className="max-h-[50vh] overflow-y-auto space-y-2">
          {loading ? (
            <p className="text-center py-4 text-gray-400">Carregando...</p>
          ) : drivers.length === 0 ? (
            <div className="text-center py-4 bg-gray-50 rounded-lg border border-dashed border-gray-300">
              <p className="text-sm text-gray-500">Nenhum entregador cadastrado.</p>
              <p className="text-xs text-gray-400 mt-1">Cadastre em Equipe {'>'} Novo Membro</p>
            </div>
          ) : (
            drivers.map(driver => (
              <button
                key={driver.id}
                onClick={() => setSelectedDriver(driver.id)}
                className={`w-full flex items-center gap-3 p-3 rounded-xl border transition-all text-left ${
                  selectedDriver === driver.id 
                    ? 'border-blue-500 bg-blue-50 ring-1 ring-blue-500' 
                    : 'border-gray-200 hover:bg-gray-50'
                }`}
              >
                <div className={`p-2 rounded-full ${selectedDriver === driver.id ? 'bg-blue-200 text-blue-700' : 'bg-gray-200 text-gray-600'}`}>
                  <User size={20} />
                </div>
                <div>
                  <p className="font-bold text-gray-900">{driver.name}</p>
                  <p className="text-xs text-gray-500">Disponível</p>
                </div>
              </button>
            ))
          )}
        </div>

        <div className="flex gap-2 pt-2">
          <button 
            onClick={() => { setSelectedDriver(null); handleDispatch(); }}
            className="flex-1 border border-gray-300 text-gray-600 py-3 rounded-xl font-bold hover:bg-gray-50 transition-colors text-sm"
          >
            Sem Entregador
          </button>
          <button 
            onClick={handleDispatch}
            disabled={processing}
            className="flex-[2] bg-blue-600 text-white py-3 rounded-xl font-bold hover:bg-blue-700 transition-colors flex items-center justify-center gap-2 shadow-lg shadow-blue-200 disabled:opacity-70"
          >
            {processing ? <Loader2 className="animate-spin" /> : <Bike size={20} />}
            Iniciar Entrega
          </button>
        </div>
      </div>
    </Modal>
  );
}