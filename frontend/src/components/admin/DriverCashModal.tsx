"use client";

import { useState, useEffect } from "react";
import { X, DollarSign, CheckCircle2, Loader2, AlertTriangle } from "lucide-react";
import Modal from "@/components/ui/Modal";
import { getDriversWithBalance, settleDriverDebt } from "@/lib/api";
import { toast } from "sonner";

interface DriverDebt {
  driver_id: number;
  driver_name: string;
  current_debt: number;
}

interface DriverCashModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function DriverCashModal({ isOpen, onClose }: DriverCashModalProps) {
  const [drivers, setDrivers] = useState<DriverDebt[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDriver, setSelectedDriver] = useState<DriverDebt | null>(null);
  const [amount, setAmount] = useState("");
  const [processing, setProcessing] = useState(false);

  const fetchDrivers = async () => {
    setLoading(true);
    try {
      const data = await getDriversWithBalance();
      // Filtra apenas quem tem dívida positiva
      setDrivers(data.filter((d: DriverDebt) => d.current_debt > 0));
    } catch (e) {
      toast.error("Erro ao carregar saldos");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) fetchDrivers();
  }, [isOpen]);

  const handleSettle = async () => {
    if (!selectedDriver || !amount) return;
    
    const val = parseFloat(amount.replace(",", "."));
    if (isNaN(val) || val <= 0) return toast.error("Valor inválido");

    setProcessing(true);
    try {
      await settleDriverDebt(selectedDriver.driver_id, val, "Baixa manual pelo gerente");
      toast.success("Pagamento registrado!");
      setSelectedDriver(null);
      setAmount("");
      fetchDrivers();
    } catch (e) {
      toast.error("Erro ao registrar pagamento");
    } finally {
      setProcessing(false);
    }
  };

  if (!isOpen) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Prestação de Contas">
      <div className="space-y-6">
        {!selectedDriver ? (
          <>
            <p className="text-sm text-gray-500">Selecione um entregador para dar baixa:</p>
            <div className="max-h-[50vh] overflow-y-auto space-y-2">
              {loading ? (
                <div className="text-center py-8"><Loader2 className="animate-spin mx-auto text-gray-400" /></div>
              ) : drivers.length === 0 ? (
                <div className="text-center py-8 text-gray-500 bg-gray-50 rounded-xl border border-dashed border-gray-300">
                  <CheckCircle2 className="mx-auto mb-2 text-green-500" />
                  <p>Tudo certo! Ninguém deve nada.</p>
                </div>
              ) : (
                drivers.map(driver => (
                  <button
                    key={driver.driver_id}
                    onClick={() => { setSelectedDriver(driver); setAmount(driver.current_debt.toFixed(2)); }}
                    className="w-full flex justify-between items-center p-4 rounded-xl border border-red-200 bg-red-50 hover:bg-red-100 transition-colors group"
                  >
                    <span className="font-bold text-gray-900">{driver.driver_name}</span>
                    <span className="font-mono font-black text-red-600 group-hover:scale-110 transition-transform">
                      R$ {driver.current_debt.toFixed(2)}
                    </span>
                  </button>
                ))
              )}
            </div>
          </>
        ) : (
          <div className="animate-in slide-in-from-right">
            <div className="bg-gray-50 p-4 rounded-xl border border-gray-200 mb-4">
              <p className="text-xs text-gray-500 font-bold uppercase">Entregador</p>
              <p className="text-lg font-bold text-gray-900">{selectedDriver.driver_name}</p>
              <div className="mt-2 flex justify-between items-center">
                <span className="text-sm text-gray-600">Dívida Total:</span>
                <span className="text-xl font-black text-red-600">R$ {selectedDriver.current_debt.toFixed(2)}</span>
              </div>
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-bold text-gray-700">Valor Recebido (R$)</label>
              <input 
                type="number" 
                className="w-full p-4 text-2xl font-bold text-center border-2 border-gray-300 rounded-xl focus:border-green-500 outline-none"
                value={amount}
                onChange={e => setAmount(e.target.value)}
                autoFocus
              />
            </div>

            <div className="flex gap-2 mt-6">
              <button 
                onClick={() => setSelectedDriver(null)}
                className="flex-1 py-3 rounded-xl font-bold text-gray-600 bg-gray-200 hover:bg-gray-300"
              >
                Voltar
              </button>
              <button 
                onClick={handleSettle}
                disabled={processing}
                className="flex-[2] py-3 rounded-xl font-bold text-white bg-green-600 hover:bg-green-700 flex items-center justify-center gap-2 shadow-lg disabled:opacity-70"
              >
                {processing ? <Loader2 className="animate-spin" /> : <DollarSign />}
                Confirmar Baixa
              </button>
            </div>
          </div>
        )}
      </div>
    </Modal>
  );
}
