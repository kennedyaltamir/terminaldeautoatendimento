"use client";

import { useState, useEffect } from "react";
import { Megaphone, BrainCircuit, Sparkles, Loader2, Wallet, MessageSquare, Tag, Plus, Trash2, Check, X } from "lucide-react";
import { generateRecommendations, getCompanySettings, updateCompanySettings, getPromotions, createPromotion, updatePromotion, deletePromotion } from "@/lib/api";
import { toast, Toaster } from "sonner";
import { Promotion } from "@/types";
import Modal from "@/components/ui/Modal";

export default function MarketingPage() {
  const [loading, setLoading] = useState(false);
  const [loyalty, setLoyalty] = useState(0);
  const [promotions, setPromotions] = useState<Promotion[]>([]);
  const [isPromoModalOpen, setIsPromoModalOpen] = useState(false);

  // Form State para Promoção
  const [promoForm, setPromoForm] = useState({
    name: "",
    code: "",
    discount_type: "percentage",
    discount_value: "",
    min_order_value: "0",
    usage_limit: ""
  });

  useEffect(() => {
    getCompanySettings()
      .then(data => setLoyalty(Number(data.loyalty_percentage) || 0));

    fetchPromotions();
  }, []);

  const fetchPromotions = async () => {
    try {
      const data = await getPromotions();
      setPromotions(data);
    } catch (e) {
      console.error(e);
    }
  };

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

  const handleCreatePromo = async () => {
    if (!promoForm.name || !promoForm.discount_value) return toast.error("Preencha os campos obrigatórios");

    try {
      await createPromotion({
        ...promoForm,
        discount_value: parseFloat(promoForm.discount_value),
        min_order_value: parseFloat(promoForm.min_order_value),
        usage_limit: promoForm.usage_limit ? parseInt(promoForm.usage_limit) : null,
        code: promoForm.code || null // Envia null se vazio para regra automática (futuro)
      });
      toast.success("Promoção criada!");
      setIsPromoModalOpen(false);
      setPromoForm({ name: "", code: "", discount_type: "percentage", discount_value: "", min_order_value: "0", usage_limit: "" });
      fetchPromotions();
    } catch (e: any) {
      toast.error(e.message || "Erro ao criar promoção");
    }
  };

  const togglePromoStatus = async (promo: Promotion) => {
    try {
      await updatePromotion(promo.id, { is_active: !promo.is_active });
      fetchPromotions();
      toast.success(`Promoção ${!promo.is_active ? 'ativada' : 'pausada'}`);
    } catch (e) {
      toast.error("Erro ao atualizar status");
    }
  };

  const handleDeletePromo = async (id: string) => {
    if (!confirm("Excluir esta promoção?")) return;
    try {
      await deletePromotion(id);
      fetchPromotions();
      toast.success("Promoção removida");
    } catch (e) {
      toast.error("Erro ao remover");
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

        {/* CARD CUPONS & PROMOÇÕES */}
        <div className="md:col-span-2 bg-gray-800 border border-gray-700 rounded-2xl p-6 shadow-xl">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <Tag className="text-orange-500" /> Cupons & Promoções
              </h3>
              <p className="text-gray-400 text-sm mt-1">Crie códigos de desconto para atrair clientes.</p>
            </div>
            <button 
              onClick={() => setIsPromoModalOpen(true)}
              className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-xl font-bold flex items-center gap-2 text-sm transition-colors"
            >
              <Plus size={18} /> Novo Cupom
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-gray-300">
              <thead className="bg-gray-900 text-xs uppercase font-bold text-gray-500">
                <tr>
                  <th className="px-4 py-3 rounded-tl-lg">Nome</th>
                  <th className="px-4 py-3">Código</th>
                  <th className="px-4 py-3">Desconto</th>
                  <th className="px-4 py-3">Mínimo</th>
                  <th className="px-4 py-3">Uso</th>
                  <th className="px-4 py-3">Status</th>
                  <th className="px-4 py-3 rounded-tr-lg text-right">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-700">
                {promotions.length === 0 ? (
                  <tr><td colSpan={7} className="text-center py-8 text-gray-500">Nenhuma promoção ativa.</td></tr>
                ) : (
                  promotions.map(promo => (
                    <tr key={promo.id} className="hover:bg-gray-700/30 transition-colors">
                      <td className="px-4 py-3 font-bold text-white">{promo.name}</td>
                      <td className="px-4 py-3">
                        <span className="font-mono bg-gray-900 px-2 py-1 rounded text-xs border border-gray-600 text-orange-400">
                          {promo.code || "AUTOMÁTICO"}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-bold text-green-400">
                        {promo.discount_type === 'percentage' ? `${Number(promo.discount_value)}%` : `R$ ${Number(promo.discount_value).toFixed(2)}`}
                      </td>
                      <td className="px-4 py-3 text-xs">R$ {Number(promo.min_order_value).toFixed(2)}</td>
                      <td className="px-4 py-3 text-xs">
                        {promo.current_usage} {promo.usage_limit ? `/ ${promo.usage_limit}` : ''}
                      </td>
                      <td className="px-4 py-3">
                        <button 
                          onClick={() => togglePromoStatus(promo)}
                          className={`px-2 py-1 rounded text-xs font-bold uppercase border ${promo.is_active ? 'bg-green-900/30 text-green-400 border-green-800' : 'bg-red-900/30 text-red-400 border-red-800'}`}
                        >
                          {promo.is_active ? 'Ativo' : 'Pausado'}
                        </button>
                      </td>
                      <td className="px-4 py-3 text-right">
                        <button onClick={() => handleDeletePromo(promo.id)} className="text-red-400 hover:text-red-300 p-2 hover:bg-red-900/20 rounded-lg transition-colors">
                          <Trash2 size={16} />
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
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

      {/* MODAL DE PROMOÇÃO */}
      <Modal isOpen={isPromoModalOpen} onClose={() => setIsPromoModalOpen(false)} title="Nova Promoção">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-1">Nome da Campanha</label>
            <input 
              className="w-full border rounded-lg p-2 bg-gray-50" 
              placeholder="Ex: Desconto de Verão"
              value={promoForm.name}
              onChange={e => setPromoForm({...promoForm, name: e.target.value})}
            />
          </div>

          <div>
            <label className="block text-sm font-bold text-gray-700 mb-1">Código do Cupom</label>
            <input 
              className="w-full border rounded-lg p-2 bg-gray-50 uppercase font-mono" 
              placeholder="VERAO10"
              value={promoForm.code}
              onChange={e => setPromoForm({...promoForm, code: e.target.value.toUpperCase()})}
            />
            <p className="text-xs text-gray-500 mt-1">Deixe em branco para aplicar automaticamente (Regra).</p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-1">Tipo</label>
              <select 
                className="w-full border rounded-lg p-2 bg-white"
                value={promoForm.discount_type}
                onChange={e => setPromoForm({...promoForm, discount_type: e.target.value})}
              >
                <option value="percentage">Porcentagem (%)</option>
                <option value="fixed">Valor Fixo (R$)</option>
                <option value="shipping">Frete Grátis</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-1">Valor do Desconto</label>
              <input 
                type="number" 
                className="w-full border rounded-lg p-2 bg-gray-50" 
                placeholder="10"
                value={promoForm.discount_value}
                onChange={e => setPromoForm({...promoForm, discount_value: e.target.value})}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-1">Pedido Mínimo (R$)</label>
              <input 
                type="number" 
                className="w-full border rounded-lg p-2 bg-gray-50" 
                value={promoForm.min_order_value}
                onChange={e => setPromoForm({...promoForm, min_order_value: e.target.value})}
              />
            </div>
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-1">Limite de Uso</label>
              <input 
                type="number" 
                className="w-full border rounded-lg p-2 bg-gray-50" 
                placeholder="Ilimitado"
                value={promoForm.usage_limit}
                onChange={e => setPromoForm({...promoForm, usage_limit: e.target.value})}
              />
            </div>
          </div>

          <button 
            onClick={handleCreatePromo}
            className="w-full bg-orange-600 text-white py-3 rounded-xl font-bold hover:bg-orange-700 transition-colors mt-4"
          >
            Criar Promoção
          </button>
        </div>
      </Modal>
    </div>
  );
}
