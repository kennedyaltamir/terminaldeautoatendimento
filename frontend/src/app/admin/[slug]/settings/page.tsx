"use client";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { getCompanySettings, updateCompanySettings, getWebhooks } from "@/lib/api";
import { settingsSchema, SettingsSchema } from "@/lib/validations/settings";
import { 
  Save, Loader2, Store, Smartphone, CreditCard, Image as ImageIcon, 
  Zap, Clock, Wifi, Palette, MessageSquare, Globe, Key, Bike, Send, Printer, FileText, Eye, EyeOff,
  Webhook, Plus, Trash2, ShieldCheck, Copy
} from "lucide-react";
import { toast, Toaster } from "sonner";
import AuthInput from "@/components/ui/AuthInput";
import ColorPicker from "@/components/ui/ColorPicker";
import ImageUpload from "@/components/ui/ImageUpload";
import BillingSection from "./BillingSection";
import PrinterSettings from "@/components/admin/PrinterSettings";
import FiscalSettings from "@/components/admin/FiscalSettings";
import WebhookManager from "@/components/admin/WebhookManager";
import WhatsappStatus from "@/components/admin/WhatsappStatus";
import { Company } from "@/types";

export default function SettingsPage() {
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"general" | "marketing" | "finance" | "fiscal" | "printer" | "integrations" | "billing">("general");
  const [companyData, setCompanyData] = useState<Company | null>(null);
  const [webhooks, setWebhooks] = useState<any[]>([]);
  const [showToken, setShowToken] = useState(false);

  const {
    register, handleSubmit, setValue, watch, reset,
    formState: { errors, isSubmitting, isDirty },
  } = useForm<SettingsSchema>({
    resolver: zodResolver(settingsSchema),
  });

  const watchedLogo = watch("logo_url");
  const watchedBanner = watch("banner_url");
  const watchedColor = watch("primary_color");
  const watchedBg = watch("background_color");
  const watchedText = watch("text_color");

  const loadData = async () => {
    try {
      const [data, webhooksData] = await Promise.all([
        getCompanySettings(),
        getWebhooks()
      ]);
      setCompanyData(data);
      setWebhooks(webhooksData);
      reset({
        ...data,
        opens_at: data.opens_at ? data.opens_at.slice(0, 5) : "",
        closes_at: data.closes_at ? data.closes_at.slice(0, 5) : "",
      });
    } catch (e) {
      toast.error("Erro ao carregar configurações");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [reset]);

  const onSubmit = async (data: SettingsSchema) => {
    try {
      const payload = Object.fromEntries(
        Object.entries(data).map(([k, v]) => [k, v === "" ? null : v])
      );
      
      await updateCompanySettings(payload as Partial<Company>);
      toast.success("Configurações salvas!");
      reset(data);
    } catch (e: any) {
      toast.error(e.message || "Erro ao salvar");
    }
  };

  if (loading || !companyData) return <div className="text-center py-20 text-gray-500">Carregando...</div>;

  const tabs = [
    { id: "general", label: "Geral & Marca", icon: Store },
    { id: "marketing", label: "Marketing", icon: Smartphone },
    { id: "finance", label: "Financeiro", icon: CreditCard },
    { id: "fiscal", label: "Fiscal", icon: FileText },
    { id: "printer", label: "Impressão", icon: Printer },
    { id: "integrations", label: "Integrações", icon: Webhook },
    { id: "billing", label: "Assinatura", icon: Zap }
  ];

  return (
    <div className="max-w-7xl mx-auto pb-20">
      <Toaster position="top-right" richColors />
      
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-white">Configurações</h1>
        {activeTab !== "billing" && activeTab !== "integrations" && activeTab !== "printer" && (
          <button onClick={handleSubmit(onSubmit)} disabled={isSubmitting || !isDirty} className="bg-orange-600 hover:bg-orange-700 disabled:opacity-50 text-white px-6 py-2 rounded-xl font-bold flex items-center gap-2 transition-all">
            {isSubmitting ? <Loader2 className="animate-spin" size={20} /> : <Save size={20} />}
            Salvar Alterações
          </button>
        )}
      </div>

      <div className="flex flex-col lg:flex-row gap-8">
        <div className="lg:w-64 shrink-0 space-y-2">
          {tabs.map((tab) => (
            <button key={tab.id} onClick={() => setActiveTab(tab.id as any)} className={`w-full text-left p-4 rounded-xl flex items-center gap-3 transition-all ${activeTab === tab.id ? "bg-orange-600 text-white shadow-lg" : "bg-gray-800 text-gray-400 hover:bg-gray-700"}`}>
              <tab.icon size={18} /> <span className="font-bold text-sm">{tab.label}</span>
            </button>
          ))}
        </div>

        <div className="flex-1 min-w-0 space-y-6">
          {activeTab === "general" && (
            <div className="bg-gray-800 rounded-xl border border-gray-700 p-6 shadow-xl space-y-8 animate-in fade-in">
              <AuthInput label="Nome do Restaurante" icon={Store} {...register("name")} error={errors.name?.message} />
              <div className="grid grid-cols-2 gap-4">
                <AuthInput label="Abre às" type="time" icon={Clock} {...register("opens_at")} />
                <AuthInput label="Fecha às" type="time" icon={Clock} {...register("closes_at")} />
              </div>
              <div className="border-t border-gray-700 pt-6 space-y-6">
                <ImageUpload label="Logo" value={watchedLogo} onChange={(url) => setValue("logo_url", url, { shouldDirty: true })} />
                <ImageUpload label="Banner" value={watchedBanner} onChange={(url) => setValue("banner_url", url, { shouldDirty: true })} />
              </div>
              <div className="border-t border-gray-700 pt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
                <ColorPicker label="Cor Principal" value={watchedColor} onChange={(c) => setValue("primary_color", c, { shouldDirty: true })} />
                <ColorPicker label="Fundo" value={watchedBg || "#f9fafb"} onChange={(c) => setValue("background_color", c, { shouldDirty: true })} />
                <ColorPicker label="Texto" value={watchedText || "#111827"} onChange={(c) => setValue("text_color", c, { shouldDirty: true })} />
              </div>
            </div>
          )}

          {activeTab === "marketing" && (
            <div className="bg-gray-800 rounded-xl border border-gray-700 p-6 shadow-xl space-y-6 animate-in fade-in">
              <h3 className="text-lg font-bold text-white flex items-center gap-2"><Smartphone size={20} className="text-blue-500"/> Redes Sociais</h3>
              <AuthInput label="Instagram URL" icon={Smartphone} placeholder="https://instagram.com/..." {...register("instagram_url")} />
              <AuthInput label="WhatsApp do Restaurante (Público)" icon={Smartphone} placeholder="5511999999999" {...register("whatsapp_number")} />
              <div className="border-t border-gray-700 pt-6">
                <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2"><Wifi size={20} className="text-blue-500"/> Wi-Fi para Clientes</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <AuthInput label="Nome da Rede (SSID)" icon={Wifi} {...register("wifi_ssid")} />
                  <AuthInput label="Senha do Wi-Fi" icon={Wifi} {...register("wifi_password")} />
                </div>
              </div>
            </div>
          )}

          {activeTab === "finance" && (
            <div className="bg-gray-800 rounded-xl border border-gray-700 p-6 shadow-xl space-y-6 animate-in fade-in">
              <h3 className="text-lg font-bold text-white flex items-center gap-2"><CreditCard size={20} className="text-green-500"/> Taxas & Fidelidade</h3>
              <div className="grid md:grid-cols-2 gap-6">
                <AuthInput label="Cashback (%)" type="number" icon={Zap} {...register("loyalty_percentage")} />
                <AuthInput label="Taxa de Entrega (R$)" type="number" step="0.01" icon={Bike} {...register("fixed_delivery_fee")} />
              </div>
              <div className="border-t border-gray-700 pt-6 space-y-4">
                <h3 className="text-lg font-bold text-white mb-2">Integrações de Pagamento</h3>
                <AuthInput label="Chave Pix (Manual)" icon={CreditCard} placeholder="CPF/CNPJ/Email" {...register("pix_key")} />
                <div className="relative">
                  <AuthInput 
                    label="Token Mercado Pago (Produção)" 
                    type={showToken ? "text" : "password"} 
                    icon={Key} 
                    placeholder="APP_USR-..." 
                    {...register("mp_access_token")} 
                  />
                  <button 
                    type="button"
                    onClick={() => setShowToken(!showToken)}
                    className="absolute right-3 top-[34px] text-gray-400 hover:text-white"
                  >
                    {showToken ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === "integrations" && (
            <div className="space-y-6 animate-in fade-in">
              <WhatsappStatus />
              <div className="bg-gray-800 rounded-xl border border-gray-700 p-6 shadow-xl space-y-6">
                <h3 className="text-lg font-bold text-white flex items-center gap-2"><Globe size={20} className="text-green-500"/> Configuração da API de Mensagens</h3>
                <AuthInput label="URL da API" icon={Globe} placeholder="https://api.sua-instancia.com" {...register("whatsapp_api_url")} />
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <AuthInput label="Nome da Instância" icon={MessageSquare} placeholder="MesaFlow_01" {...register("whatsapp_instance")} />
                  <AuthInput label="Token da API" type="password" icon={Key} placeholder="Token de segurança" {...register("whatsapp_token")} />
                </div>
                <div className="border-t border-gray-700 pt-6">
                  <WebhookManager webhooks={webhooks} onUpdate={loadData} />
                </div>
              </div>
            </div>
          )}

          {activeTab === "billing" && <BillingSection company={companyData} />}
          {activeTab === "fiscal" && <FiscalSettings register={register} errors={errors} />}
          {activeTab === "printer" && <PrinterSettings />}
        </div>
      </div>
    </div>
  );
}
