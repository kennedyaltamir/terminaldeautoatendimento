/**
 * DOMAIN: FRONTEND
 * FILE: src/app/admin/support/page.tsx
 * OBJECTIVE: Portal de Suporte Técnico (God Mode) - Versão Black Box.
 * DESCRIPTION: Inclui feedback visual de cooldown e integração com auditoria offline.
 */

"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { ShieldAlert, Key, Mail, ArrowRight, Loader2, Lock, CheckCircle2, WifiOff, RefreshCw, Timer } from "lucide-react";
import { Toaster } from "sonner";
import { motion, AnimatePresence, Variants } from "framer-motion";
import AuthInput from "@/components/ui/AuthInput";
import { useImpersonate } from "@/hooks/useImpersonate";
import { cn } from "@/lib/utils";

const supportSchema = z.object({
  secret: z.string().min(1, "Chave obrigatória").max(64),
  email: z.string().email("E-mail inválido")
});

type SupportSchema = z.infer<typeof supportSchema>;

const shakeVariants: Variants = {
  idle: { x: 0 },
  shake: {
    x: [0, -15, 15, -10, 10, -5, 5, 0],
    transition: { duration: 0.5, ease: "easeInOut" }
  }
};

const KEY_TARGET = "mf_god_target";
const KEY_END_TIME = "mf_god_endtime";
const COUNTDOWN_DURATION = 3500;

export default function SupportPage() {
  const { impersonate, loading, isSuccess, setIsSuccess, networkError, cooldown } = useImpersonate();
  const router = useRouter();
  
  const [shakeState, setShakeState] = useState("idle");
  const [countdown, setCountdown] = useState(3);
  const [targetSlug, setTargetSlug] = useState("");

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
    getValues
  } = useForm<SupportSchema>({
    resolver: zodResolver(supportSchema),
    mode: "onChange"
  });

  // Recuperação de Estado
  useEffect(() => {
    const savedTarget = sessionStorage.getItem(KEY_TARGET);
    const savedEndTime = sessionStorage.getItem(KEY_END_TIME);

    if (savedTarget && savedEndTime) {
      const endTime = parseInt(savedEndTime, 10);
      const now = Date.now();
      const remaining = Math.ceil((endTime - now) / 1000);

      if (remaining > 0) {
        setTargetSlug(savedTarget);
        setIsSuccess(true);
        setCountdown(remaining);
        router.prefetch(`/admin/${savedTarget}/dashboard`);
      } else {
        sessionStorage.removeItem(KEY_TARGET);
        sessionStorage.removeItem(KEY_END_TIME);
      }
    }
  }, [setIsSuccess, router]);

  // Countdown
  useEffect(() => {
    if (isSuccess && targetSlug) {
      const timer = setInterval(() => {
        const endTime = parseInt(sessionStorage.getItem(KEY_END_TIME) || "0", 10);
        const remaining = Math.ceil((endTime - Date.now()) / 1000);

        if (remaining <= 0) {
          clearInterval(timer);
          sessionStorage.removeItem(KEY_TARGET);
          sessionStorage.removeItem(KEY_END_TIME);
          router.push(`/admin/${targetSlug}/dashboard`);
        } else {
          setCountdown(remaining);
        }
      }, 200);
      return () => clearInterval(timer);
    }
  }, [isSuccess, targetSlug, router]);

  const onSubmit = async (data: SupportSchema) => {
    setShakeState("idle");
    try {
      const slug = await impersonate(data.secret, data.email);
      if (slug) {
        setTargetSlug(slug);
        const endTime = Date.now() + COUNTDOWN_DURATION;
        sessionStorage.setItem(KEY_TARGET, slug);
        sessionStorage.setItem(KEY_END_TIME, endTime.toString());
        router.prefetch(`/admin/${slug}/dashboard`);
      }
    } catch {
      setShakeState("shake");
      setTimeout(() => setShakeState("idle"), 500);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4 sm:p-6 font-sans selection:bg-red-500/30 selection:text-red-200">
      <Toaster position="top-center" richColors theme="dark" />
      
      <div className="w-full max-w-md bg-slate-900 border border-red-900/30 rounded-[2.5rem] p-8 shadow-2xl relative overflow-hidden group">
        <div className={cn(
          "absolute top-0 right-0 w-64 h-64 rounded-full blur-[80px] -mr-20 -mt-20 pointer-events-none transition-colors duration-1000",
          isSuccess ? "bg-green-500/10" : "bg-red-600/10"
        )} />

        <AnimatePresence mode="wait">
          {!isSuccess ? (
            <motion.div
              key="form"
              variants={shakeVariants}
              animate={shakeState}
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95, filter: "blur(10px)" }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
            >
              <div className="text-center mb-10 relative z-10">
                <div className="bg-red-950/50 w-20 h-20 rounded-3xl flex items-center justify-center mx-auto mb-6 border border-red-500/20 shadow-lg shadow-red-900/20">
                  <ShieldAlert size={40} className="text-red-500" />
                </div>
                <h1 className="text-3xl font-black text-white tracking-tight mb-2">God Mode</h1>
                <p className="text-slate-400 text-sm font-medium">Acesso administrativo de suporte.</p>
              </div>

              {networkError ? (
                <motion.div 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-red-950/30 border border-red-900/50 rounded-2xl p-6 text-center mb-6"
                >
                  <WifiOff className="mx-auto text-red-400 mb-3" size={32} />
                  <h3 className="text-white font-bold mb-1">Sem Conexão</h3>
                  <p className="text-red-200/70 text-xs mb-4">Não foi possível validar as credenciais.</p>
                  <button 
                    onClick={() => onSubmit(getValues())}
                    className="bg-red-600 hover:bg-red-500 text-white px-6 py-2 rounded-xl text-xs font-bold flex items-center gap-2 mx-auto transition-colors"
                  >
                    <RefreshCw size={14} /> Tentar Novamente
                  </button>
                </motion.div>
              ) : (
                <form onSubmit={handleSubmit(onSubmit)} className="space-y-5 relative z-10">
                  <fieldset disabled={loading || cooldown > 0} className="space-y-4 group-disabled:opacity-50 transition-opacity">
                    <AuthInput 
                      label="Chave Mestra" 
                      type="password" 
                      icon={Key} 
                      placeholder="SUPER_ADMIN_SECRET" 
                      error={errors.secret?.message}
                      {...register("secret")}
                      className="border-red-900/30 focus:border-red-500 focus:ring-red-500/20 transition-all"
                      autoComplete="new-password"
                      spellCheck={false}
                      aria-invalid={!!errors.secret}
                    />

                    <AuthInput 
                      label="E-mail do Cliente" 
                      type="email" 
                      icon={Mail} 
                      placeholder="cliente@loja.com" 
                      error={errors.email?.message}
                      {...register("email")}
                      className="border-red-900/30 focus:border-red-500 focus:ring-red-500/20 transition-all"
                      aria-invalid={!!errors.email}
                    />
                  </fieldset>

                  <button 
                    type="submit" 
                    disabled={loading || !isValid || cooldown > 0}
                    className={cn(
                      "w-full bg-red-600 hover:bg-red-500 text-white font-black py-4 rounded-xl flex items-center justify-center gap-3 transition-all shadow-lg shadow-red-900/20 uppercase tracking-widest text-xs focus-visible:ring-4 focus-visible:ring-red-500/50 outline-none",
                      "disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none active:scale-[0.98]"
                    )}
                  >
                    {loading ? (
                      <>
                        <Loader2 className="animate-spin" size={18} /> Autenticando...
                      </>
                    ) : cooldown > 0 ? (
                      <>
                        <Timer size={18} className="animate-pulse" /> Aguarde {cooldown}s
                      </>
                    ) : (
                      <>
                        <Lock size={16} /> Acessar Painel <ArrowRight size={16} />
                      </>
                    )}
                  </button>
                </form>
              )}
            </motion.div>
          ) : (
            <motion.div
              key="success"
              initial={{ opacity: 0, scale: 0.8, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              transition={{ type: "spring", stiffness: 200, damping: 20 }}
              className="flex flex-col items-center justify-center py-12 text-center"
              role="alert"
              aria-live="assertive"
            >
              <motion.div 
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", stiffness: 300, damping: 15, delay: 0.1 }}
                className="w-24 h-24 bg-green-500/20 rounded-full flex items-center justify-center mb-8 border border-green-500/30 shadow-[0_0_30px_rgba(34,197,94,0.2)]"
              >
                <CheckCircle2 size={48} className="text-green-500" />
              </motion.div>
              
              <h2 className="text-3xl font-black text-white mb-3 tracking-tight">Acesso Concedido</h2>
              <p className="text-slate-400 text-sm mb-10 max-w-[260px] leading-relaxed">
                Sessão administrativa segura estabelecida com sucesso.
              </p>
              
              <div className="bg-slate-800/80 backdrop-blur px-8 py-4 rounded-2xl border border-slate-700 flex flex-col items-center gap-1">
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Redirecionando em</p>
                <span className="text-4xl font-mono font-black text-white tabular-nums">
                  {countdown}<span className="text-base text-slate-500 ml-1">s</span>
                </span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <div className="mt-8 pt-6 border-t border-white/5 text-center">
          <p className="text-[10px] text-slate-500 font-mono uppercase font-bold tracking-widest flex items-center justify-center gap-2">
            <span className={cn("w-1.5 h-1.5 rounded-full transition-colors duration-500", isSuccess ? "bg-green-500 shadow-[0_0_10px_#22c55e]" : "bg-red-500 animate-pulse")}></span>
            {isSuccess ? "Sessão Ativa • Log Registrado" : "Ambiente Monitorado"}
          </p>
        </div>
      </div>
    </div>
  );
}
