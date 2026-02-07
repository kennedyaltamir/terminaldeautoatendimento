"use client";

import { useEffect, useState } from "react";
import { getCompanySettings, updatePassword } from "@/lib/api";
import { Save, Loader2, User, Lock, Mail, ShieldCheck } from "lucide-react";
import { toast, Toaster } from "sonner";

export default function ProfilePage() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [profile, setProfile] = useState({ name: "", owner_email: "" });
  const [passForm, setPassForm] = useState({ current_password: "", new_password: "", confirm_password: "" });

  useEffect(() => {
    getCompanySettings()
      .then((data) => setProfile({ name: data.name, owner_email: data.owner_email || "" }))
      .catch(() => toast.error("Erro ao carregar perfil"))
      .finally(() => setLoading(false));
  }, []);

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    if (passForm.new_password !== passForm.confirm_password) {
      return toast.error("A nova senha e a confirmação não coincidem");
    }
    setSaving(true);
    try {
      await updatePassword({
        current_password: passForm.current_password,
        new_password: passForm.new_password
      });
      toast.success("Senha atualizada com sucesso!");
      setPassForm({ current_password: "", new_password: "", confirm_password: "" });
    } catch (error: any) {
      toast.error(error.message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="text-center py-20 text-gray-500">Carregando...</div>;

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-20">
      <Toaster position="top-right" richColors />
      <div>
        <h1 className="text-3xl font-bold text-white">Meu Perfil</h1>
        <p className="text-gray-400 text-sm mt-1">Gerencie suas credenciais de acesso.</p>
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        {/* Cartão de Identificação */}
        <div className="md:col-span-1">
          <div className="bg-gray-800 rounded-2xl border border-gray-700 p-6 text-center shadow-xl">
            <div className="w-24 h-24 bg-gradient-to-br from-orange-500 to-red-600 rounded-full flex items-center justify-center text-white mx-auto mb-4 shadow-lg">
              <User size={40} />
            </div>
            <h2 className="text-xl font-bold text-white mb-1">{profile.name}</h2>
            <div className="inline-flex items-center gap-2 bg-gray-900 px-3 py-1 rounded-full border border-gray-700">
              <Mail size={12} className="text-gray-400" />
              <span className="text-xs text-gray-300">{profile.owner_email}</span>
            </div>
            <div className="mt-6 pt-6 border-t border-gray-700">
              <div className="flex items-center justify-center gap-2 text-green-400 text-sm font-bold">
                <ShieldCheck size={16} /> Conta Segura
              </div>
            </div>
          </div>
        </div>

        {/* Formulário de Senha */}
        <div className="md:col-span-2">
          <div className="bg-gray-800 rounded-2xl border border-gray-700 p-8 shadow-xl">
            <h3 className="text-lg font-bold text-white flex items-center gap-2 mb-6">
              <Lock size={20} className="text-orange-500" /> Alterar Senha
            </h3>
            <form onSubmit={handlePasswordChange} className="space-y-5">
              <div>
                <label className="block text-sm font-bold text-gray-400 mb-1.5">Senha Atual</label>
                <input 
                  type="password" 
                  required 
                  className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none transition-all" 
                  value={passForm.current_password} 
                  onChange={e => setPassForm({...passForm, current_password: e.target.value})}
                  autoComplete="current-password" // 🛡️ FIX: Acessibilidade e Padrão Web
                />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                <div>
                  <label className="block text-sm font-bold text-gray-400 mb-1.5">Nova Senha</label>
                  <input 
                    type="password" 
                    required 
                    className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none transition-all" 
                    value={passForm.new_password} 
                    onChange={e => setPassForm({...passForm, new_password: e.target.value})}
                    autoComplete="new-password" // 🛡️ FIX: Acessibilidade e Padrão Web
                  />
                </div>
                <div>
                  <label className="block text-sm font-bold text-gray-400 mb-1.5">Confirmar Nova Senha</label>
                  <input 
                    type="password" 
                    required 
                    className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none transition-all" 
                    value={passForm.confirm_password} 
                    onChange={e => setPassForm({...passForm, confirm_password: e.target.value})}
                    autoComplete="new-password" // 🛡️ FIX: Acessibilidade e Padrão Web
                  />
                </div>
              </div>
              <div className="pt-4">
                <button 
                  type="submit" 
                  disabled={saving} 
                  className="w-full bg-orange-600 hover:bg-orange-700 text-white font-bold py-3.5 rounded-xl flex items-center justify-center gap-2 transition-all shadow-lg shadow-orange-900/20 disabled:opacity-50 disabled:cursor-not-allowed active:scale-95"
                >
                  {saving ? <Loader2 className="animate-spin" /> : <Save size={20} />}
                  Atualizar Senha
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
