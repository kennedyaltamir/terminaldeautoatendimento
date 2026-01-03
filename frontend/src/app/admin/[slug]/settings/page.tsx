"use client";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { getCompanySettings, updateCompanySettings } from "@/lib/api";
import { settingsSchema, SettingsSchema } from "@/lib/validations/settings";
import { Save, Loader2, Store, Smartphone, CreditCard, Image as ImageIcon, Trash2, AlertTriangle, Zap, Bug } from "lucide-react";
import { toast, Toaster } from "sonner";
import AuthInput from "@/components/ui/AuthInput";
import ColorPicker from "@/components/ui/ColorPicker";
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
      loyalty_percentage: 0,
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

  const watchedColor = watch("primary_color");
  const watchedName = watch("name");
  const watchedLogo = watch("logo_url");
  const watchedBanner = watch("banner_url");

  useEffect(() => {
    getCompanySettings()
      .then((data) => {
        setCompanyData(data);
        reset({
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
      .catch(() => toast.error("Erro ao carregar configurações"))
      .finally(() => setLoading(false));
  }, [reset]);

  const onSubmit = async (data: SettingsSchema) => {
    try {
      const payload = Object.fromEntries(
        Object.entries(data).map(([k, v]) => [k, v === "" ? null : v])
      );
      
      await updateCompanySettings(payload);
      toast.success("Configurações salvas com sucesso!");
      reset(data);
    } catch (error: any) {
      toast.error(error.message || "Erro ao salvar alterações");
    }
  };

  if (loading) return <div className="text-center py-20 text-gray-500">Carregando...</div>;

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-20">
      <Toaster position="top-right" richColors />
      
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white">Configurações da Loja</h1>
          <p className="text-gray-400 text-sm mt-1">Gerencie a identidade visual e dados operacionais.</p>
        </div>
        {activeTab !== "billing" && (
          <button 
            onClick={handleSubmit(onSubmit)}
            disabled={isSubmitting || !isDirty}
            className="bg-orange-600 hover:bg-orange-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-2.5 px-6 rounded-xl flex items-center gap-2 transition-all shadow-lg shadow-orange-900/20"
          >
            {isSubmitting ? <Loader2 className="animate-spin" size={20} /> : <Save size={20} />}
            {isDirty ? "Salvar Alterações" : "Salvo"}
          </button>
        )}
      </div>

      <div className="flex border-b border-gray-700 overflow-x-auto no-scrollbar">
        {[
          { id: "general", label: "Geral & Marca", icon: Store },
          { id: "marketing", label: "Marketing & Wi-Fi", icon: Smartphone },
          { id: "finance", label: "Financeiro", icon: CreditCard },
          { id: "billing", label: "Assinatura", icon: Zap },
        ].map((tab) => (
          <button 
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-6 py-3 font-medium text-sm transition-colors border-b-2 flex items-center gap-2 whitespace-nowrap ${
              activeTab === tab.id 
                ? "border-orange-500 text-orange-500" 
                : "border-transparent text-gray-400 hover:text-white"
            }`}
          >
            <tab.icon size={16} /> {tab.label}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          {activeTab === "billing" ? (
            <div className="animate-in fade-in slide-in-from-bottom-4">
              <BillingSection company={companyData} />
            </div>
          ) : (
            <form className="bg-gray-800 rounded-xl border border-gray-700 p-6 shadow-xl space-y-6" onSubmit={handleSubmit(onSubmit)}>
              {activeTab === "general" && (
                <div className="space-y-6 animate-in fade-in">
                  <AuthInput 
                    label="Nome do Restaurante"
                    icon={Store}
                    placeholder="Ex: Burger King"
                    error={errors.name?.message}
                    {...register("name")}
                  />
                  <div className="grid grid-cols-2 gap-4">
                    <AuthInput label="Abre às" type="time" icon={Store} {...register("opens_at")} />
                    <AuthInput label="Fecha às" type="time" icon={Store} {...register("closes_at")} />
                  </div>
                  <div className="border-t border-gray-700 pt-6 space-y-6">
                    <h3 className="text-white font-bold flex items-center gap-2">Identidade Visual</h3>
                    <AuthInput label="URL do Logo" icon={ImageIcon} placeholder="https://..." error={errors.logo_url?.message} {...register("logo_url")} />
                    <AuthInput label="URL do Banner (Capa)" icon={ImageIcon} placeholder="https://..." error={errors.banner_url?.message} {...register("banner_url")} />
                    <ColorPicker label="Cor Principal" value={watchedColor} onChange={(color) => setValue("primary_color", color, { shouldDirty: true })} error={errors.primary_color?.message} />
                  </div>
                </div>
              )}

              {activeTab === "marketing" && (
                <div className="space-y-6 animate-in fade-in">
                  <AuthInput label="Instagram URL" icon={Smartphone} placeholder="https://instagram.com/..." error={errors.instagram_url?.message} {...register("instagram_url")} />
                  <AuthInput label="WhatsApp (Apenas números)" icon={Smartphone} placeholder="5511999999999" error={errors.whatsapp_number?.message} {...register("whatsapp_number")} />
                  <div className="border-t border-gray-700 pt-6 space-y-6">
                    <h3 className="text-white font-bold">Wi-Fi para Clientes</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <AuthInput label="Nome da Rede (SSID)" icon={Smartphone} {...register("wifi_ssid")} />
                      <AuthInput label="Senha do Wi-Fi" icon={Smartphone} {...register("wifi_password")} />
                    </div>
                  </div>
                </div>
              )}

              {activeTab === "finance" && (
                <div className="space-y-6 animate-in fade-in">
                  <div className="bg-purple-900/20 border border-purple-500/30 p-4 rounded-xl">
                    <h3 className="text-white font-bold mb-2">Cashback (Fidelidade)</h3>
                    <p className="text-xs text-gray-400 mb-4">Porcentagem do pedido que volta como crédito.</p>
                    <div className="flex items-center gap-2">
                      <input type="number" className="w-24 bg-gray-900 border border-gray-700 rounded-lg p-2 text-white outline-none focus:ring-2 focus:ring-purple-500" {...register("loyalty_percentage")} />
                      <span className="text-gray-400 font-bold">%</span>
                    </div>
                  </div>
                  <AuthInput label="Chave Pix (Manual)" icon={CreditCard} placeholder="CPF/CNPJ/Email" {...register("pix_key")} />
                  <AuthInput label="Token Mercado Pago (Produção)" type="password" icon={CreditCard} placeholder="APP_USR-..." {...register("mp_access_token")} />
                </div>
              )}
            </form>
          )}

          <div className="bg-red-900/10 border border-red-900/30 rounded-xl p-6 space-y-4">
            <h3 className="text-red-500 font-bold mb-2 flex items-center gap-2"><AlertTriangle size={18}/> Zona de Perigo</h3>
            
            <button 
              onClick={() => { throw new Error("Teste Sentry Frontend: Erro Simulado pelo Usuário"); }}
              className="w-full text-red-400 hover:text-red-300 text-sm font-bold flex items-center justify-center gap-2 hover:bg-red-900/20 px-4 py-3 rounded-lg transition-colors border border-red-900/30"
            >
              <Bug size={16} /> Simular Erro (Teste Sentry)
            </button>

            <button 
              onClick={() => toast.error("Funcionalidade desativada na demo.")}
              className="w-full text-red-400 hover:text-red-300 text-sm font-bold flex items-center justify-center gap-2 hover:bg-red-900/20 px-4 py-3 rounded-lg transition-colors"
            >
              <Trash2 size={16} /> Excluir minha conta e dados
            </button>
          </div>
        </div>

        <div className="hidden lg:block lg:col-span-1">
          <div className="sticky top-24">
            <h3 className="text-gray-400 text-xs font-bold uppercase tracking-wider mb-4 text-center">Preview do Cliente</h3>
            <div className="bg-white rounded-[2rem] border-8 border-gray-800 overflow-hidden shadow-2xl relative h-[600px] flex flex-col mx-auto w-[320px]">
              <div className="h-32 bg-gray-200 relative shrink-0">
                {watchedBanner ? <img src={watchedBanner} className="w-full h-full object-cover" alt="Banner" /> : <div className="w-full h-full bg-gray-300 flex items-center justify-center text-gray-400 text-xs">Sem Banner</div>}
                <div className="absolute -bottom-6 left-4 w-16 h-16 bg-white rounded-xl shadow-md p-1 z-10">
                  {watchedLogo ? <img src={watchedLogo} className="w-full h-full object-contain rounded-lg" alt="Logo" /> : <div className="w-full h-full bg-gray-200 rounded-lg"></div>}
                </div>
              </div>
              <div className="bg-white px-4 pt-8 pb-4 shadow-sm border-b border-gray-100 relative z-0">
                <h2 className="font-bold text-gray-900 text-lg leading-tight truncate">{watchedName || "Nome do Restaurante"}</h2>
                <p className="text-xs text-gray-500 mt-1">Aberto • Fecha às 23:00</p>
              </div>
              <div className="p-4 bg-gray-50 flex-1 overflow-hidden space-y-3">
                <div className="flex gap-2 overflow-x-auto pb-2 no-scrollbar">
                  <div className="px-3 py-1 rounded-full text-xs font-bold text-white shadow-sm" style={{ backgroundColor: watchedColor }}>Lanches</div>
                  <div className="px-3 py-1 rounded-full text-xs font-bold bg-white text-gray-500 border">Bebidas</div>
                </div>
                {[1, 2].map(i => (
                  <div key={i} className="bg-white p-3 rounded-xl border border-gray-100 flex gap-3 shadow-sm">
                    <div className="w-16 h-16 bg-gray-200 rounded-lg shrink-0"></div>
                    <div className="flex-1 min-w-0">
                      <div className="h-3 w-20 bg-gray-200 rounded mb-2"></div>
                      <div className="h-2 w-full bg-gray-100 rounded mb-1"></div>
                      <p className="text-xs font-bold mt-2" style={{ color: watchedColor }}>R$ 25,00</p>
                    </div>
                  </div>
                ))}
              </div>
              <div className="bg-white border-t border-gray-200 p-3 text-center text-xs text-gray-400">Menu Digital</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}