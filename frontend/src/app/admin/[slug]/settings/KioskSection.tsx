"use client";

import { useState } from "react";
import { Monitor, Lock, Save, Loader2, CheckCircle2, AlertTriangle } from "lucide-react";
import { toast } from "sonner";
import { Company } from "@/types";
import { updateCompanySettings } from "@/lib/api";

export default function KioskSection({ company }: { company: Company }) {
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [isSet, setIsSet] = useState(company.kiosk_password_set || false);

  const handleSave = async () => {
    if (!password) return;
    if (password.length < 4) {
      toast.error("A senha deve ter no mínimo 4 dígitos.");
      return;
    }

    setLoading(true);
    try {
      await updateCompanySettings({ kiosk_password: password });
      toast.success("Senha do Totem atualizada!");
      setPassword("");
      setIsSet(true);
    } catch (e) {
      toast.error("Erro ao salvar senha.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-xl p-6 animate-in fade-in">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Monitor className="text-purple-500" /> Modo Totem (Kiosk)
          </h3>
          <p className="text-sm text-gray-400 mt-1">
            Configure a segurança para terminais de autoatendimento.
          </p>
        </div>
        {isSet ? (
          <span className="bg-green-900/30 text-green-400 px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1 border border-green-800">
            <CheckCircle2 size={12} /> Senha Ativa
          </span>
        ) : (
          <span className="bg-yellow-900/30 text-yellow-400 px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1 border border-yellow-800">
            <AlertTriangle size={12} /> Usando Padrão (123456)
          </span>
        )}
      </div>

      <div className="bg-gray-900 p-5 rounded-xl border border-gray-700 space-y-4">
        <div>
          <label className="block text-sm font-bold text-gray-300 mb-2">
            Senha Administrativa de Saída
          </label>
          <div className="flex gap-3">
            <div className="relative flex-1">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={18} />
              <input 
                type="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder={isSet ? "•••••••• (Redefinir)" : "Definir nova senha"}
                className="w-full bg-gray-800 border border-gray-600 rounded-xl pl-10 pr-4 py-3 text-white focus:ring-2 focus:ring-purple-500 outline-none transition-all"
              />
            </div>
            <button 
              onClick={handleSave}
              disabled={loading || !password}
              className="bg-purple-600 hover:bg-purple-700 text-white px-6 rounded-xl font-bold transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {loading ? <Loader2 className="animate-spin" size={18} /> : <Save size={18} />}
              Salvar
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Esta senha é exigida para sair do modo tela cheia no totem.
          </p>
        </div>
      </div>
    </div>
  );
}

