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

  const { register, handleSubmit, setValue, watch, reset, formState: { errors, isSubmitting, isDirty } } = useForm<SettingsSchema>({
    resolver: zodResolver(settingsSchema),
    defaultValues: { primary_color: "#ea580c", loyalty_percentage: 0, name: "", logo_url: "", banner_url: "", opens_at: "", closes_at: "", instagram_url: "", whatsapp_number: "", wifi_ssid: "", wifi_password: "", pix_key: "", mp_access_token: "" }
  });

  const watchedColor = watch("primary_color");

  useEffect(() => {
    getCompanySettings().then((data) => {
        setCompanyData(data);
        reset({ name: data.name, logo_url: data.logo_url || "", banner_url: data.banner_url || "", primary_color: data.primary_color || "#ea580c", opens_at: data.opens_at ? data.opens_at.slice(0, 5) : "", closes_at: data.closes_at ? data.closes_at.slice(0, 5) : "", pix_key: data.pix_key || "", mp_access_token: data.mp_access_token || "", loyalty_percentage: Number(data.loyalty_percentage) || 0, instagram_url: data.instagram_url || "", whatsapp_number: data.whatsapp_number || "", wifi_ssid: data.wifi_ssid || "", wifi_password: data.wifi_password || "" });
      }).catch(() => toast.error("Erro ao carregar")).finally(() => setLoading(false));
  }, [reset]);

  const onSubmit = async (data: SettingsSchema) => {
    try {
      const payload = Object.fromEntries(Object.entries(data).map(([k, v]) => [k, v === "" ? null : v]));
      await updateCompanySettings(payload);
      toast.success("Salvo!");
      reset(data);
    } catch (error: any) { toast.error("Erro ao salvar"); }
  };

  if (loading) return <div className="text-center py-20">Carregando...</div>;

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-20">
      <Toaster position="top-right" richColors />
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-white">Configurações</h1>
        <button onClick={handleSubmit(onSubmit)} disabled={isSubmitting || !isDirty} className="bg-orange-600 text-white px-6 py-2 rounded-xl font-bold flex items-center gap-2">
          {isSubmitting ? <Loader2 className="animate-spin" size={20} /> : <Save />} Salvar
        </button>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-gray-800 p-6 rounded-xl border border-gray-700">
          <AuthInput label="Nome" icon={Store} {...register("name")} error={errors.name?.message} />
          <div className="mt-6"><ColorPicker label="Cor" value={watchedColor} onChange={(c) => setValue("primary_color", c, { shouldDirty: true })} /></div>
        </div>
      </div>
    </div>
  );
}