"use client";
import { useEffect, useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { getCompanySettings } from "@/lib/api";
import { 
  Check, Zap, Shield, Star, ArrowRight, Loader2, 
  AlertCircle, HelpCircle, CreditCard, History, ShieldCheck 
} from "lucide-react";
import { toast, Toaster } from "sonner";
import { Company } from "@/types";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

function BillingContent() {
  const [company, setCompany] = useState<Company | null>(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const searchParams = useSearchParams();
  const router = useRouter();

  useEffect(() => {
    const status = searchParams.get("billing");
    if (status === "success") {
      toast.success("Assinatura ativada com sucesso! 🎉", {
        description: "Seu restaurante agora é Pro. Aproveite os recursos ilimitados."
      });
      router.replace(window.location.pathname);
    } else if (status === "cancel") {
      toast.error("O processo de pagamento foi interrompido.");
    }
    getCompanySettings()
      .then(setCompany)
      .catch(() => toast.error("Erro ao carregar dados de faturamento"))
      .finally(() => setLoading(false));
  }, [searchParams, router]);

  const handleUpgrade = async () => {
    setProcessing(true);
    try {
      const token = localStorage.getItem("mesaflow_access_token");
      const res = await fetch(`${API_URL}/admin/billing/upgrade`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) throw new Error("Falha ao iniciar checkout");
      const data = await res.json();
      if (data.url) window.location.href = data.url;
    } catch (e) {
      toast.error("Erro ao conectar com o provedor de pagamentos.");
    } finally {
      setProcessing(false);
    }
  };

  const handlePortal = async () => {
    setProcessing(true);
    try {
      const token = localStorage.getItem("mesaflow_access_token");
      const res = await fetch(`${API_URL}/admin/billing/portal`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) throw new Error("Falha ao abrir portal");
      const data = await res.json();
      if (data.url) window.location.href = data.url;
    } catch (e) {
      toast.error("Erro ao abrir portal de faturamento.");
    } finally {
      setProcessing(false);
    }
  };

  if (loading) return (
    <div className="flex h-[60vh] flex-col items-center justify-center gap-4">
      <Loader2 className="animate-spin text-orange-500" size={40} />
      <p className="text-slate-500 font-bold animate-pulse">Carregando planos...</p>
    </div>
  );

  if (!company) return null;

  const isPro = company.plan_tier === "pro" || company.plan_tier === "enterprise";

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-6xl mx-auto space-y-12 pb-20"
    >
      <Toaster position="top-center" richColors />
      
      <div className="text-center space-y-4">
        <h1 className="text-4xl md:text-5xl font-black text-white tracking-tight">
          Planos & <span className="text-orange-500">Crescimento</span>
        </h1>
        <p className="text-slate-400 text-lg max-w-2xl mx-auto">
          Escolha a infraestrutura ideal para o volume da sua operação.
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-8 items-stretch">
        {/* PLANO START */}
        <div className={cn(
          "bg-slate-900/50 border-2 rounded-[2.5rem] p-10 flex flex-col transition-all",
          !isPro ? "border-slate-700 shadow-xl" : "border-slate-800 opacity-50 grayscale"
        )}>
          <div className="flex justify-between items-start mb-8">
            <div>
              <h3 className="text-2xl font-black text-white">Start</h3>
              <p className="text-slate-500 text-sm font-bold uppercase tracking-widest mt-1">Para validação</p>
            </div>
            <div className="bg-slate-800 p-3 rounded-2xl text-slate-400">
              <Shield size={24} />
            </div>
          </div>
          <div className="mb-10">
            <span className="text-5xl font-black text-white">Grátis</span>
            <p className="text-slate-500 text-sm mt-2">Ideal para pequenos testes ou MVP.</p>
          </div>
          <ul className="space-y-5 mb-12 flex-1">
            {[
              { text: "Até 50 pedidos/mês", check: true },
              { text: "Cardápio Digital Básico", check: true },
              { text: "1 Usuário Administrativo", check: true },
              { text: "Sem KDS de Cozinha", check: false },
              { text: "Sem Gestão de Estoque", check: false },
            ].map((item, i) => (
              <li key={i} className={cn("flex items-center gap-3 text-sm font-bold", item.check ? "text-slate-300" : "text-slate-600")}>
                {item.check ? <Check size={18} className="text-emerald-500" /> : <AlertCircle size={18} />}
                {item.text}
              </li>
            ))}
          </ul>
          <button 
            type="button"
            onClick={() => toast.info("Você já está no plano Start.")}
            className="w-full py-4 rounded-2xl border-2 border-slate-700 text-slate-500 font-black uppercase tracking-widest text-xs cursor-default"
          >
            {isPro ? "Plano Anterior" : "Plano Atual"}
          </button>
        </div>

        {/* PLANO PRO */}
        <div className={cn(
          "relative bg-slate-900 border-2 rounded-[2.5rem] p-10 flex flex-col transition-all shadow-2xl",
          isPro ? "border-emerald-500 shadow-emerald-900/20" : "border-orange-500 shadow-orange-900/20 scale-[1.02]"
        )}>
          {!isPro && (
            <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-orange-600 text-white text-[10px] font-black px-6 py-2 rounded-full shadow-xl tracking-[0.2em] uppercase">
              Recomendado
            </div>
          )}
          <div className="flex justify-between items-start mb-8">
            <div>
              <h3 className="text-2xl font-black text-white flex items-center gap-2">
                Pro <Zap className="text-orange-500 fill-orange-500" size={20} />
              </h3>
              <p className="text-orange-500/70 text-sm font-bold uppercase tracking-widest mt-1">Operação Real</p>
            </div>
            <div className={cn("p-3 rounded-2xl", isPro ? "bg-emerald-500/10 text-emerald-500" : "bg-orange-500/10 text-orange-500")}>
              <Star size={24} className="fill-current" />
            </div>
          </div>
          <div className="mb-10">
            <div className="flex items-baseline gap-1">
              <span className="text-5xl font-black text-white tabular-nums">R$ 149</span>
              <span className="text-slate-500 font-bold">/mês</span>
            </div>
            <p className="text-slate-400 text-sm mt-2">Tudo o que você precisa para escalar.</p>
          </div>
          <ul className="space-y-5 mb-12 flex-1">
            {[
              "Pedidos Ilimitados",
              "KDS (Monitor de Cozinha)",
              "Gestão de Estoque & Ficha Técnica",
              "App do Garçom & Logística",
              "Fidelidade & Cashback Automático",
              "Suporte Prioritário"
            ].map((item, i) => (
              <li key={i} className="flex items-center gap-3 text-sm font-bold text-white">
                <Check size={18} className="text-emerald-500" />
                {item}
              </li>
            ))}
          </ul>
          <button 
            type="button"
            onClick={isPro ? handlePortal : handleUpgrade}
            disabled={processing}
            className={cn(
              "w-full py-5 rounded-2xl font-black uppercase tracking-widest text-xs transition-all flex items-center justify-center gap-3 shadow-xl active:scale-95 disabled:opacity-50",
              isPro ? "bg-slate-800 text-white hover:bg-slate-700" : "bg-orange-600 text-white hover:bg-orange-700 shadow-orange-900/20"
            )}
          >
            {processing ? <Loader2 className="animate-spin" /> : isPro ? <><CreditCard size={18}/> Gerenciar Assinatura</> : <>Assinar Agora <ArrowRight size={18} /></>}
          </button>
        </div>
      </div>

      {/* FAQ SECTION */}
      <div className="pt-12 border-t border-slate-800">
        <div className="flex items-center gap-3 mb-10">
          <HelpCircle className="text-orange-500" size={28} />
          <h2 className="text-2xl font-black text-white tracking-tight">Dúvidas Frequentes</h2>
        </div>
        <div className="grid md:grid-cols-3 gap-8">
          {[
            { q: "Preciso de cartão de crédito?", a: "Sim, para o plano Pro. O faturamento é recorrente e você pode cancelar a qualquer momento sem multas." },
            { q: "Como funciona o suporte?", a: "Clientes Pro têm acesso a um canal exclusivo no WhatsApp com tempo de resposta inferior a 15 minutos em horário comercial." },
            { q: "Posso mudar de plano?", a: "Sim. O upgrade é imediato. O downgrade para o plano Start ocorre no final do ciclo de faturamento atual." }
          ].map((item, i) => (
            <div key={i} className="bg-slate-900/30 border border-slate-800 p-6 rounded-3xl space-y-3">
              <h4 className="text-white font-bold text-sm">{item.q}</h4>
              <p className="text-slate-500 text-xs leading-relaxed font-medium">{item.a}</p>
            </div>
          ))}
        </div>
      </div>

      {/* FOOTER INFO */}
      <div className="flex flex-col md:flex-row justify-between items-center gap-6 px-8 py-6 bg-slate-900/50 rounded-3xl border border-slate-800">
        <div className="flex items-center gap-4">
          <div className="bg-emerald-500/10 p-2 rounded-xl text-emerald-500">
            <ShieldCheck size={20} />
          </div>
          <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">
            Pagamentos processados com segurança via Stripe®
          </p>
        </div>
        <button 
          type="button" 
          onClick={() => toast.info("Histórico de faturas disponível no Portal do Cliente.")}
          className="text-[10px] font-black text-orange-500 uppercase tracking-widest hover:underline flex items-center gap-2"
        >
          <History size={14} /> Ver Histórico de Faturas
        </button>
      </div>
    </motion.div>
  );
}

export default function BillingPage() {
  return (
    <Suspense fallback={
      <div className="flex h-screen items-center justify-center bg-slate-950">
        <Loader2 className="animate-spin text-orange-500" size={40} />
      </div>
    }>
      <BillingContent />
    </Suspense>
  );
}
