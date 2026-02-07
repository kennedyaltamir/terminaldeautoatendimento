
"use client";

import React from "react";
import { Monitor, Lock, ShieldAlert, Info } from "lucide-react";
import AuthInput from "@/components/ui/AuthInput";
import { Company } from "@/types";
import { UseFormRegister, FieldErrors } from "react-hook-form";
import { SettingsSchema } from "@/lib/validations/settings";

interface KioskSectionProps {
  company: Company | null;
  register: UseFormRegister<SettingsSchema>;
  errors: FieldErrors<SettingsSchema>;
}

export default function KioskSection({ company, register, errors }: KioskSectionProps) {
  // 🛡️ GUARD: Impede o crash detectado no live_error_tracker
  if (!company) return null;

  return (
    <div className="glass-card p-8 space-y-8 animate-in slide-in-from-right-4">
      <div className="flex items-center gap-3 border-b border-white/5 pb-6">
        <div className="bg-orange-600/20 p-2 rounded-xl text-orange-500"><Monitor size={24}/></div>
        <h3 className="text-xl font-black text-white tracking-tight">Modo Totem (Autoatendimento)</h3>
      </div>

      <div className="grid md:grid-cols-2 gap-10">
        <div className="space-y-4">
          <p className="text-sm text-slate-400 leading-relaxed">
            Configure a senha de segurança para sair do modo tela cheia no terminal físico.
          </p>
          <AuthInput 
            label="Nova Senha do Totem" 
            type="password" 
            icon={Lock} 
            placeholder="Mínimo 4 dígitos"
            {...register("kiosk_password")} 
            error={errors.kiosk_password?.message}
          />
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${company.kiosk_password_set ? 'bg-green-500' : 'bg-yellow-500'}`} />
            <span className="text-[10px] font-black uppercase text-slate-500 tracking-widest">
              {company.kiosk_password_set ? "Senha Customizada Ativa" : "Usando Senha Padrão (123456)"}
            </span>
          </div>
        </div>

        <div className="bg-slate-950/50 p-6 rounded-3xl border border-white/5 space-y-4">
          <h4 className="text-xs font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
            <ShieldAlert size={14} className="text-orange-500" /> Segurança de Perímetro
          </h4>
          <ul className="space-y-3">
            {[
              "Bloqueio de gestos do sistema",
              "Prevenção de burn-in de tela",
              "Reset automático por inatividade",
              "Trap-mode em caso de fuga"
            ].map((item, i) => (
              <li key={i} className="flex items-center gap-2 text-xs text-slate-400">
                <div className="w-1 h-1 bg-orange-500 rounded-full" />
                {item}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
