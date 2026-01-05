"use client";

import { FileText, Lock, Info } from "lucide-react";
import AuthInput from "@/components/ui/AuthInput";
import { UseFormRegister, FieldErrors } from "react-hook-form";
import { SettingsSchema } from "@/lib/validations/settings";

interface FiscalSettingsProps {
  register: UseFormRegister<SettingsSchema>;
  errors: FieldErrors<SettingsSchema>;
}

export default function FiscalSettings({ register, errors }: FiscalSettingsProps) {
  return (
    <div className="space-y-8 animate-in fade-in">
      <div>
        <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <FileText size={20} className="text-blue-500" /> Dados da Empresa
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <AuthInput 
            label="CNPJ (Apenas números)" 
            icon={FileText} 
            placeholder="00000000000191" 
            error={errors.cnpj?.message} 
            {...register("cnpj")} 
          />
          <AuthInput 
            label="Inscrição Estadual" 
            icon={FileText} 
            placeholder="Isento ou Número" 
            {...register("inscricao_estadual")} 
          />
        </div>
      </div>

      <div className="border-t border-gray-700 pt-8">
        <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <Lock size={20} className="text-yellow-500" /> Credenciais de Emissão (Focus NFe)
        </h3>
        
        <div className="bg-blue-900/20 border border-blue-800 p-4 rounded-xl mb-6 flex gap-3">
          <Info className="text-blue-400 shrink-0" size={20} />
          <p className="text-xs text-blue-200 leading-relaxed">
            O MesaFlow utiliza a API da <b>Focus NFe</b> para emissão. Você precisa criar uma conta lá e obter o Token de Produção e o CSC (Código de Segurança do Contribuinte) para emitir NFC-e em ambiente real.
          </p>
        </div>

        <div className="space-y-4">
          <AuthInput 
            label="Token de Acesso (API Key)" 
            type="password"
            icon={Lock} 
            placeholder="Token da Focus NFe" 
            {...register("fiscal_token")} 
          />
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="md:col-span-2">
              <AuthInput 
                label="CSC (Token de Segurança)" 
                type="password"
                icon={Lock} 
                placeholder="Código alfanumérico do CSC" 
                {...register("csc_token")} 
              />
            </div>
            <div>
              <AuthInput 
                label="ID do CSC" 
                icon={Lock} 
                placeholder="Ex: 000001" 
                {...register("csc_id")} 
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
