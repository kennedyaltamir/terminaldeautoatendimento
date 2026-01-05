"use client";

import { useEffect, useState } from "react";
import { useForm, FieldErrors } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { getCompanySettings, updateCompanySettings } from "@/lib/api";
import { settingsSchema, SettingsSchema } from "@/lib/validations/settings";
import { 
  Save, Loader2, Store, Smartphone, CreditCard, Image as ImageIcon, 
  Trash2, AlertTriangle, Zap, Bug, Bike, Clock, Wifi, Palette, 
  Search, Plus // <--- Adicionados aqui
} from "lucide-react";
import { toast, Toaster } from "sonner";
import AuthInput from "@/components/ui/AuthInput";
import ColorPicker from "@/components/ui/ColorPicker";
import ImageUpload from "@/components/ui/ImageUpload";
import BillingSection from "./BillingSection";

export default function SettingsPage() {
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"general" | "marketing" | "finance" | "billing">("general");
  const [companyData, setCompanyData] = useState<any>(null);

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    reset,
    formState: { errors, isSubmitting, isDirty },
  } = useForm<SettingsSchema>({
    resolver: zodResolver(settingsSchema),
    defaultValues: {
      primary_color: "#ea580c",
      background_color: "#f9fafb",
      text_color: "#111827",
      accent_color: "#ea580c",
      loyalty_percentage: 0,
      fixed_delivery_fee: 0,
      name: "",
      logo_url: "",
      banner_url: "",
      opens_at: "",
      closes_at: "",
      instagram_url: "",
      whatsapp_number: "",
      wifi_ssid: "",
      wifi_password: "",
      pix_key: "",
      mp_access_token: ""
    }
  });

  // Watch com fallback seguro
  const watchedColor = watch("primary_color") || "#ea580c";
  const watchedBg = watch("background_color") || "#f9fafb";
  const watchedText = watch("text_color") || "#111827";
  const watchedName = watch("name");
  const watchedLogo = watch("logo_url");
  const watchedBanner = watch("banner_url");

  useEffect(() => {
    getCompanySettings()
      .then((data) => {
        setCompanyData(data);
        // Preenche o formulário com os dados vindos da API
        reset({
          name: data.name,
          logo_url: data.logo_url || "",
          banner_url: data.banner_url || "",
          primary_color: data.primary_color || "#ea580c",
          background_color: data.background_color || "#f9fafb",
          text_color: data.text_color || "#111827",
          accent_color: data.accent_color || "#ea580c",
          opens_at: data.opens_at ? data.opens_at.slice(0, 5) : "",
          closes_at: data.closes_at ? data.closes_at.slice(0, 5) : "",
          pix_key: data.pix_key || "",
          mp_access_token: data.mp_access_token || "",
          loyalty_percentage: Number(data.loyalty_percentage) || 0,
          fixed_delivery_fee: Number(data.fixed_delivery_fee) || 0,
          instagram_url: data.instagram_url || "",
          whatsapp_number: data.whatsapp_number || "",
          wifi_ssid: data.wifi_ssid || "",
          wifi_password: data.wifi_password || "",
        });
      })
      .catch(() => toast.error("Erro ao carregar configurações"))
      .finally(() => setLoading(false));
  }, [reset]);

  const onSubmit = async (data: SettingsSchema) => {
    try {
      // Limpeza de dados antes de enviar
      const payload = Object.fromEntries(
        Object.entries(data).map(([k, v]) => {
          // Converte strings vazias para null para limpar no banco
          if (v === "") return [k, null];
          // Garante que números sejam números
          if (k === 'loyalty_percentage' || k === 'fixed_delivery_fee') return [k, Number(v)];
          return [k, v];
        })
      );

      await updateCompanySettings(payload);
      toast.success("Configurações salvas com sucesso!");
      
      // Atualiza o estado "pristine" do formulário com os novos dados
      reset(data); 
    } catch (error: any) {
      console.error(error);
      toast.error(error.message || "Erro ao salvar alterações");
    }
  };

  // Função para capturar erros de validação e mostrar ao usuário
  const onInvalid = (errors: FieldErrors<SettingsSchema>) => {
    console.log("Erros de validação:", errors);
    const firstError = Object.values(errors)[0];
    if (firstError) {
      toast.error(`Erro no campo: ${firstError.message}`);
    } else {
      toast.error("Verifique os campos obrigatórios.");
    }
  };

  if (loading) return <div className="text-center py-20 text-gray-500">Carregando...</div>;

  const tabs = [
    { id: "general", label: "Geral & Marca", icon: Store, desc: "Identidade visual e horários" },
    { id: "marketing", label: "Marketing & Wi-Fi", icon: Smartphone, desc: "Redes sociais e conexão" },
    { id: "finance", label: "Financeiro & Delivery", icon: CreditCard, desc: "Pagamentos e taxas" },
    { id: "billing", label: "Plano & Assinatura", icon: Zap, desc: "Gerenciar sua conta" }
  ];

  return (
    <div className="max-w-7xl mx-auto pb-20">
      <Toaster position="top-right" richColors />
      
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white">Configurações</h1>
          <p className="text-gray-400 text-sm mt-1">Personalize sua loja e gerencie sua operação.</p>
        </div>
        {activeTab !== "billing" && (
          <button 
            onClick={handleSubmit(onSubmit, onInvalid)} 
            disabled={isSubmitting || !isDirty} 
            className="bg-orange-600 hover:bg-orange-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-2.5 px-6 rounded-xl flex items-center gap-2 transition-all shadow-lg shadow-orange-900/20"
          >
            {isSubmitting ? <Loader2 className="animate-spin" size={20} /> : <Save size={20} />}
            {isDirty ? "Salvar Alterações" : "Salvo"}
          </button>
        )}
      </div>

      <div className="flex flex-col lg:flex-row gap-8">
        {/* SIDEBAR DE NAVEGAÇÃO */}
        <div className="lg:w-64 shrink-0 space-y-2">
          {tabs.map((tab) => (
            <button 
              key={tab.id} 
              type="button"
              onClick={() => setActiveTab(tab.id as any)} 
              className={`w-full text-left p-4 rounded-xl transition-all flex items-center gap-3 group ${
                activeTab === tab.id 
                  ? "bg-orange-600 text-white shadow-lg shadow-orange-900/20" 
                  : "bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white"
              }`}
            >
              <div className={`p-2 rounded-lg ${activeTab === tab.id ? "bg-white/20" : "bg-gray-900 group-hover:bg-gray-800"}`}>
                <tab.icon size={18} />
              </div>
              <div>
                <span className="block font-bold text-sm">{tab.label}</span>
                <span className={`text-[10px] ${activeTab === tab.id ? "text-orange-100" : "text-gray-500"}`}>{tab.desc}</span>
              </div>
            </button>
          ))}
        </div>

        {/* CONTEÚDO PRINCIPAL */}
        <div className="flex-1 min-w-0">
          {activeTab === "billing" ? (
            <div className="animate-in fade-in slide-in-from-bottom-4">
              <BillingSection company={companyData} />
            </div>
          ) : (
            <form className="space-y-6" onSubmit={handleSubmit(onSubmit, onInvalid)}>
              <div className="bg-gray-800 rounded-xl border border-gray-700 p-6 shadow-xl animate-in fade-in">
                
                {activeTab === "general" && (
                  <div className="space-y-8">
                    <div>
                      <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2"><Store size={20} className="text-orange-500"/> Dados Básicos</h3>
                      <div className="grid gap-6">
                        <AuthInput label="Nome do Restaurante" icon={Store} placeholder="Ex: Burger King" error={errors.name?.message} {...register("name")} />
                        <div className="grid grid-cols-2 gap-4">
                          <AuthInput label="Abre às" type="time" icon={Clock} {...register("opens_at")} />
                          <AuthInput label="Fecha às" type="time" icon={Clock} {...register("closes_at")} />
                        </div>
                      </div>
                    </div>

                    <div className="border-t border-gray-700 pt-8">
                      <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2"><ImageIcon size={20} className="text-orange-500"/> Identidade Visual</h3>
                      <div className="space-y-6">
                        <ImageUpload 
                          label="Logo da Marca" 
                          value={watchedLogo} 
                          onChange={(url) => setValue("logo_url", url, { shouldDirty: true })} 
                        />
                        <ImageUpload 
                          label="Banner de Capa" 
                          value={watchedBanner} 
                          onChange={(url) => setValue("banner_url", url, { shouldDirty: true })} 
                        />
                      </div>
                    </div>

                    <div className="border-t border-gray-700 pt-8">
                      <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2"><Palette size={20} className="text-orange-500"/> Personalização de Cores</h3>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <ColorPicker 
                          label="Cor Principal" 
                          value={watchedColor} 
                          onChange={(color) => setValue("primary_color", color, { shouldDirty: true })} 
                          error={errors.primary_color?.message} 
                        />
                        <ColorPicker 
                          label="Cor de Fundo" 
                          value={watchedBg} 
                          onChange={(color) => setValue("background_color", color, { shouldDirty: true })} 
                        />
                        <ColorPicker 
                          label="Cor do Texto" 
                          value={watchedText} 
                          onChange={(color) => setValue("text_color", color, { shouldDirty: true })} 
                        />
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === "marketing" && (
                  <div className="space-y-8">
                    <div>
                      <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2"><Smartphone size={20} className="text-blue-500"/> Redes Sociais</h3>
                      <div className="space-y-6">
                        <AuthInput label="Instagram URL" icon={Smartphone} placeholder="https://instagram.com/..." error={errors.instagram_url?.message} {...register("instagram_url")} />
                        <AuthInput label="WhatsApp (Apenas números)" icon={Smartphone} placeholder="5511999999999" error={errors.whatsapp_number?.message} {...register("whatsapp_number")} />
                      </div>
                    </div>

                    <div className="border-t border-gray-700 pt-8">
                      <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2"><Wifi size={20} className="text-blue-500"/> Wi-Fi para Clientes</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <AuthInput label="Nome da Rede (SSID)" icon={Wifi} {...register("wifi_ssid")} />
                        <AuthInput label="Senha do Wi-Fi" icon={Wifi} {...register("wifi_password")} />
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === "finance" && (
                  <div className="space-y-8">
                    <div>
                      <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2"><CreditCard size={20} className="text-green-500"/> Taxas & Fidelidade</h3>
                      <div className="grid md:grid-cols-2 gap-6">
                        <div className="bg-purple-900/20 border border-purple-500/30 p-4 rounded-xl">
                            <h3 className="text-white font-bold mb-2">Cashback</h3>
                            <p className="text-xs text-gray-400 mb-4">Porcentagem do pedido que volta como crédito.</p>
                            <div className="flex items-center gap-2">
                                <input type="number" className="w-24 bg-gray-900 border border-gray-700 rounded-lg p-2 text-white outline-none focus:ring-2 focus:ring-purple-500" {...register("loyalty_percentage")} />
                                <span className="text-gray-400 font-bold">%</span>
                            </div>
                        </div>
                        <div className="bg-blue-900/20 border border-blue-500/30 p-4 rounded-xl">
                            <h3 className="text-white font-bold mb-2 flex items-center gap-2"><Bike size={18}/> Taxa de Entrega</h3>
                            <p className="text-xs text-gray-400 mb-4">Valor fixo cobrado em pedidos de delivery.</p>
                            <div className="flex items-center gap-2">
                                <span className="text-gray-400 font-bold">R$</span>
                                <input type="number" step="0.01" className="w-24 bg-gray-900 border border-gray-700 rounded-lg p-2 text-white outline-none focus:ring-2 focus:ring-blue-500" {...register("fixed_delivery_fee")} />
                            </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="border-t border-gray-700 pt-8">
                      <h3 className="text-lg font-bold text-white mb-4">Integrações de Pagamento</h3>
                      <div className="space-y-4">
                        <AuthInput label="Chave Pix (Manual)" icon={CreditCard} placeholder="CPF/CNPJ/Email" {...register("pix_key")} />
                        <AuthInput label="Token Mercado Pago (Produção)" type="password" icon={CreditCard} placeholder="APP_USR-..." {...register("mp_access_token")} />
                      </div>
                    </div>
                  </div>
                )}

                <div className="pt-6 border-t border-gray-700 flex justify-end">
                  <button 
                    type="submit"
                    disabled={isSubmitting || !isDirty} 
                    className="bg-orange-600 hover:bg-orange-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-3 px-8 rounded-xl flex items-center gap-2 transition-all shadow-lg shadow-orange-900/20"
                  >
                    {isSubmitting ? <Loader2 className="animate-spin" size={20} /> : <Save size={20} />}
                    {isDirty ? "Salvar Alterações" : "Salvo"}
                  </button>
                </div>
              </div>
            </form>
          )}

          {/* Preview Section */}
          <div className="hidden lg:block lg:col-span-1">
            <div className="sticky top-24">
              <h3 className="text-gray-400 text-xs font-bold uppercase tracking-wider mb-4 text-center">Preview do Cliente</h3>
              <div className="bg-white rounded-[2rem] border-8 border-gray-800 overflow-hidden shadow-2xl relative h-[600px] flex flex-col mx-auto w-[320px]" style={{ backgroundColor: watchedBg }}>
                
                {/* Header */}
                <div className="sticky top-0 z-30 bg-white/95 backdrop-blur-sm shadow-sm">
                  <div className="p-4 flex justify-between items-center border-b border-gray-100">
                    <div className="flex items-center gap-2">
                      {watchedLogo ? <img src={watchedLogo} className="w-8 h-8 object-contain rounded-lg" alt="Logo" /> : <div className="w-8 h-8 bg-gray-200 rounded-lg"></div>}
                      <h1 className="font-bold text-sm truncate max-w-[150px]" style={{ color: watchedText }}>{watchedName || "Nome do Restaurante"}</h1>
                    </div>
                  </div>

                  {/* Search Bar Fake */}
                  <div className="px-4 pt-4 pb-2">
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <Search className="h-4 w-4 text-gray-400" />
                      </div>
                      <div className="block w-full pl-9 pr-4 py-2 border border-gray-200 rounded-xl bg-white text-xs text-gray-400 shadow-sm">
                        Buscar no cardápio...
                      </div>
                    </div>
                  </div>

                  {/* Category Nav Fake */}
                  <div className="flex overflow-x-auto no-scrollbar py-2 px-4 gap-2">
                    <div className="whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-bold text-white shadow-md" style={{ backgroundColor: watchedColor }}>Lanches</div>
                    <div className="whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-bold bg-gray-100 text-gray-500">Bebidas</div>
                  </div>
                </div>

                {/* Banner */}
                {watchedBanner && (
                  <div className="w-full h-32 relative shrink-0">
                    <img src={watchedBanner} className="w-full h-full object-cover" alt="Banner" />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                  </div>
                )}

                {/* Content */}
                <div className="p-4 flex-1 overflow-hidden space-y-4">
                  <div>
                    <h2 className="text-sm font-bold mb-2 flex items-center gap-2" style={{ color: watchedText }}>
                      <div className="w-1 h-4 rounded-full" style={{ backgroundColor: watchedColor }}></div>
                      Lanches
                    </h2>
                    <div className="space-y-3">
                      {[1, 2].map(i => (
                        <div key={i} className="bg-white p-3 rounded-xl shadow-sm flex justify-between items-center border border-gray-100">
                          <div className="flex-1 pr-2">
                            <h3 className="font-bold text-gray-900 text-xs">X-Bacon</h3>
                            <p className="text-[10px] text-gray-500 line-clamp-2 mt-0.5">Pão, carne, queijo e bacon crocante.</p>
                            <p className="font-bold text-xs mt-1" style={{ color: watchedColor }}>R$ 28,90</p>
                          </div>
                          <div className="flex flex-col items-center gap-1">
                            <div className="w-14 h-14 bg-gray-200 rounded-lg"></div>
                            <div className="w-6 h-6 rounded-full flex items-center justify-center text-white shadow-sm" style={{ backgroundColor: watchedColor }}>
                              <Plus size={12} />
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}