
"use client";

/**
 * MESAFLOW SOVEREIGN IDENTITY RECOVERY (PHASE 1)
 * -----------------------------------------------------------------------------
 * VERSION: 5.0 (L8.6 Sovereign Resilience)
 * SECURITY_CONTRACT: 
 *  1. CSPRNG-based Intent IDs (No Math.random).
 *  2. Environment-specific endpoint resolution (No semantic contamination).
 *  3. Network failure prevents UX lock to allow legitimate retries.
 */

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { motion, AnimatePresence } from "framer-motion";
import { 
  ChefHat, 
  ArrowLeft, 
  Mail, 
  Loader2, 
  CheckCircle2, 
  ShieldCheck, 
  Sparkles 
} from "lucide-react";
import { Toaster, toast } from "sonner";

// Shared Infrastructure
import Logo from "@/components/ui/Logo";
import { 
  generateSovereignUUID, 
  enforceSilentHandshake, 
  trackRecoveryStage,
  getSovereignEndpoint 
} from "@/lib/security/recovery-contracts";

const forgotSchema = z.object({
  email: z.string().email("Insira um e-mail de identidade válido."),
});

type ForgotSchema = z.infer<typeof forgotSchema>;

export default function ForgotPasswordPage() {
  const [isSent, setIsSent] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);
  
  const { 
    register, 
    handleSubmit, 
    formState: { errors, isSubmitting } 
  } = useForm<ForgotSchema>({
    resolver: zodResolver(forgotSchema)
  });

  useEffect(() => {
    return () => abortControllerRef.current?.abort();
  }, []);

  const onSubmit = async (data: ForgotSchema) => {
    // 1. UX Throttle (Prevenção de cliques acidentais)
    if (sessionStorage.getItem("mf_recovery_ux_lock")) {
      toast.info("Solicitação em processamento", { description: "Aguarde um momento." });
      return enforceSilentHandshake(setIsSent);
    }

    // 2. Handshake de Intenção Forense (CSPRNG)
    const recoveryIntentId = generateSovereignUUID();
    trackRecoveryStage(recoveryIntentId, 'client_initiated');

    // 3. Preparação de Canal Seguro
    abortControllerRef.current = new AbortController();
    
    try {
      const secureEndpoint = getSovereignEndpoint(process.env.NEXT_PUBLIC_API_URL);
      
      const res = await fetch(`${secureEndpoint}/auth/forgot-password`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "X-Recovery-Intent": recoveryIntentId 
        },
        body: JSON.stringify(data),
        signal: abortControllerRef.current.signal
      });
      
      // 4. Finalização do Rito (Sucesso ou Erro de Negócio)
      trackRecoveryStage(recoveryIntentId, 'server_acknowledged');
      enforceSilentHandshake(setIsSent);
      sessionStorage.setItem("mf_recovery_ux_lock", "true");
      
      if (!res.ok) {
        console.warn(`[Forensic] Intent ${recoveryIntentId} returned status ${res.status}`);
      }
    } catch (e: any) {
      if (e.name === 'AbortError') return;
      
      trackRecoveryStage(recoveryIntentId, 'network_fail');
      
      // 🛡️ L8.6 Fix: Em erro de rede, NÃO ativamos o Silent Handshake visual.
      // Isso permite que o usuário tente novamente sem gerar um falso positivo psicológico.
      toast.error("Não foi possível concluir a solicitação.", {
        description: "Verifique sua conexão e tente novamente."
      });
      
      if (e.message.includes("CRITICAL_SECURITY_VIOLATION")) {
        console.error(`[SRE_ALERT] ${e.message}`);
      }
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-950 p-6 relative overflow-hidden">
      <meta name="referrer" content="no-referrer" />

      {/* Mesh Gradient Background */}
      <div className="absolute inset-0 z-0 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-orange-600/10 rounded-full blur-[120px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-blue-600/10 rounded-full blur-[120px]" />
      </div>

      <Toaster position="top-center" richColors theme="dark" />
      
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md z-10"
      >
        <div className="text-center mb-10">
          <Link href="/" className="inline-block hover:scale-105 transition-transform">
            <Logo size="lg" variant="light" animated={true} />
          </Link>
          <h1 className="text-3xl font-black text-white mt-8 tracking-tighter uppercase">
            Recuperar <span className="text-orange-500">Acesso</span>
          </h1>
          <p className="text-slate-400 text-sm mt-2 font-medium">
            Restaure sua soberania operacional no MesaFlow OS.
          </p>
        </div>

        <div className="bg-slate-900/50 backdrop-blur-2xl border border-white/10 p-8 md:p-10 rounded-[2.5rem] shadow-3xl relative overflow-hidden">
          <AnimatePresence mode="wait">
            {isSent ? (
              <motion.div 
                key="success"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="text-center space-y-8 py-4"
              >
                <div className="bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 p-6 rounded-3xl flex flex-col items-center gap-4">
                  <div className="bg-emerald-500/20 p-3 rounded-full">
                    <CheckCircle2 size={40} className="motion-safe:animate-pulse" />
                  </div>
                  <p className="text-sm font-bold leading-relaxed">
                    Se o e-mail informado estiver em nossa base, você receberá as instruções de reset em instantes.
                  </p>
                </div>
                
                <div className="space-y-4">
                  <Link 
                    href="/admin/login" 
                    className="block w-full bg-white text-slate-950 py-4 rounded-2xl font-black uppercase text-xs tracking-widest hover:bg-orange-500 hover:text-white transition-all active:scale-95 shadow-lg"
                  >
                    Voltar para o Login
                  </Link>
                </div>
              </motion.div>
            ) : (
              <motion.form 
                key="form"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0, x: -20 }}
                onSubmit={handleSubmit(onSubmit)} 
                className="space-y-8"
              >
                <div className="space-y-3">
                  <label className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] ml-1">
                    E-mail de Identidade
                  </label>
                  <input 
                    {...register("email")}
                    type="email"
                    placeholder="seu@email.com" 
                    className="w-full bg-slate-950/50 border border-slate-800 focus:border-orange-500 text-white h-14 rounded-2xl px-4 outline-none transition-all placeholder:text-slate-700"
                  />
                  {errors.email && (
                    <p className="text-red-500 text-[10px] font-bold uppercase ml-1">{errors.email.message}</p>
                  )}
                </div>
                
                <div className="space-y-4">
                  <button 
                    type="submit" 
                    disabled={isSubmitting}
                    className="w-full bg-orange-600 text-white py-5 rounded-2xl font-black uppercase text-xs tracking-[0.2em] hover:bg-orange-500 transition-all flex items-center justify-center gap-3 shadow-xl shadow-orange-900/20 active:scale-95 disabled:opacity-50"
                  >
                    {isSubmitting ? (
                      <Loader2 className="animate-spin" size={20} />
                    ) : (
                      <>
                        <Sparkles size={18} />
                        Enviar Link de Restauração
                      </>
                    )}
                  </button>

                  <Link 
                    href="/admin/login" 
                    className="flex items-center justify-center gap-2 text-slate-500 hover:text-white text-[10px] font-black uppercase tracking-widest transition-colors py-2"
                  >
                    <ArrowLeft size={14} /> Lembrei minha senha
                  </Link>
                </div>
              </motion.form>
            )}
          </AnimatePresence>
        </div>

        {/* Footer de Confiança */}
        <div className="mt-12 flex flex-col items-center gap-4 opacity-40 grayscale hover:grayscale-0 transition-all duration-500">
          <div className="flex items-center gap-6">
            <Link href="/trust/security" className="flex items-center gap-2 text-[10px] font-black text-white uppercase tracking-widest hover:text-orange-500 transition-colors">
              <ShieldCheck size={14} className="text-orange-500" /> AES-256 Protected
            </Link>
            <div className="w-1.5 h-1.5 bg-slate-800 rounded-full" />
            <Link href="/trust/compliance" className="text-[10px] font-black text-white uppercase tracking-widest hover:text-orange-500 transition-colors">
              ISO 27001 Compliant
            </Link>
          </div>
          <p className="text-[9px] text-slate-600 font-bold uppercase tracking-[0.3em]">
            MesaFlow Trust Center • 2026
          </p>
        </div>
      </motion.div>

      <style jsx global>{`
        @media (prefers-reduced-motion: reduce) {
          .animate-pulse, .animate-bounce, .motion-safe\\:animate-pulse {
            animation: none !important;
            transition: none !important;
          }
        }
      `}</style>
    </div>
  );
}