"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { settingsSchema, SettingsSchema } from "@/lib/validations/settings";
import { updateCompanySettings } from "@/lib/api";
import { Company } from "@/types";
import { toast } from "sonner";
import { FileText, Save, Loader2, Info, ShieldCheck, Search, ExternalLink, AlertCircle } from "lucide-react";

interface FiscalSectionProps {
  company: Company;
}

export default function FiscalSection({ company }: FiscalSectionProps) {
  const [loading, setLoading] = useState(false);
  const [searchingCnpj, setSearchingCnpj] = useState(false);
  const [testingConnection, setTestingConnection] = useState(false);
  const isSandbox = process.env.NEXT_PUBLIC_ENVIRONMENT !== 'production';

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors },
  } = useForm<SettingsSchema>({
    resolver: zodResolver(settingsSchema),
    // Sincronização total com o objeto company para satisfazer o Zod
    defaultValues: {
      ...company,
      name: company.name || "Minha Loja",
      primary_color: company.primary_color || "#ea580c",
      loyalty_percentage: company.loyalty_percentage || 0,
      fixed_delivery_fee: company.fixed_delivery_fee || 0,
      cnpj: company.cnpj || "",
      inscricao_estadual: company.inscricao_estadual || "",
      fiscal_token: company.fiscal_token || "",
      csc_token: company.csc_token || "",
      csc_id: company.csc_id || "",
    },
  });

  const cnpjValue = watch("cnpj");
  const tokenValue = watch("fiscal_token");

  const handleSearchCNPJ = async () => {
    const cleanCNPJ = cnpjValue?.replace(/\D/g, "");
    if (!cleanCNPJ || cleanCNPJ.length !== 14) {
      toast.error("Digite um CNPJ válido (14 números) para buscar.");
      return;
    }

    setSearchingCnpj(true);
    try {
      const res = await fetch(`https://brasilapi.com.br/api/cnpj/v1/${cleanCNPJ}`);
      if (!res.ok) throw new Error("CNPJ não encontrado na Receita.");
      const data = await res.json();
      toast.success(`Empresa encontrada: ${data.razao_social}`);
      setValue("cnpj", cleanCNPJ, { shouldValidate: true });
    } catch (e: any) {
      toast.error(e.message);
    } finally {
      setSearchingCnpj(false);
    }
  };

  const handleTestConnection = async () => {
    if (!tokenValue) {
      toast.error("Preencha o token antes de testar.");
      return;
    }
    setTestingConnection(true);
    try {
      if (tokenValue.length < 10) throw new Error("Token parece inválido.");
      await new Promise(r => setTimeout(r, 800));
      toast.success("Conexão simulada com sucesso!");
    } catch (e: any) {
      toast.error(e.message);
    } finally {
      setTestingConnection(false);
    }
  };

  const onSubmit = async (data: SettingsSchema) => {
    setLoading(true);
    try {
      const cleanCnpj = data.cnpj?.replace(/\D/g, "") || "";
      
      // Enviamos apenas o que mudou ou o que é relevante para esta aba
      // mas o 'data' aqui já contém tudo o que o Zod validou
      const payload = {
        cnpj: cleanCnpj,
        inscricao_estadual: data.inscricao_estadual,
        fiscal_token: data.fiscal_token,
        csc_token: data.csc_token,
        csc_id: data.csc_id
      };
      
      await updateCompanySettings(payload);
      toast.success("Configurações fiscais salvas!");
      setTimeout(() => window.location.reload(), 1000);
    } catch (error: any) {
      toast.error(error.message || "Erro ao salvar.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-xl p-6 animate-in fade-in">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <FileText className="text-blue-500" /> Emissão Fiscal (NFC-e)
          </h3>
        </div>
        {company.fiscal_token ? (
          <span className="bg-green-900/30 text-green-400 border border-green-800 px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1">
            <ShieldCheck size={14} /> Conectado
          </span>
        ) : (
          <span className="bg-gray-700 text-gray-400 px-3 py-1 rounded-full text-xs font-bold">
            Pendente
          </span>
        )}
      </div>

      <div className={`p-4 rounded-xl border mb-6 flex gap-3 ${isSandbox ? 'bg-yellow-900/20 border-yellow-700/50 text-yellow-200' : 'bg-blue-900/20 border-blue-700/50 text-blue-200'}`}>
        <Info className="shrink-0 mt-0.5" size={18} />
        <div className="text-sm">
          <p className="font-bold uppercase">Modo: {isSandbox ? 'Homologação' : 'Produção'}</p>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Campos ocultos para satisfazer o Schema global */}
        <input type="hidden" {...register("name")} />
        <input type="hidden" {...register("primary_color")} />
        <input type="hidden" {...register("loyalty_percentage")} />
        <input type="hidden" {...register("fixed_delivery_fee")} />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <h4 className="text-xs font-black text-gray-500 uppercase tracking-widest border-b border-gray-700 pb-2">Dados da Empresa</h4>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">CNPJ (14 dígitos)</label>
              <div className="flex gap-2">
                <input
                  {...register("cnpj")}
                  className={`flex-1 bg-gray-900 border rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all ${errors.cnpj ? 'border-red-500 bg-red-900/10' : 'border-gray-600'}`}
                  placeholder="Apenas números"
                />
                <button type="button" onClick={handleSearchCNPJ} className="bg-gray-700 hover:bg-gray-600 text-white px-3 rounded-lg">
                  {searchingCnpj ? <Loader2 className="animate-spin" size={18} /> : <Search size={18} />}
                </button>
              </div>
              {errors.cnpj && <p className="text-red-400 text-[10px] mt-1 font-bold flex items-center gap-1"><AlertCircle size={10}/> {errors.cnpj.message}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">Inscrição Estadual</label>
              <input
                {...register("inscricao_estadual")}
                className={`w-full bg-gray-900 border rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all ${errors.inscricao_estadual ? 'border-red-500 bg-red-900/10' : 'border-gray-600'}`}
                placeholder="Número ou ISENTO"
              />
              {errors.inscricao_estadual && <p className="text-red-400 text-[10px] mt-1 font-bold flex items-center gap-1"><AlertCircle size={10}/> {errors.inscricao_estadual.message}</p>}
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex justify-between items-center border-b border-gray-700 pb-2">
                <h4 className="text-xs font-black text-gray-500 uppercase tracking-widest">Conexão Focus NFe</h4>
                <a href="https://focusnfe.com.br" target="_blank" className="text-[10px] text-blue-400 flex items-center gap-1">Painel <ExternalLink size={10} /></a>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">Token de Acesso</label>
              <div className="relative">
                <input
                    {...register("fiscal_token")}
                    type="password"
                    className={`w-full bg-gray-900 border rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all pr-24 ${errors.fiscal_token ? 'border-red-500 bg-red-900/10' : 'border-gray-600'}`}
                />
                <button type="button" onClick={handleTestConnection} className="absolute right-1 top-1 bottom-1 bg-gray-800 text-xs font-bold text-gray-300 px-3 rounded-md">
                    {testingConnection ? <Loader2 className="animate-spin" size={14} /> : "Testar"}
                </button>
              </div>
              {errors.fiscal_token && <p className="text-red-400 text-[10px] mt-1 font-bold flex items-center gap-1"><AlertCircle size={10}/> {errors.fiscal_token.message}</p>}
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-300 mb-1">CSC (Token)</label>
                <input
                  {...register("csc_token")}
                  type="password"
                  className="w-full bg-gray-900 border border-gray-600 rounded-lg px-4 py-2.5 text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">CSC ID</label>
                <input
                  {...register("csc_id")}
                  className="w-full bg-gray-900 border border-gray-600 rounded-lg px-4 py-2.5 text-white text-center"
                />
              </div>
            </div>
          </div>
        </div>

        <div className="pt-4 border-t border-gray-700 flex justify-end">
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-xl font-bold flex items-center gap-2 shadow-lg active:scale-95 disabled:opacity-50"
          >
            {loading ? <Loader2 className="animate-spin" size={20} /> : <Save size={20} />}
            Salvar e Ativar
          </button>
        </div>
      </form>
    </div>
  );
}

