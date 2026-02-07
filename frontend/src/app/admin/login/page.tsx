"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { login } from "@/lib/api";
import { setTokens, setUserRole } from "@/lib/auth";
import { toast } from "sonner";
import { Loader2, Eye, EyeOff, ArrowRight, Lock, Mail } from "lucide-react";
import Logo from "@/components/ui/Logo";

export default function LoginPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData(e.currentTarget);
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;

    try {
      const data = await login({ email, password });
      
      // Persistência de Sessão
      setTokens(data.access_token, data.refresh_token);
      setUserRole(data.user_role);
      
      // Armazena slug para redirecionamentos futuros
      if (data.company_slug) {
        localStorage.setItem("mesaflow_company_slug", data.company_slug);
      }

      toast.success(`Bem-vindo, ${data.user_name}!`);
      
      // Redirecionamento Inteligente
      const target = data.user_role === 'driver' 
        ? `/admin/${data.company_slug}/driver`
        : `/admin/${data.company_slug}/dashboard`;
        
      router.push(target);
    } catch (err: any) {
      console.error(err);
      toast.error(err.message || "Falha ao entrar. Verifique suas credenciais.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black flex flex-col items-center justify-center p-4 relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-orange-600/20 rounded-full blur-[120px] pointer-events-none" />
      
      <div className="w-full max-w-md relative z-10">
        <div className="text-center mb-10">
          <div className="flex justify-center mb-6">
            <Logo size="xl" animated={true} />
          </div>
          <h1 className="text-3xl font-black text-white tracking-tight mb-2">
            Acesse seu Painel
          </h1>
          <p className="text-slate-400 text-sm">
            Gerencie sua operação com inteligência soberana.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6 bg-slate-900/50 p-8 rounded-[2rem] border border-slate-800 backdrop-blur-xl shadow-2xl">
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-widest ml-1">E-mail Corporativo</label>
            <div className="relative group">
              <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-orange-500 transition-colors" size={20} />
              <input
                name="email"
                type="email"
                required
                autoComplete="email" // 🛡️ FIX: DOM Compliance
                placeholder="admin@empresa.com"
                className="w-full bg-slate-950 border border-slate-800 rounded-2xl py-4 pl-12 pr-4 text-white focus:border-orange-500 outline-none transition-all placeholder:text-slate-700"
              />
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between items-center ml-1">
              <label className="text-xs font-bold text-slate-400 uppercase tracking-widest">Senha de Acesso</label>
              <Link 
                href="/admin/forgot-password" 
                className="text-[10px] font-bold text-orange-500 hover:text-orange-400 transition-colors uppercase tracking-wider"
              >
                Esqueceu a senha?
              </Link>
            </div>
            <div className="relative group">
              <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-orange-500 transition-colors" size={20} />
              <input
                name="password"
                type={showPassword ? "text" : "password"}
                required
                autoComplete="current-password" // 🛡️ FIX: DOM Compliance
                placeholder="••••••••"
                className="w-full bg-slate-950 border border-slate-800 rounded-2xl py-4 pl-12 pr-12 text-white focus:border-orange-500 outline-none transition-all placeholder:text-slate-700"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-white transition-colors"
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-orange-600 hover:bg-orange-700 text-white font-black py-4 rounded-2xl transition-all shadow-lg shadow-orange-900/20 flex items-center justify-center gap-2 active:scale-[0.98] disabled:opacity-70 disabled:cursor-not-allowed group"
          >
            {loading ? (
              <Loader2 className="animate-spin" />
            ) : (
              <>
                ENTRAR NO SISTEMA <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
              </>
            )}
          </button>
        </form>

        <p className="text-center mt-8 text-slate-500 text-sm">
          Ainda não tem uma conta?{" "}
          <Link href="/admin/register" className="text-white font-bold hover:underline">
            Criar agora
          </Link>
        </p>
      </div>
    </div>
  );
}
