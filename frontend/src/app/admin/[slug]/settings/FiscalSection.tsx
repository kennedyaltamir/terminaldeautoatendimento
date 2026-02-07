"use client";

import React from "react";
import { FileText, ShieldCheck, AlertCircle, ExternalLink } from "lucide-react";
import { UseFormRegister, FieldErrors } from "react-hook-form";
import { SettingsSchema } from "@/lib/validations/settings";
import { Company } from "@/types";

interface FiscalSectionProps {
  register: UseFormRegister<SettingsSchema>;
  errors: FieldErrors<SettingsSchema>;
  company: Company | null;
}

export default function FiscalSection({ register, errors, company }: FiscalSectionProps) {
  // 🛡️ GUARD: Prevenção de crash L2
  if (!company) return null;

  return (
    <div className="glass-card p-8 space-y-8 animate-in slide-in-from-right-4">
      <div className="flex justify-between items-start border-b border-white/5 pb-6">
        <div className="flex items-center gap-3">
          <div className="bg-blue-600/20 p-2 rounded-xl text-blue-500"><FileText size={24}/></div>
          <h3 className="text-xl font-black text-white tracking-tight">Módulo Fiscal (NFC-e)</h3>
        </div>
        <a 
          href="/docs/manuals/FISCAL_INTEGRATION_MASTER_GUIDE.md" 
          target="_blank"
          className="text-blue-400 hover:text-blue-300 text-[10px] font-black uppercase tracking-widest flex items-center gap-1"
        >
          Manual de Homologação <ExternalLink size={12} />
        </a>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="space-y-6">
          <h4 className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Dados Fiscais</h4>
          <div className="space-y-4">
            <div className="space-y-1">
              <label className="text-xs font-bold text-slate-400">CNPJ do Estabelecimento</label>
              <input
                {...register("cnpj")}
                placeholder="Apenas números"
                className="w-full bg-slate-950 border border-white/10 rounded-xl p-3 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
              />
              {errors.cnpj && <p className="text-red-500 text-[10px] font-bold">{errors.cnpj.message}</p>}
            </div>

            <div className="space-y-1">
              <label className="text-xs font-bold text-slate-400">Inscrição Estadual</label>
              <input
                {...register("inscricao_estadual")}
                className="w-full bg-slate-950 border border-white/10 rounded-xl p-3 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
              />
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <h4 className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Credenciais Focus NFe</h4>
          <div className="space-y-4">
            <div className="space-y-1">
              <label className="text-xs font-bold text-slate-400">Token de API</label>
              <input
                type="password"
                {...register("fiscal_token")}
                className="w-full bg-slate-950 border border-white/10 rounded-xl p-3 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-xs font-bold text-slate-400">CSC Token</label>
                <input
                  type="password"
                  {...register("csc_token")}
                  className="w-full bg-slate-950 border border-white/10 rounded-xl p-3 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                />
              </div>
              <div className="space-y-1">
                <label className="text-xs font-bold text-slate-400">CSC ID</label>
                <input
                  {...register("csc_id")}
                  placeholder="Ex: 000001"
                  className="w-full bg-slate-950 border border-white/10 rounded-xl p-3 text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-blue-900/20 border border-blue-800 p-4 rounded-2xl flex gap-3">
        <ShieldCheck className="text-blue-400 shrink-0" size={20} />
        <div className="text-[10px] text-blue-200 leading-relaxed uppercase font-bold tracking-wider">
          Status de Homologação: {company.name}
          <p className="mt-1 opacity-70 font-normal normal-case">O Certificado Digital A1 deve ser carregado diretamente no painel da Focus NFe. O MesaFlow não armazena arquivos .pfx.</p>
        </div>
      </div>
    </div>
  );
}
