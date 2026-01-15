"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { settingsSchema, SettingsSchema } from "@/lib/validations/settings";
import { updateCompanySettings } from "@/lib/api";
import { Company } from "@/types";
import { toast } from "sonner";
import { FileText, Save, Loader2, AlertTriangle, Info, ShieldCheck } from "lucide-react";

interface FiscalSectionProps {
  company: Company;
}

export default function FiscalSection({ company }: FiscalSectionProps) {
  const [loading, setLoading] = useState(false);
  const isSandbox = process.env.NEXT_PUBLIC_ENVIRONMENT !== 'production';

  const {
    register,
    handleSubmit,
    formState: { errors, isDirty },
  } = useForm<SettingsSchema>({
    resolver: zodResolver(settingsSchema),
    defaultValues: {
      name: company.name, // Obrigatório pelo schema, mas hidden ou readonly
      cnpj: company.cnpj || "",
      inscricao_estadual: company.inscricao_estadual || "",
      fiscal_token: company.fiscal_token || "",
      csc_token: company.csc_token || "",
      csc_id: company.csc_id || "",
    },
  });

  const onSubmit = async (data: SettingsSchema) => {
    setLoading(true);
    try {
      // Filtra apenas os campos fiscais para envio
      const payload = {
        cnpj: data.cnpj,
        inscricao_estadual: data.inscricao_estadual,
        fiscal_token: data.fiscal_token,
        csc_token: data.csc_token,
        csc_id: data.csc_id
      };
      
      await updateCompanySettings(payload);
      toast.success("Configurações fiscais atualizadas com sucesso!");
    } catch (error: any) {
      toast.error(error.message || "Erro ao salvar configurações.");
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
          <p className="text-sm text-gray-400 mt-1">
            Configure suas credenciais da <b>Focus NFe</b> para emitir notas automaticamente.
          </p>
        </div>
        {company.fiscal_token ? (
          <span className="bg-green-900/30 text-green-400 border border-green-800 px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1">
            <ShieldCheck size={14} /> Ativo
          </span>
        ) : (
          <span className="bg-gray-700 text-gray-400 px-3 py-1 rounded-full text-xs font-bold">
            Não Configurado
          </span>
        )}
      </div>

      {/* Alerta de Ambiente */}
      <div className={`p-4 rounded-xl border mb-6 flex gap-3 ${isSandbox ? 'bg-yellow-900/20 border-yellow-700/50 text-yellow-200' : 'bg-blue-900/20 border-blue-700/50 text-blue-200'}`}>
        <Info className="shrink-0 mt-0.5" size={18} />
        <div className="text-sm">
          <p className="font-bold uppercase mb-1">
            Ambiente: {isSandbox ? 'HOMOLOGAÇÃO (TESTES)' : 'PRODUÇÃO'}
          </p>
          <p className="opacity-90">
            {isSandbox 
              ? "Insira o 'Token de Homologação' da Focus NFe. As notas emitidas aqui NÃO têm validade fiscal."
              : "Insira o 'Token de Produção'. As notas emitidas terão validade jurídica."}
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Dados da Empresa */}
          <div className="space-y-4">
            <h4 className="text-sm font-bold text-gray-500 uppercase tracking-wider border-b border-gray-700 pb-2">Dados Tributários</h4>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">CNPJ (Apenas números)</label>
              <input
                {...register("cnpj")}
                className="w-full bg-gray-900 border border-gray-600 rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                placeholder="00000000000191"
                maxLength={14}
              />
              {errors.cnpj && <p className="text-red-400 text-xs mt-1">{errors.cnpj.message}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">Inscrição Estadual</label>
              <input
                {...register("inscricao_estadual")}
                className="w-full bg-gray-900 border border-gray-600 rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                placeholder="Isento ou Número"
              />
            </div>
          </div>

          {/* Credenciais Focus NFe */}
          <div className="space-y-4">
            <h4 className="text-sm font-bold text-gray-500 uppercase tracking-wider border-b border-gray-700 pb-2">Credenciais API</h4>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">Token de Acesso (API Key)</label>
              <input
                {...register("fiscal_token")}
                type="password"
                className="w-full bg-gray-900 border border-gray-600 rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all font-mono text-sm"
                placeholder="Ex: a1b2c3d4..."
              />
              <p className="text-[10px] text-gray-500 mt-1">Disponível no Painel Focus NFe {'>'} Tokens</p>
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-300 mb-1">CSC Token (Cód. Segurança)</label>
                <input
                  {...register("csc_token")}
                  type="password"
                  className="w-full bg-gray-900 border border-gray-600 rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all font-mono text-sm"
                  placeholder="Ex: AAAA-BBBB..."
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">CSC ID</label>
                <input
                  {...register("csc_id")}
                  className="w-full bg-gray-900 border border-gray-600 rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all text-center"
                  placeholder="1"
                />
              </div>
            </div>
          </div>
        </div>

        <div className="pt-4 border-t border-gray-700 flex justify-end">
          <button
            type="submit"
            disabled={loading || !isDirty}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-bold flex items-center gap-2 transition-all shadow-lg shadow-blue-900/20 disabled:opacity-50 disabled:cursor-not-allowed active:scale-95"
          >
            {loading ? <Loader2 className="animate-spin" size={20} /> : <Save size={20} />}
            Salvar Configuração Fiscal
          </button>
        </div>
      </form>
    </div>
  );
}
