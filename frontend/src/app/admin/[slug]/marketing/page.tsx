"use client";

import { useState, useEffect } from "react";
import { Megaphone, BrainCircuit, Sparkles, Loader2, Wallet, MessageSquare } from "lucide-react";
import { generateRecommendations, getCompanySettings, updateCompanySettings } from "@/lib/api";
import { toast, Toaster } from "sonner";

export default function MarketingPage() {
  const [loading, setLoading] = useState(false);
  const [loyalty, setLoyalty] = useState(0);
  const [settingsLoading, setSettingsLoading] = useState(true);

  useEffect(() => {
    getCompanySettings()
      .then(data => setLoyalty(Number(data.loyalty_percentage) || 0))
      .finally(() => setSettingsLoading(false));
  }, []);

  const handleTrainAI = async () => {
    setLoading(true);
    try {
      await generateRecommendations();
      toast.success("IA iniciada! As recomendações aparecerão em breve.");
    } catch (e) {
      toast.error("Erro ao iniciar treinamento da IA.");
    } finally {
      setLoading(false);
    }
  };

  const handleSaveLoyalty = async () => {
    try {
      await updateCompanySettings({ loyalty_percentage: loyalty });
      toast.success("Configuração de fidelidade salva!");
    } catch (e) {
      toast.error("Erro ao salvar.");
    }
  };

  return (
    <div className="space-y-8 pb-20 animate-in fade-in">
      <Toaster position="top-right" richColors />
      
      <div className="flex items-center gap-3">
        <div className="bg-pink-600 p-3 rounded-xl shadow-lg shadow-pink-500/20">
          <Megaphone size={24} className="text-white" />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-white">Marketing & Inteligência</h1>
          <p className="text-gray-400 text-sm">Ferramentas para vender mais e fidelizar clientes.</p>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        
        {/* CARD IA */}
        <div className="bg-gray-800 border border-gray-700 rounded-2xl p-6 shadow-xl relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-purple-600/10 rounded-full blur-2xl -mr-10 -mt-10"></div>
          
          <div className="flex items-start justify-between mb-6 relative z-10">
            <div>
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <BrainCircuit className="text-purple-500" /> Motor de Upselling (IA)
              </h3>
              <p className="text-gray-400 text-sm mt-2 leading-relaxed">
                Nossa IA analisa o histórico de vendas para descobrir padrões como "Quem pede Hambúrguer também pede Batata".
                Isso gera sugestões automáticas no carrinho.
              </p>
            </div>
          </div>

          <div className="bg-gray-900/50 p-4 rounded-xl border border-gray-700 mb-6">
            <div className="flex items-center gap-3 text-sm text-gray-300">
              <Sparkles size={16} className="text-yellow-400" />
              <span>Último Treinamento: <b>Hoje, 10:00</b></span>
            </div>
          </div>

          <button 
            onClick={handleTrainAI}
            disabled={loading}
            className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 rounded-xl flex items-center justify-center gap-2 transition-all shadow-lg shadow-purple-900/20 disabled:opacity-70"
          >
            {loading ? <Loader2 className="animate-spin" /> : <BrainCircuit size={20} />}
            Treinar IA Agora
          </button>
        </div>

        {/* CARD FIDELIDADE */}
        <div className="bg-gray-800 border border-gray-700 rounded-2xl p-6 shadow-xl">
          <div className="flex items-start justify-between mb-6">
            <div>
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <Wallet className="text-green-500" /> Programa de Fidelidade
              </h3>
              <p className="text-gray-400 text-sm mt-2">
                Defina a porcentagem do valor do pedido que volta como crédito (Cashback) para o cliente.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4 mb-6">
            <div className="flex-1">
              <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Porcentagem de Cashback</label>
              <div className="flex items-center gap-2">
                <input 
                  type="number" 
                  min="0" 
                  max="100"
                  className="w-full bg-gray-900 border border-gray-600 rounded-xl p-3 text-white font-bold text-lg focus:ring-2 focus:ring-green-500 outline-none"
                  value={loyalty}
                  onChange={e => setLoyalty(Number(e.target.value))}
                />
                <span className="text-gray-400 font-bold text-xl">%</span>
              </div>
            </div>
            <div className="flex-1 bg-green-900/20 border border-green-800 p-3 rounded-xl">
              <p className="text-xs text-green-300">
                Exemplo: Em um pedido de <b>R$ 100,00</b>, o cliente ganha <b>R$ {loyalty.toFixed(2)}</b> de crédito.
              </p>
            </div>
          </div>

          <button 
            onClick={handleSaveLoyalty}
            className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 rounded-xl transition-all shadow-lg shadow-green-900/20"
          >
            Salvar Configuração
          </button>
        </div>

        {/* CARD WHATSAPP (Atalho) */}
        <div className="md:col-span-2 bg-gray-800 border border-gray-700 rounded-2xl p-6 shadow-xl flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="bg-green-500/20 p-3 rounded-full text-green-500">
              <MessageSquare size={24} />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">Automação de WhatsApp</h3>
              <p className="text-gray-400 text-sm">Configure as mensagens automáticas de status.</p>
            </div>
          </div>
          <a href="settings" className="bg-gray-700 hover:bg-gray-600 text-white px-6 py-2 rounded-lg font-bold text-sm transition-colors">
            Configurar
          </a>
        </div>

      </div>
    </div>
  );
}
