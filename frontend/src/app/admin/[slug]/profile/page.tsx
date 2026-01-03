"use client";

import { useEffect, useState } from "react";
import { getCompanySettings, updatePassword } from "@/lib/api";
import { Save, Loader2, User, Lock, Mail } from "lucide-react";

export default function ProfilePage() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [profile, setProfile] = useState({ name: "", owner_email: "" });
  const [passForm, setPassForm] = useState({ current_password: "", new_password: "", confirm_password: "" });

  useEffect(() => {
    getCompanySettings()
      .then((data) => setProfile({ name: data.name, owner_email: data.owner_email }))
      .catch(() => alert("Erro ao carregar perfil"))
      .finally(() => setLoading(false));
  }, []);

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    if (passForm.new_password !== passForm.confirm_password) {
      return alert("A nova senha e a confirmação não coincidem");
    }
    setSaving(true);
    try {
      await updatePassword({
        current_password: passForm.current_password,
        new_password: passForm.new_password
      });
      alert("Senha atualizada com sucesso!");
      setPassForm({ current_password: "", new_password: "", confirm_password: "" });
    } catch (error: any) {
      alert(error.message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="text-center py-20">Carregando...</div>;

  return (
    <div className="max-w-2xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold text-white">Meu Perfil</h1>
      <div className="bg-gray-800 rounded-xl border border-gray-700 p-6 space-y-6">
        <div className="flex items-center gap-4 border-b border-gray-700 pb-6">
          <div className="w-16 h-16 bg-orange-600 rounded-full flex items-center justify-center text-white">
            <User size={32} />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white">{profile.name}</h2>
            <p className="text-gray-400 flex items-center gap-2 text-sm">
              <Mail size={14} /> {profile.owner_email}
            </p>
          </div>
        </div>
        <form onSubmit={handlePasswordChange} className="space-y-4">
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <Lock size={18} className="text-orange-500" /> Alterar Senha
          </h3>
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">Senha Atual</label>
            <input type="password" required className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none" value={passForm.current_password} onChange={e => setPassForm({...passForm, current_password: e.target.value})} />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-1">Nova Senha</label>
              <input type="password" required className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none" value={passForm.new_password} onChange={e => setPassForm({...passForm, new_password: e.target.value})} />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-1">Confirmar Nova Senha</label>
              <input type="password" required className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none" value={passForm.confirm_password} onChange={e => setPassForm({...passForm, confirm_password: e.target.value})} />
            </div>
          </div>
          <button type="submit" disabled={saving} className="w-full bg-orange-600 hover:bg-orange-700 text-white font-bold py-3 rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-50">
            {saving ? <Loader2 className="animate-spin" /> : <Save size={20} />}
            Atualizar Senha
          </button>
        </form>
      </div>
    </div>
  );
}