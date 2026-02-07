"use client";

import { useState } from "react";
import { CreditCard, CheckCircle2, X, ExternalLink, Loader2 } from "lucide-react";
import { toast } from "sonner";
import { Company } from "@/types";
import { getPaymentAuthUrl, disconnectPaymentProvider } from "@/lib/api";

export default function FinanceSection({ company }: { company: Company }) {
  const [loading, setLoading] = useState(false);

  const handleConnectMP = async () => {
    setLoading(true);
    try {
      const data = await getPaymentAuthUrl("mercadopago");
      if (data.url) window.location.href = data.url;
    } catch (e) {
      toast.error("Erro ao iniciar conexão");
    } finally {
      setLoading(false);
    }
  };

  const handleDisconnect = async () => {
    if (!confirm("Desconectar pagamentos?")) return;
    try {
      await disconnectPaymentProvider();
      window.location.reload();
    } catch (e) {
      toast.error("Erro ao desconectar");
    }
  };

  const isConnected = company.payment_provider === 'mercadopago';

  return (
    <div className="space-y-6 animate-in fade-in">
      <div className="bg-gray-800 border border-gray-700 rounded-xl p-6">
        <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <CreditCard className="text-blue-500" /> Provedor de Pagamento
        </h3>
        
        <div className="bg-gray-900 p-4 rounded-lg border border-gray-700 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <img src="https://logopng.com.br/logos/mercado-pago-205.png" className="w-12 h-12 object-contain bg-white rounded-lg p-1" alt="Mercado Pago" />
            <div>
              <p className="font-bold text-white">Mercado Pago</p>
              <p className="text-xs text-gray-400">Pix Automático e Cartão</p>
            </div>
          </div>

          {isConnected ? (
            <div className="flex items-center gap-4">
              <span className="text-green-500 text-xs font-bold flex items-center gap-1 bg-green-900/20 px-3 py-1 rounded-full">
                <CheckCircle2 size={14} /> Conectado
              </span>
              <button onClick={handleDisconnect} className="text-red-400 hover:text-red-300 p-2">
                <X size={20} />
              </button>
            </div>
          ) : (
            <button 
              onClick={handleConnectMP}
              disabled={loading}
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-bold transition-colors flex items-center gap-2"
            >
              {loading ? <Loader2 className="animate-spin" size={16} /> : "Conectar"}
            </button>
          )}
        </div>

        <div className="mt-6 pt-6 border-t border-gray-700">
          <h4 className="text-sm font-bold text-gray-400 uppercase mb-3">Outras Opções (Em Breve)</h4>
          <div className="grid grid-cols-2 gap-4 opacity-50">
            <div className="border border-gray-700 p-3 rounded-lg flex items-center gap-3">
              <div className="w-8 h-8 bg-orange-500 rounded-full"></div>
              <span className="text-sm font-bold text-gray-500">Efi (Gerencianet)</span>
            </div>
            <div className="border border-gray-700 p-3 rounded-lg flex items-center gap-3">
              <div className="w-8 h-8 bg-green-600 rounded-full"></div>
              <span className="text-sm font-bold text-gray-500">Pagar.me</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}