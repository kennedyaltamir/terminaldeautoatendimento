"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ShieldAlert, Key, Mail, ArrowRight, Loader2 } from "lucide-react";
import { toast, Toaster } from "sonner";
import { setTokens, setUserRole } from "@/lib/auth";
import AuthInput from "@/components/ui/AuthInput";

export default function SupportPage() {
  const [secret, setSecret] = useState("");
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleImpersonate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!secret || !email) return toast.error("Preencha todos os campos.");

    setLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/impersonate`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "X-Super-Secret": secret 
        },
        body: JSON.stringify({ target_email: email })
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Falha no acesso suporte.");
      }

      const data = await res.json();
      setTokens(data.access_token, data.refresh_token);
      setUserRole(data.user_role);
      
      toast.success("Acesso suporte concedido!");
      setTimeout(() => {
        router.push(`/admin/${data.company_slug}/dashboard`);
      }, 1000);

    } catch (e: any) {
      toast.error(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center p-6 font-sans">
      <Toaster position="top-center" richColors />
      
      <div className="w-full max-w-md bg-gray-900 border border-red-900/30 rounded-3xl p-8 shadow-2xl relative overflow-hidden">
        {/* Background Glow */}
        <div className="absolute top-0 right-0 w-32 h-32 bg-red-600/10 rounded-full blur-3xl -mr-10 -mt-10"></div>

        <div className="text-center mb-8">
          <div className="bg-red-600/20 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-red-600/30">
            <ShieldAlert size={32} className="text-red-500" />
          </div>
          <h1 className="text-2xl font-black text-white tracking-tight">God Mode</h1>
          <p className="text-gray-500 text-sm mt-2">Acesso administrativo de suporte técnico.</p>
        </div>

        <form onSubmit={handleImpersonate} className="space-y-6">
          <AuthInput 
            label="Chave Mestra" 
            type="password" 
            icon={Key} 
            placeholder="SUPER_ADMIN_SECRET" 
            value={secret}
            onChange={e => setSecret(e.target.value)}
          />

          <AuthInput 
            label="E-mail do Cliente" 
            type="email" 
            icon={Mail} 
            placeholder="cliente@loja.com" 
            value={email}
            onChange={e => setEmail(e.target.value)}
          />

          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-4 rounded-xl flex items-center justify-center gap-2 transition-all shadow-lg shadow-red-900/20 disabled:opacity-50"
          >
            {loading ? <Loader2 className="animate-spin" /> : <>Acessar Painel <ArrowRight size={20} /></>}
          </button>
        </form>

        <p className="text-[10px] text-gray-600 mt-8 text-center uppercase font-bold tracking-widest">
          Acesso monitorado e auditado
        </p>
      </div>
    </div>
  );
}
