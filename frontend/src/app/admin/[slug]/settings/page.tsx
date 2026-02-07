/**
 * Author: MESAFLOW_AI
 * Version: 16.0.0 (Platinum Master - DOM & Security Fix)
 * DNA_ID: settings-page-v16-master
 * Objective: Unified Unit Governance. Fixed DOM warnings and optimized form hierarchy.
 * LAST_MODIFIED: 2026-01-28 16:40:00
 */
"use client";

import React, { use, useState, useEffect, useCallback, useMemo } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { settingsSchema, SettingsSchema } from "@/lib/validations/settings";
import { getCompanySettings, updateCompanySettings, getWebhooks } from "@/lib/api";
import { 
  Save, Loader2, Building2, Palette, 
  ShieldCheck, CreditCard, 
  Info, Lock as LockIcon,
  Smartphone, Instagram, QrCode, Globe,
  MessageSquare, Key, Send, FileText,
  Printer, Monitor, CheckCircle2, Trash2,
  Bug, Clock, Webhook, Eye, EyeOff,
  Zap, AlertTriangle, Wifi, Terminal
} from "lucide-react";
import { toast } from "sonner";
import { cn, formatCurrency } from "@/lib/utils";
import { Company, WebhookResponse } from "@/types";

// Componentes de UI
import AuthInput from "@/components/ui/AuthInput";
import ColorPicker from "@/components/ui/ColorPicker";
import ImageUpload from "@/components/ui/ImageUpload";

// Seções Modulares
import BillingSection from "./BillingSection";
import PrinterSettings from "@/components/admin/PrinterSettings";
import FiscalSettings from "@/components/admin/FiscalSettings";
import WebhookManager from "@/components/admin/WebhookManager";
import WhatsappStatus from "@/components/admin/WhatsappStatus";

export default function SettingsPage({ params: paramsPromise }: { params: Promise<{ slug: string }> }) {
  const { slug } = use(paramsPromise);
  
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<string>("general");
  const [companyData, setCompanyData] = useState<Company | null>(null);
  const [webhooks, setWebhooks] = useState<WebhookResponse[]>([]);
  const [showToken, setShowToken] = useState(false);
  const [testingWhatsapp, setTestingWhatsapp] = useState(false);

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    reset,
    formState: { errors, isSubmitting, isDirty },
  } = useForm<SettingsSchema>({
    resolver: zodResolver(settingsSchema),
    mode: "onChange"
  });

  const watchedName = watch("name");
  const watchedLogo = watch("logo_url");
  const watchedBanner = watch("banner_url");
  const watchedColor = watch("primary_color") || "#ea580c";

  const loadData = useCallback(async () => {
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
        qr_config: data.qr_config || {
          show_wifi: true,
          show_instagram: true,
          show_steps: true,
          show_logo: true,
          dark_mode: false,
          custom_color: data.primary_color
        }
      });
    } catch (e) {
      setTimeout(() => toast.error("Erro ao carregar configurações."), 0);
    } finally {
      setLoading(false);
    }
  }, [reset]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const onSubmit = async (data: SettingsSchema) => {
    try {
      const payload = Object.fromEntries(
        Object.entries(data).map(([k, v]) => [k, v === "" ? null : v])
      );
      await updateCompanySettings(payload as Partial<Company>);
      toast.success("Configurações seladas com sucesso!");
      reset(data);
    } catch (e: any) {
      toast.error(e.message || "Erro ao salvar.");
    }
  };

  const onInvalid = useCallback((formErrors: any) => {
    setTimeout(() => {
      const errorCount = Object.keys(formErrors).length;
      toast.error(`Existem ${errorCount} campo(s) com erro.`, {
        description: "Verifique os campos destacados em vermelho."
      });
    }, 0);
  }, []);

  if (loading || !companyData) return (
    <div className="flex h-screen items-center justify-center bg-black">
      <div className="flex flex-col items-center gap-4">
      <Loader2 className="animate-spin text-orange-500" size={40} />
        <p className="text-slate-500 font-black uppercase tracking-widest text-[10px]">Sincronizando Unidade...</p>
      </div>
    </div>
  );

  const tabs = [
    { id: "general", label: "Geral & Marca", icon: Building2, desc: "Identidade e horários" },
    { id: "hardware", label: "Hardware POS", icon: Terminal, desc: "Máquinas Stone/TEF" },
    { id: "marketing", label: "Marketing & Wi-Fi", icon: Smartphone, desc: "Redes e conexões" },
    { id: "finance", label: "Financeiro & Taxas", icon: CreditCard, desc: "Pagamentos e delivery" },
    { id: "kiosk", label: "Segurança Totem", icon: LockIcon, desc: "Autoatendimento" },
    { id: "integrations", label: "Integrações", icon: Webhook, desc: "Webhooks e APIs" },
    { id: "fiscal", label: "Fiscal", icon: FileText, desc: "NFC-e e Impostos" },
    { id: "billing", label: "Assinatura", icon: Zap, desc: "Plano MesaFlow" },
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-8 pb-20 animate-in fade-in duration-500">
      {/* 🛡️ FORMULÁRIO SOBERANO: Envolve toda a estrutura para evitar avisos de DOM */}
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-8">
          <div>
            <h1 className="text-4xl font-black text-white tracking-tighter uppercase">Configurações</h1>
            <p className="text-slate-500 text-sm font-bold uppercase tracking-widest mt-1">Unidade: {slug}</p>
          </div>
          <button 
            type="submit"
            disabled={isSubmitting || !isDirty}
            className={cn(
              "px-8 py-4 rounded-2xl font-black uppercase text-xs tracking-widest flex items-center gap-3 shadow-xl transition-all active:scale-95 disabled:opacity-50",
              isDirty ? "bg-orange-600 text-white shadow-orange-900/20" : "bg-slate-800 text-slate-500"
            )}
          >
            {isSubmitting ? <Loader2 className="animate-spin" size={18} /> : <Save size={18} />}
            {isDirty ? "Salvar Alterações" : "Sincronizado"}
          </button>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* NAVEGAÇÃO */}
          <aside className="lg:col-span-3 space-y-2">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                type="button"
                onClick={() => setActiveTab(tab.id)}
                className={cn(
                  "w-full flex items-center gap-4 px-6 py-4 rounded-2xl text-left transition-all group",
                  activeTab === tab.id 
                    ? "bg-orange-600 text-white shadow-lg shadow-orange-900/20" 
                    : "bg-slate-900/50 text-slate-500 hover:text-slate-300 hover:bg-slate-900 border border-transparent hover:border-slate-800"
                )}
              >
                <div className={cn(
                  "p-2 rounded-lg transition-colors",
                  activeTab === tab.id ? "bg-white/20" : "bg-black/20 group-hover:bg-black/40"
                )}>
                  <tab.icon size={18} />
                </div>
                <div>
                  <p className="font-black text-sm uppercase tracking-tight">{tab.label}</p>
                  <p className={cn("text-[10px] font-bold", activeTab === tab.id ? "text-orange-100" : "text-slate-600")}>{tab.desc}</p>
                </div>
              </button>
            ))}
          </aside>

          {/* CONTEÚDO DAS ABAS */}
          <main className="lg:col-span-6 space-y-8">
            {activeTab === "general" && (
              <div className="bg-slate-900/50 border border-slate-800 p-8 rounded-[2.5rem] space-y-8 animate-in slide-in-from-bottom-2">
                <h3 className="text-white font-black uppercase text-xs tracking-widest flex items-center gap-2">
                  <Building2 size={16} className="text-orange-500" /> Dados Gerais
                </h3>
                <div className="space-y-6">
                  <AuthInput label="Nome Comercial" icon={Building2} {...register("name")} error={errors.name?.message} />
                  <div className="grid grid-cols-2 gap-4">
                    <AuthInput label="Abre às" type="time" icon={Clock} {...register("opens_at")} />
                    <AuthInput label="Fecha às" type="time" icon={Clock} {...register("closes_at")} />
                  </div>
                  <AuthInput label="CNPJ" icon={FileText} {...register("cnpj")} error={errors.cnpj?.message} />
                </div>
                <div className="border-t border-slate-800 pt-8 space-y-8">
                  <h3 className="text-white font-black uppercase text-xs tracking-widest flex items-center gap-2">
                    <Palette size={16} className="text-orange-500" /> Branding
                  </h3>
                  <ImageUpload label="Logo" value={watchedLogo} onChange={(url) => setValue("logo_url", url, { shouldDirty: true })} />
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <ColorPicker label="Cor Principal" value={watchedColor} onChange={(c) => setValue("primary_color", c, { shouldDirty: true })} />
                  </div>
                </div>
              </div>
            )}

            {activeTab === "hardware" && (
              <div className="bg-slate-900/50 border border-slate-800 p-8 rounded-[2.5rem] space-y-8 animate-in slide-in-from-bottom-2">
                <div className="flex items-center gap-4">
                  <div className="bg-blue-600/20 p-3 rounded-2xl text-blue-500 border border-blue-500/20"><Terminal size={24} /></div>
                  <div>
                    <h2 className="text-xl font-bold text-white">Hardware POS</h2>
                    <p className="text-[10px] text-slate-500 uppercase font-black tracking-[0.2em]">Stone Smart POS</p>
                  </div>
                </div>
                <div className="grid md:grid-cols-2 gap-6">
                  <AuthInput label="Stone Merchant ID" icon={Key} placeholder="ID do Lojista" {...register("stone_merchant_id")} />
                  <AuthInput label="Stone Terminal ID (S/N)" icon={Smartphone} placeholder="Número de Série" {...register("stone_terminal_id")} />
                </div>
              <div className="p-5 bg-blue-500/5 border border-blue-500/10 rounded-3xl flex gap-4 items-center">
                <ShieldCheck className="text-blue-500 shrink-0" size={24} />
                <p className="text-xs text-blue-200/60 leading-relaxed font-medium">
                  A vinculação do hardware permite que o MesaFlow OS dispare o valor da venda diretamente para o leitor de cartões via protocolo Intent.
                </p>
              </div>
            </div>
          )}

          {activeTab === "marketing" && (
            <div className="bg-slate-900/50 border border-slate-800 p-8 rounded-[2.5rem] space-y-8 animate-in slide-in-from-bottom-2">
              <h3 className="text-white font-black uppercase text-xs tracking-widest flex items-center gap-2">
                <Smartphone size={16} className="text-blue-500" /> Presença Digital
              </h3>
              <div className="space-y-6">
                <AuthInput label="Instagram URL" icon={Instagram} placeholder="https://instagram.com/..." {...register("instagram_url")} />
                <AuthInput label="WhatsApp Público" icon={MessageSquare} placeholder="5511999999999" {...register("whatsapp_number")} />
                <div className="border-t border-slate-800 pt-8 space-y-6">
                  <h4 className="text-white font-bold text-sm flex items-center gap-2"><Wifi size={16} className="text-purple-500"/> Wi-Fi para Clientes</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <AuthInput label="Nome da Rede (SSID)" icon={Wifi} {...register("wifi_ssid")} />
                    <AuthInput label="Senha do Wi-Fi" icon={LockIcon} {...register("wifi_password")} />
                  </div>
                </div>
              </div>
              </div>
            )}

            {activeTab === "finance" && (
              <div className="bg-slate-900/50 border border-slate-800 p-8 rounded-[2.5rem] space-y-8 animate-in slide-in-from-bottom-2">
                <h3 className="text-white font-black uppercase text-xs tracking-widest flex items-center gap-2">
                  <CreditCard size={16} className="text-emerald-500" /> Financeiro
                </h3>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-purple-900/10 border border-purple-500/20 p-6 rounded-3xl">
                  <p className="text-[10px] font-black text-purple-400 uppercase mb-2">Cashback (%)</p>
                  <input type="number" className="w-full bg-black/40 border border-slate-800 rounded-xl p-3 text-white outline-none focus:border-purple-500" {...register("loyalty_percentage")} />
                </div>
                <div className="bg-blue-900/10 border border-blue-500/20 p-6 rounded-3xl">
                  <p className="text-[10px] font-black text-blue-400 uppercase mb-2">Taxa de Entrega (R$)</p>
                  <input type="number" step="0.01" className="w-full bg-black/40 border border-slate-800 rounded-xl p-3 text-white outline-none focus:border-blue-500" {...register("fixed_delivery_fee")} />
                </div>
              </div>
              <div className="border-t border-slate-800 pt-8 space-y-6">
                <AuthInput label="Chave Pix (Recebimento Direto)" icon={QrCode} {...register("pix_key")} />
                  <div className="relative">
                    {/* 🛡️ FIX: Adicionado autoComplete="off" para API Keys */}
                    <AuthInput 
                      label="Mercado Pago Token" 
                      type={showToken ? "text" : "password"} 
                      icon={Key} 
                      autoComplete="off"
                      {...register("mp_access_token")} 
                    />
                    <button type="button" onClick={() => setShowToken(!showToken)} className="absolute right-4 top-10 text-slate-500 hover:text-white">
                      {showToken ? <EyeOff size={16} /> : <Eye size={16} />}
                    </button>
                  </div>
                </div>
              </div>
            )}

            {activeTab === "kiosk" && (
              <div className="bg-slate-900/50 border border-slate-800 p-8 rounded-[2.5rem] space-y-8 animate-in slide-in-from-bottom-2">
                <h3 className="text-white font-black uppercase text-xs tracking-widest flex items-center gap-2">
                  <Monitor size={16} className="text-orange-500" /> Segurança Totem
                </h3>
                <div className="space-y-2">
                  <label className="text-[10px] font-black text-slate-500 uppercase ml-2">Senha Mestra de Saída</label>
                  {/* 🛡️ FIX: Adicionado autoComplete="new-password" para evitar avisos de DOM */}
                  <input 
                    type="password" 
                    maxLength={6} 
                    autoComplete="new-password"
                    placeholder="Padrão: 123456" 
                    {...register("kiosk_password")} 
                    className="w-full bg-black border border-slate-800 rounded-xl p-4 text-white focus:border-orange-500 outline-none transition-all font-mono text-2xl tracking-[0.5em]" 
                  />
                </div>
              </div>
            )}

          {activeTab === "integrations" && (
            <div className="space-y-6 animate-in slide-in-from-bottom-2">
              <WhatsappStatus />
              <WebhookManager webhooks={webhooks} onUpdate={loadData} />
            </div>
          )}

            {activeTab === "fiscal" && <FiscalSettings register={register} errors={errors} />}
            {activeTab === "printer" && <PrinterSettings />}
            {activeTab === "billing" && <BillingSection company={companyData} />}

          {/* DANGER ZONE */}
          <div className="bg-red-950/20 border border-red-900/30 rounded-[2rem] p-8 space-y-4">
            <h3 className="text-red-500 font-black uppercase text-xs tracking-widest flex items-center gap-2">
              <AlertTriangle size={18}/> Zona de Perigo
            </h3>
            <div className="flex flex-col md:flex-row gap-4">
              <button type="button" onClick={() => { throw new Error("Teste Sentry Manual"); }} className="flex-1 bg-slate-900 text-red-400 hover:bg-red-900/20 border border-red-900/30 py-3 rounded-xl font-bold text-xs flex items-center justify-center gap-2 transition-all">
                <Bug size={16} /> Simular Erro Crítico
              </button>
              <button type="button" className="flex-1 bg-red-600 hover:bg-red-700 text-white py-3 rounded-xl font-bold text-xs flex items-center justify-center gap-2 transition-all shadow-lg shadow-red-900/20">
                <Trash2 size={16} /> Excluir Conta
              </button>
            </div>
          </div>
          </main>

          {/* PREVIEW */}
          <aside className="lg:col-span-3 hidden lg:block">
            <div className="sticky top-24 space-y-4">
              <h3 className="text-slate-500 font-black uppercase text-[10px] tracking-[0.2em] text-center">Live Preview</h3>
              <div className="bg-slate-900 rounded-[3rem] border-[8px] border-slate-800 overflow-hidden shadow-2xl relative h-[600px] flex flex-col ring-4 ring-black">
                <div className="h-32 bg-slate-800 relative shrink-0">
                  {watchedBanner && <img src={watchedBanner} className="w-full h-full object-cover opacity-50" alt="Banner" />}
                  <div className="absolute -bottom-6 left-6 w-16 h-16 bg-white rounded-2xl shadow-xl p-1.5 z-10 border border-slate-200">
                    {watchedLogo ? <img src={watchedLogo} className="w-full h-full object-contain rounded-lg" alt="Logo" /> : <div className="w-full h-full bg-slate-100 rounded-lg flex items-center justify-center text-slate-300 font-black text-xl">{watchedName?.charAt(0) || "M"}</div>}
                  </div>
                </div>
                <div className="bg-white px-6 pt-10 pb-4 border-b border-slate-100">
                  <h2 className="font-black text-slate-900 text-lg leading-tight truncate">{watchedName || "Nome da Loja"}</h2>
                  <div className="flex items-center gap-2 mt-1">
                    <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                    <p className="text-[10px] text-slate-500 font-bold uppercase tracking-tighter">Aberto agora</p>
                  </div>
                </div>
                <div className="p-4 bg-slate-50 flex-1 overflow-hidden space-y-4">
                <div className="flex gap-2 overflow-x-auto no-scrollbar pb-2">
                  <div className="px-4 py-1.5 rounded-full text-[10px] font-black text-white shadow-md shrink-0" style={{ backgroundColor: watchedColor }}>LANCHES</div>
                  <div className="px-4 py-1.5 rounded-full text-[10px] font-black bg-white text-slate-400 border border-slate-200 shrink-0">BEBIDAS</div>
                </div>
                {[1, 2].map(i => (
                  <div key={i} className="bg-white p-3 rounded-2xl shadow-sm flex justify-between items-center border border-slate-100">
                    <div className="flex-1 pr-3">
                      <div className="h-2.5 w-20 bg-slate-100 rounded-full mb-2" />
                      <div className="h-2 w-full bg-slate-50 rounded-full mb-1" />
                      <p className="font-black text-xs mt-2" style={{ color: watchedColor }}>R$ 25,00</p>
                    </div>
                    <div className="w-14 h-14 bg-slate-100 rounded-xl flex items-center justify-center"><CheckCircle2 size={20} className="text-slate-200" /></div>
                  </div>
                ))}
              </div>
              <div className="bg-white border-t border-slate-100 p-4 flex justify-center"><div className="w-32 h-1 bg-slate-200 rounded-full" /></div>
              </div>
            </div>
          </aside>
        </div>
      </form>
    </div>
  );
}