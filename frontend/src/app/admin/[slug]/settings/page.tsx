"use client";

import { useEffect, useState } from "react";
import { getCompanySettings, updateCompanySettings } from "@/lib/api";
import { Save, Loader2, Clock, QrCode, CreditCard, AlertTriangle, CheckCircle2, Gift, Palette, Store, Smartphone, Wifi, Instagram, Phone, Image as ImageIcon, Trash2 } from "lucide-react";

export default function SettingsPage() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [activeTab, setActiveTab] = useState<"general" | "marketing" | "finance">("general");
  
  const [form, setForm] = useState({
    name: "",
    logo_url: "",
    banner_url: "",
    primary_color: "#ea580c",
    opens_at: "",
    closes_at: "",
    pix_key: "",
    mp_access_token: "",
    loyalty_percentage: 0,
    instagram_url: "",
    whatsapp_number: "",
    wifi_ssid: "",
    wifi_password: "",
  });

  useEffect(() => {
    getCompanySettings()
      .then((data) => {
        setForm({
          name: data.name,
          logo_url: data.logo_url || "",
          banner_url: data.banner_url || "",
          primary_color: data.primary_color || "#ea580c",
          opens_at: data.opens_at ? data.opens_at.slice(0, 5) : "",
          closes_at: data.closes_at ? data.closes_at.slice(0, 5) : "",
          pix_key: data.pix_key || "",
          mp_access_token: data.mp_access_token || "",
          loyalty_percentage: Number(data.loyalty_percentage) || 0,
          instagram_url: data.instagram_url || "",
          whatsapp_number: data.whatsapp_number || "",
          wifi_ssid: data.wifi_ssid || "",
          wifi_password: data.wifi_password || "",
        });
      })
      .catch(() => alert("Erro ao carregar configurações"))
      .finally(() => setLoading(false));
  }, []);

  const handleSave = async () => {
    setSaving(true);
    try {
      const payload: any = {
        ...form,
        opens_at: form.opens_at || null,
        closes_at: form.closes_at || null,
        logo_url: form.logo_url || null,
        banner_url: form.banner_url || null,
        pix_key: form.pix_key || null,
        mp_access_token: form.mp_access_token || "",
        instagram_url: form.instagram_url || null,
        whatsapp_number: form.whatsapp_number || null,
        wifi_ssid: form.wifi_ssid || null,
        wifi_password: form.wifi_password || null,
      };

      await updateCompanySettings(payload);
      alert("Configurações salvas com sucesso!");
    } catch (error: any) {
      console.error(error);
      alert("Erro ao salvar: " + (error.message || "Verifique os dados."));
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="text-center py-20 text-gray-500">Carregando configurações...</div>;

  const isMpConnected = form.mp_access_token && form.mp_access_token.startsWith("APP_USR-");

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-20">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Configurações da Loja</h1>
          <p className="text-gray-400 text-sm mt-1">Personalize sua marca e dados financeiros.</p>
        </div>
        <button 
          onClick={handleSave}
          disabled={saving}
          className="bg-orange-600 hover:bg-orange-700 text-white font-bold py-2.5 px-6 rounded-xl flex items-center gap-2 transition-all disabled:opacity-50 shadow-lg shadow-orange-900/20"
        >
          {saving ? <Loader2 className="animate-spin" size={20} /> : <Save size={20} />}
          Salvar Alterações
        </button>
      </div>

      <div className="flex border-b border-gray-700 overflow-x-auto">
        <button 
          onClick={() => setActiveTab("general")}
          className={`px-6 py-3 font-medium text-sm transition-colors border-b-2 flex items-center gap-2 whitespace-nowrap ${activeTab === "general" ? "border-orange-500 text-orange-500" : "border-transparent text-gray-400 hover:text-white"}`}
        >
          <Store size={16} /> Geral & Marca
        </button>
        <button 
          onClick={() => setActiveTab("marketing")}
          className={`px-6 py-3 font-medium text-sm transition-colors border-b-2 flex items-center gap-2 whitespace-nowrap ${activeTab === "marketing" ? "border-orange-500 text-orange-500" : "border-transparent text-gray-400 hover:text-white"}`}
        >
          <Smartphone size={16} /> Marketing & Wi-Fi
        </button>
        <button 
          onClick={() => setActiveTab("finance")}
          className={`px-6 py-3 font-medium text-sm transition-colors border-b-2 flex items-center gap-2 whitespace-nowrap ${activeTab === "finance" ? "border-orange-500 text-orange-500" : "border-transparent text-gray-400 hover:text-white"}`}
        >
          <CreditCard size={16} /> Financeiro
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* COLUNA ESQUERDA: FORMULÁRIO */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-gray-800 rounded-xl border border-gray-700 p-6 shadow-xl">
            
            {activeTab === "general" && (
              <div className="space-y-6">
                <div>
                  <label className="block text-xs font-bold text-gray-500 uppercase mb-2 tracking-wider">Nome do Restaurante</label>
                  <input 
                    type="text" 
                    className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none transition-all"
                    value={form.name}
                    onChange={(e) => setForm({...form, name: e.target.value})}
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-gray-500 uppercase mb-2 tracking-wider flex items-center gap-2">
                      <Clock size={14} /> Abre às
                    </label>
                    <input 
                      type="time" 
                      className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none transition-all"
                      value={form.opens_at}
                      onChange={(e) => setForm({...form, opens_at: e.target.value})}
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-gray-500 uppercase mb-2 tracking-wider flex items-center gap-2">
                      <Clock size={14} /> Fecha às
                    </label>
                    <input 
                      type="time" 
                      className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none transition-all"
                      value={form.closes_at}
                      onChange={(e) => setForm({...form, closes_at: e.target.value})}
                    />
                  </div>
                </div>

                <div className="border-t border-gray-700 pt-6">
                  <h3 className="text-white font-bold mb-4 flex items-center gap-2"><Palette size={18} className="text-orange-500"/> Identidade Visual</h3>
                  
                  <div className="mb-4">
                    <label className="block text-xs font-bold text-gray-500 uppercase mb-2 tracking-wider">URL do Logo</label>
                    <input 
                      type="text" 
                      className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none transition-all text-sm"
                      placeholder="https://..."
                      value={form.logo_url}
                      onChange={(e) => setForm({...form, logo_url: e.target.value})}
                    />
                    <p className="text-xs text-gray-500 mt-1">Recomendado: Imagem quadrada (PNG/JPG), fundo transparente.</p>
                  </div>

                  <div className="mb-4">
                    <label className="block text-xs font-bold text-gray-500 uppercase mb-2 tracking-wider">URL do Banner (Capa)</label>
                    <input 
                      type="text" 
                      className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none transition-all text-sm"
                      placeholder="https://..."
                      value={form.banner_url}
                      onChange={(e) => setForm({...form, banner_url: e.target.value})}
                    />
                    <p className="text-xs text-gray-500 mt-1">Recomendado: Imagem horizontal (1200x400).</p>
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-gray-500 uppercase mb-2 tracking-wider">Cor Principal</label>
                    <div className="flex gap-4 items-center">
                      <div className="relative">
                        <input 
                          type="color" 
                          className="h-12 w-12 rounded-lg cursor-pointer bg-transparent border-0 p-0 overflow-hidden"
                          value={form.primary_color}
                          onChange={(e) => setForm({...form, primary_color: e.target.value})}
                        />
                        <div className="absolute inset-0 rounded-lg border border-gray-600 pointer-events-none"></div>
                      </div>
                      <input 
                        type="text" 
                        className="flex-1 bg-gray-900 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none uppercase font-mono"
                        value={form.primary_color}
                        onChange={(e) => setForm({...form, primary_color: e.target.value})}
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === "marketing" && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-white font-bold mb-4 flex items-center gap-2"><Smartphone size={18} className="text-blue-500"/> Redes Sociais</h3>
                  <div className="grid gap-4">
                    <div>
                      <label className="block text-xs font-bold text-gray-500 uppercase mb-2 tracking-wider flex items-center gap-2"><Instagram size={14}/> Instagram URL</label>
                      <input 
                        type="text" 
                        className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                        placeholder="https://instagram.com/seu_restaurante"
                        value={form.instagram_url}
                        onChange={(e) => setForm({...form, instagram_url: e.target.value})}
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-bold text-gray-500 uppercase mb-2 tracking-wider flex items-center gap-2"><Phone size={14}/> WhatsApp (Apenas números)</label>
                      <input 
                        type="text" 
                        className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-green-500 outline-none transition-all"
                        placeholder="5511999999999"
                        value={form.whatsapp_number}
                        onChange={(e) => setForm({...form, whatsapp_number: e.target.value})}
                      />
                    </div>
                  </div>
                </div>

                <div className="border-t border-gray-700 pt-6">
                  <h3 className="text-white font-bold mb-4 flex items-center gap-2"><Wifi size={18} className="text-purple-500"/> Wi-Fi para Clientes</h3>
                  <div className="grid gap-4">
                    <div>
                      <label className="block text-xs font-bold text-gray-500 uppercase mb-2 tracking-wider">Nome da Rede (SSID)</label>
                      <input 
                        type="text" 
                        className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-purple-500 outline-none transition-all"
                        placeholder="Wi-Fi Clientes"
                        value={form.wifi_ssid}
                        onChange={(e) => setForm({...form, wifi_ssid: e.target.value})}
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-bold text-gray-500 uppercase mb-2 tracking-wider">Senha</label>
                      <input 
                        type="text" 
                        className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-purple-500 outline-none transition-all"
                        placeholder="senha123"
                        value={form.wifi_password}
                        onChange={(e) => setForm({...form, wifi_password: e.target.value})}
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === "finance" && (
              <div className="space-y-8">
                <div className="p-4 rounded-xl border bg-purple-900/20 border-purple-500/30">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 rounded-lg bg-purple-600 text-white">
                      <Gift size={24} />
                    </div>
                    <div>
                      <h3 className="font-bold text-white">Programa de Fidelidade (Cashback)</h3>
                      <p className="text-xs text-gray-400">Porcentagem do valor do pedido que volta como crédito para o cliente.</p>
                    </div>
                  </div>
                  
                  <label className="block text-xs font-bold text-gray-500 uppercase mb-2 tracking-wider">% de Cashback</label>
                  <div className="flex items-center gap-2">
                    <input 
                      type="number" 
                      className="w-24 bg-gray-900 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-purple-500 outline-none transition-all font-mono"
                      placeholder="0"
                      value={form.loyalty_percentage}
                      onChange={(e) => setForm({...form, loyalty_percentage: parseFloat(e.target.value)})}
                    />
                    <span className="text-gray-400 font-bold">%</span>
                  </div>
                  <p className="text-xs text-gray-500 mt-2">Defina 0 para desativar.</p>
                </div>

                <div className={`p-4 rounded-xl border transition-all ${!isMpConnected ? 'bg-gray-700/30 border-orange-500/50' : 'bg-gray-900/30 border-gray-700 opacity-50'}`}>
                  <div className="flex items-center gap-3 mb-4">
                    <div className={`p-2 rounded-lg ${!isMpConnected ? 'bg-orange-500 text-white' : 'bg-gray-700 text-gray-400'}`}>
                      <QrCode size={24} />
                    </div>
                    <div>
                      <h3 className="font-bold text-white">Pix Manual (Direto)</h3>
                      <p className="text-xs text-gray-400">O dinheiro cai na hora na sua conta. Baixa manual.</p>
                    </div>
                    {!isMpConnected && <span className="ml-auto text-xs bg-orange-500/20 text-orange-400 px-2 py-1 rounded font-bold">ATIVO</span>}
                  </div>
                  
                  <label className="block text-xs font-bold text-gray-500 uppercase mb-2 tracking-wider">Sua Chave Pix</label>
                  <input 
                    type="text" 
                    className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none transition-all font-mono"
                    placeholder="CPF, Email ou Aleatória"
                    value={form.pix_key}
                    onChange={(e) => setForm({...form, pix_key: e.target.value})}
                    disabled={!!isMpConnected}
                  />
                </div>

                <div className={`p-4 rounded-xl border transition-all ${isMpConnected ? 'bg-green-900/20 border-green-500/50' : 'bg-gray-900/30 border-gray-700'}`}>
                  <div className="flex items-center gap-3 mb-4">
                    <div className={`p-2 rounded-lg ${isMpConnected ? 'bg-green-600 text-white' : 'bg-gray-700 text-gray-400'}`}>
                      <CreditCard size={24} />
                    </div>
                    <div>
                      <h3 className="font-bold text-white">Pix Automático (Mercado Pago)</h3>
                      <p className="text-xs text-gray-400">Baixa automática e QR Code dinâmico.</p>
                    </div>
                    {isMpConnected && <span className="ml-auto text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded font-bold flex items-center gap-1"><CheckCircle2 size={12}/> CONECTADO</span>}
                  </div>

                  <label className="block text-xs font-bold text-gray-500 uppercase mb-2 tracking-wider">Access Token (Produção)</label>
                  <input 
                    type="password" 
                    className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-green-500 outline-none transition-all font-mono text-xs"
                    placeholder="APP_USR-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
                    value={form.mp_access_token}
                    onChange={(e) => setForm({...form, mp_access_token: e.target.value})}
                  />
                </div>
              </div>
            )}
          </div>
          
          {/* ZONA DE PERIGO */}
          <div className="bg-red-900/10 border border-red-900/30 rounded-xl p-6">
            <h3 className="text-red-500 font-bold mb-2 flex items-center gap-2"><AlertTriangle size={18}/> Zona de Perigo</h3>
            <p className="text-gray-400 text-sm mb-4">Ações irreversíveis.</p>
            <button className="text-red-400 hover:text-red-300 text-sm font-bold flex items-center gap-2 hover:bg-red-900/20 px-4 py-2 rounded-lg transition-colors">
              <Trash2 size={16} /> Excluir minha conta e dados
            </button>
          </div>
        </div>

        {/* COLUNA DIREITA: PREVIEW */}
        <div className="lg:col-span-1">
          <div className="sticky top-24">
            <h3 className="text-gray-400 text-xs font-bold uppercase tracking-wider mb-4 flex items-center gap-2">
              <Smartphone size={14} /> Preview do Cliente
            </h3>
            
            {/* Mockup de Celular */}
            <div className="bg-white rounded-[2rem] border-8 border-gray-800 overflow-hidden shadow-2xl relative h-[550px] flex flex-col">
              
              {/* Banner */}
              <div className="h-32 bg-gray-200 relative">
                {form.banner_url ? (
                  <img src={form.banner_url} className="w-full h-full object-cover" alt="Banner" />
                ) : (
                  <div className="w-full h-full bg-gray-300 animate-pulse flex items-center justify-center text-gray-400 text-xs">Sem Banner</div>
                )}
                {/* Logo Sobreposto */}
                <div className="absolute -bottom-6 left-4 w-16 h-16 bg-white rounded-xl shadow-md p-1">
                  {form.logo_url ? (
                    <img src={form.logo_url} className="w-full h-full object-contain rounded-lg" alt="Logo" />
                  ) : (
                    <div className="w-full h-full bg-gray-200 rounded-lg animate-pulse"></div>
                  )}
                </div>
              </div>

              {/* Header do App */}
              <div className="bg-white px-4 pt-8 pb-4 shadow-sm border-b border-gray-100">
                <div>
                  <h2 className="font-bold text-gray-900 text-lg leading-tight">{form.name || "Nome do Restaurante"}</h2>
                  <p className="text-xs text-gray-500 mt-1">Aberto • Fecha às {form.closes_at || "23:00"}</p>
                </div>
              </div>

              {/* Corpo do App */}
              <div className="p-4 bg-gray-50 flex-1 overflow-hidden">
                <div className="space-y-3">
                  <div className="h-20 bg-white rounded-lg border border-gray-100 shadow-sm p-3 flex gap-3">
                    <div className="w-14 h-14 bg-gray-200 rounded-md"></div>
                    <div className="flex-1">
                      <div className="h-3 w-24 bg-gray-200 rounded mb-2"></div>
                      <div className="h-3 w-12 bg-gray-200 rounded"></div>
                    </div>
                    <div 
                      className="w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-xs shadow-md"
                      style={{ backgroundColor: form.primary_color }}
                    >
                      +
                    </div>
                  </div>
                </div>
              </div>

              {/* Footer do App (Marketing) */}
              <div className="bg-white border-t border-gray-200 p-3 flex justify-around text-gray-400">
                {form.instagram_url && <Instagram size={20} className="text-pink-600" />}
                {form.whatsapp_number && <Phone size={20} className="text-green-600" />}
                {form.wifi_ssid && <Wifi size={20} className="text-blue-600" />}
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}