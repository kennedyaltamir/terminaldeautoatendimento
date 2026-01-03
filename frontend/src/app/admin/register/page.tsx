"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { register } from "@/lib/api";
import { setToken } from "@/lib/auth";
import { ChefHat, ArrowRight, Loader2, Mail, Lock, Store, Link as LinkIcon, AlertCircle, CheckCircle2 } from "lucide-react";
import Link from "next/link";

export default function RegisterPage() {
  const [form, setForm] = useState({
    company_name: "",
    company_slug: "",
    owner_email: "",
    password: ""
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  // Auto-gerar slug
  useEffect(() => {
    const slug = form.company_name
      .toLowerCase()
      .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
      .replace(/[^a-z0-9]/g, "-")
      .replace(/-+/g, "-")
      .replace(/^-|-$/g, "");
    
    setForm(prev => ({ ...prev, company_slug: slug }));
  }, [form.company_name]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await register(form);
      setToken(data.access_token);
      router.push(`/admin/${form.company_slug}/dashboard`);
    } catch (err: any) {
      setError(err.message || "Erro ao criar conta. Tente outro email ou slug.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex bg-white dark:bg-gray-900 font-sans overflow-hidden">
      
      {/* LADO ESQUERDO - FORMULÁRIO */}
      <div className="w-full lg:w-1/2 flex flex-col justify-center px-8 sm:px-12 lg:px-24 py-12 animate-slide-in-left relative z-10">
        <div className="mb-8">
          <Link href="/" className="flex items-center gap-2 mb-8 group w-fit">
            <div className="bg-orange-600 p-2 rounded-xl shadow-lg shadow-orange-500/20 group-hover:scale-110 transition-transform">
              <ChefHat className="text-white w-6 h-6" />
            </div>
            <span className="text-2xl font-bold text-gray-900 dark:text-white tracking-tight">MesaFlow</span>
          </Link>
          <h1 className="text-4xl font-black text-gray-900 dark:text-white mb-2 tracking-tight">Crie sua conta grátis</h1>
          <p className="text-gray-500 dark:text-gray-400 text-lg">Comece a vender em minutos. Sem cartão de crédito.</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 text-sm p-4 rounded-xl flex items-center gap-3 animate-fade-in">
              <AlertCircle size={20} />
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-1.5">Nome do Restaurante</label>
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Store className="h-5 w-5 text-gray-400 group-focus-within:text-orange-500 transition-colors" />
                </div>
                <input
                  type="text"
                  required
                  value={form.company_name}
                  onChange={(e) => setForm({...form, company_name: e.target.value})}
                  className="w-full pl-10 pr-4 py-3 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                  placeholder="Ex: Pizzaria do João"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-1.5">Link do Cardápio (Slug)</label>
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <LinkIcon className="h-5 w-5 text-gray-400 group-focus-within:text-orange-500 transition-colors" />
                </div>
                <div className="flex items-center w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl focus-within:ring-2 focus-within:ring-orange-500 focus-within:border-transparent transition-all overflow-hidden">
                  <span className="pl-10 pr-1 text-gray-500 text-sm font-medium">mesaflow.com/</span>
                  <input
                    type="text"
                    required
                    value={form.company_slug}
                    onChange={(e) => setForm({...form, company_slug: e.target.value})}
                    className="flex-1 py-3 bg-transparent text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none font-bold"
                    placeholder="pizzaria-joao"
                  />
                </div>
              </div>
              {form.company_slug && (
                <p className="text-xs text-green-600 mt-1 flex items-center gap-1 animate-fade-in">
                  <CheckCircle2 size={12} /> Link disponível: mesaflow.com/{form.company_slug}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-1.5">Seu Email</label>
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-gray-400 group-focus-within:text-orange-500 transition-colors" />
                </div>
                <input
                  type="email"
                  required
                  value={form.owner_email}
                  onChange={(e) => setForm({...form, owner_email: e.target.value})}
                  className="w-full pl-10 pr-4 py-3 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                  placeholder="admin@restaurante.com"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-1.5">Senha</label>
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-400 group-focus-within:text-orange-500 transition-colors" />
                </div>
                <input
                  type="password"
                  required
                  value={form.password}
                  onChange={(e) => setForm({...form, password: e.target.value})}
                  className="w-full pl-10 pr-4 py-3 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                  placeholder="Mínimo 6 caracteres"
                />
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-orange-600 hover:bg-orange-700 text-white font-bold py-3.5 rounded-xl transition-all shadow-lg shadow-orange-500/30 hover:shadow-orange-500/50 hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loading ? <Loader2 className="animate-spin" /> : <>Criar Conta Grátis <ArrowRight size={20} /></>}
          </button>
        </form>

        <div className="mt-8 text-center">
          <p className="text-gray-500 dark:text-gray-400">
            Já tem uma conta?{" "}
            <Link href="/admin/login" className="text-orange-600 font-bold hover:underline">
              Fazer Login
            </Link>
          </p>
        </div>
      </div>

      {/* LADO DIREITO - IMAGEM/DEPOIMENTO */}
      <div className="hidden lg:flex w-1/2 bg-gray-900 relative overflow-hidden animate-slide-in-right">
        <div className="absolute inset-0 bg-[url('https://images.pexels.com/photos/260922/pexels-photo-260922.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1')] bg-cover bg-center opacity-40"></div>
        <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-gray-900/40 to-transparent"></div>
        
        <div className="relative z-10 flex flex-col justify-end p-16 h-full text-white">
          <div className="mb-6">
            <h2 className="text-3xl font-bold mb-4">Comece a revolução no seu atendimento.</h2>
            <ul className="space-y-3 text-gray-300">
              <li className="flex items-center gap-2"><CheckCircle2 className="text-green-500" size={20}/> Cardápio Digital Ilimitado</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="text-green-500" size={20}/> KDS de Cozinha em Tempo Real</li>
              <li className="flex items-center gap-2"><CheckCircle2 className="text-green-500" size={20}/> Pagamentos via Pix Automático</li>
            </ul>
          </div>
        </div>
      </div>

    </div>
  );
}