"use client";

import { useEffect, useState } from "react";
import { getCompanySettings, updateCompanySettings } from "@/lib/api";
import { Company } from "@/types";
import { toast, Toaster } from "sonner";
import { Loader2, Save, Store, Palette, Clock, Globe, Smartphone } from "lucide-react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { settingsSchema, SettingsSchema } from "@/lib/validations/settings";
import ImageUpload from "@/components/ui/ImageUpload";
import ColorPicker from "@/components/ui/ColorPicker";
import BillingSection from "./BillingSection";
import FinanceSection from "./FinanceSection";
import FiscalSection from "./FiscalSection"; // NOVO

export default function SettingsPage({ params }: { params: { slug: string } }) {
  const [company, setCompany] = useState<Company | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    reset,
    formState: { errors, isDirty },
  } = useForm<SettingsSchema>({
    resolver: zodResolver(settingsSchema),
  });

  useEffect(() => {
    getCompanySettings()
      .then((data) => {
        setCompany(data);
        // Preenche o formulário com dados existentes
        reset({
          name: data.name,
          logo_url: data.logo_url,
          banner_url: data.banner_url,
          primary_color: data.primary_color,
          background_color: data.background_color,
          text_color: data.text_color,
          accent_color: data.accent_color,
          opens_at: data.opens_at,
          closes_at: data.closes_at,
          instagram_url: data.instagram_url,
          whatsapp_number: data.whatsapp_number,
          wifi_ssid: data.wifi_ssid,
          wifi_password: data.wifi_password,
          // Campos fiscais são tratados no FiscalSection, mas o reset limpa tudo, então ok
        });
      })
      .catch(() => toast.error("Erro ao carregar configurações"))
      .finally(() => setLoading(false));
  }, [reset]);

  const onSubmit = async (data: SettingsSchema) => {
    setSaving(true);
    try {
      await updateCompanySettings(data);
      toast.success("Configurações salvas com sucesso!");
      // Atualiza estado local para refletir mudanças
      setCompany(prev => prev ? { ...prev, ...data } : null);
    } catch (error: any) {
      toast.error(error.message || "Erro ao salvar");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="flex h-screen items-center justify-center bg-gray-900 text-white"><Loader2 className="animate-spin" /></div>;
  if (!company) return null;

  return (
    <div className="space-y-8 pb-20 max-w-5xl mx-auto">
      <Toaster position="top-right" richColors />
      
      <div>
        <h1 className="text-3xl font-bold text-white">Configurações da Loja</h1>
        <p className="text-gray-400 text-sm mt-1">Gerencie a aparência, operação e integrações do seu negócio.</p>
      </div>

      {/* SEÇÃO 1: IDENTIDADE VISUAL */}
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        <div className="bg-gray-800 border border-gray-700 rounded-xl p-6">
          <h3 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
            <Palette className="text-orange-500" /> Identidade Visual
          </h3>
          
          <div className="grid md:grid-cols-2 gap-8 mb-8">
            <ImageUpload 
              label="Logo da Loja" 
              value={watch("logo_url")} 
              onChange={(url) => setValue("logo_url", url, { shouldDirty: true })} 
            />
            <ImageUpload 
              label="Banner de Capa" 
              value={watch("banner_url")} 
              onChange={(url) => setValue("banner_url", url, { shouldDirty: true })} 
            />
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <ColorPicker label="Cor Primária" value={watch("primary_color")} onChange={(c) => setValue("primary_color", c, { shouldDirty: true })} />
            <ColorPicker label="Cor de Fundo" value={watch("background_color") || "#f9fafb"} onChange={(c) => setValue("background_color", c, { shouldDirty: true })} />
            <ColorPicker label="Cor do Texto" value={watch("text_color") || "#111827"} onChange={(c) => setValue("text_color", c, { shouldDirty: true })} />
            <ColorPicker label="Cor de Destaque" value={watch("accent_color") || "#ea580c"} onChange={(c) => setValue("accent_color", c, { shouldDirty: true })} />
          </div>
        </div>

        {/* SEÇÃO 2: OPERAÇÃO */}
        <div className="bg-gray-800 border border-gray-700 rounded-xl p-6">
          <h3 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
            <Store className="text-green-500" /> Dados Operacionais
          </h3>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-bold text-gray-300 mb-1">Nome da Loja</label>
              <input {...register("name")} className="input-modern bg-gray-900 text-white border-gray-600" />
              {errors.name && <p className="text-red-400 text-xs mt-1">{errors.name.message}</p>}
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-bold text-gray-300 mb-1 flex items-center gap-1"><Clock size={14}/> Abertura</label>
                <input type="time" {...register("opens_at")} className="input-modern bg-gray-900 text-white border-gray-600" />
              </div>
              <div>
                <label className="block text-sm font-bold text-gray-300 mb-1 flex items-center gap-1"><Clock size={14}/> Fechamento</label>
                <input type="time" {...register("closes_at")} className="input-modern bg-gray-900 text-white border-gray-600" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-300 mb-1 flex items-center gap-1"><Globe size={14}/> Instagram (URL)</label>
              <input {...register("instagram_url")} placeholder="https://instagram.com/..." className="input-modern bg-gray-900 text-white border-gray-600" />
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-300 mb-1 flex items-center gap-1"><Smartphone size={14}/> WhatsApp (Número)</label>
              <input {...register("whatsapp_number")} placeholder="5511999999999" className="input-modern bg-gray-900 text-white border-gray-600" />
            </div>
          </div>
        </div>

        {/* BOTÃO SALVAR GERAL */}
        <div className="flex justify-end sticky bottom-6 z-20">
          <button 
            type="submit" 
            disabled={saving || !isDirty}
            className="bg-orange-600 hover:bg-orange-700 text-white px-8 py-4 rounded-xl font-bold text-lg shadow-2xl shadow-orange-900/50 flex items-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed active:scale-95"
          >
            {saving ? <Loader2 className="animate-spin" /> : <Save />}
            Salvar Alterações
          </button>
        </div>
      </form>

      {/* SEÇÃO 3: MÓDULOS ESPECÍFICOS (Componentes Isolados) */}
      <div className="grid gap-8">
        <FiscalSection company={company} />
        <FinanceSection company={company} />
        <BillingSection company={company} />
      </div>
    </div>
  );
}
