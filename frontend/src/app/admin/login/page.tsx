"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { login } from "@/lib/api";
import { setToken, setUserRole } from "@/lib/auth";
import { loginSchema, LoginSchema } from "@/lib/validations/auth";
import { ChefHat, ArrowRight, Loader2, Mail, Lock, Chrome } from "lucide-react";
import { Toaster, toast } from "sonner";
import AuthInput from "@/components/ui/AuthInput";
import { motion, AnimatePresence } from "framer-motion";
import Script from "next/script";

export default function LoginPage() {
  const router = useRouter();
  const [isSocialLoading, setIsSocialLoading] = useState(false);
  const [showSocialModal, setShowSocialModal] = useState(false);

  const handleGoogleResponse = async (response: any) => {
    setIsSocialLoading(true);
    setShowSocialModal(false);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/google`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ credential: response.credential })
      });

      if (!res.ok) throw new Error("Falha na autenticação Google");

      const data = await res.json();
      setToken(data.access_token);
      setUserRole(data.user_role);
      toast.success(`Bem-vindo, ${data.user_name}!`);

      setTimeout(() => router.push(`/admin/${data.company_slug}/dashboard`), 500);
    } catch (e) {
      toast.error("Erro ao entrar com Google.");
    } finally {
      setIsSocialLoading(false);
    }
  };

  useEffect(() => {
    if ((window as any).google && showSocialModal) {
      (window as any).google.accounts.id.initialize({
        client_id: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID,
        callback: handleGoogleResponse
      });
      (window as any).google.accounts.id.renderButton(
        document.getElementById("google-btn-modal"),
        { theme: "filled_blue", size: "large", width: "100%", text: "signin_with" }
      );
    }
  }, [showSocialModal]);

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginSchema>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginSchema) => {
    try {
      const response = await login(data.email, data.password);
      setToken(response.access_token);
      setUserRole(response.user_role); 
      toast.success(`Bem-vindo, ${response.user_name}!`);

      setTimeout(() => {
        const slug = response.company_slug;
        const role = response.user_role;
        if (role === 'kitchen') router.push(`/admin/${slug}/kitchen`);
        else if (role === 'cashier') router.push(`/admin/${slug}/waiter`);
        else if (role === 'driver') router.push(`/admin/${slug}/driver`);
        else router.push(`/admin/${slug}/dashboard`);
      }, 500);
    } catch (err: any) {
      toast.error(err.message || "Credenciais inválidas");
    }
  };

  return (
    <div className="min-h-screen flex bg-white dark:bg-gray-900 font-sans overflow-hidden">
      <Toaster position="top-center" richColors />
      <Script src="https://accounts.google.com/gsi/client" strategy="afterInteractive" />

      <motion.div 
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className="w-full lg:w-1/2 flex flex-col justify-center px-8 sm:px-12 lg:px-24 py-12 relative z-10"
      >
        <div className="max-w-md mx-auto w-full">
          <div className="mb-10">
            <Link href="/" className="flex items-center gap-3 mb-8 group w-fit">
              <div className="bg-orange-600 p-3 rounded-2xl shadow-lg shadow-orange-500/20 group-hover:scale-110 transition-transform">
                <ChefHat className="text-white w-8 h-8" />
              </div>
              <span className="text-3xl font-black text-gray-900 dark:text-white tracking-tight">MesaFlow</span>
            </Link>
            <h1 className="text-4xl font-black text-gray-900 dark:text-white mb-2 tracking-tight">Acesse sua conta</h1>
            <p className="text-gray-500 dark:text-gray-400 text-lg">Gestão profissional para seu negócio.</p>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <AuthInput label="Email" icon={Mail} placeholder="seu@email.com" error={errors.email?.message} {...register("email")} />
            <div>
              <div className="flex justify-end mb-1">
                <Link href="/admin/forgot-password" className="text-xs font-semibold text-orange-600 hover:text-orange-700">Esqueceu a senha?</Link>
              </div>
              <AuthInput label="Senha" type="password" icon={Lock} placeholder="••••••••" error={errors.password?.message} {...register("password")} />
            </div>

            <button type="submit" disabled={isSubmitting} className="w-full bg-orange-600 hover:bg-orange-700 text-white font-bold py-3.5 rounded-xl transition-all shadow-lg shadow-orange-500/30 hover:shadow-orange-500/50 active:scale-95 disabled:opacity-70 flex items-center justify-center gap-2">
              {isSubmitting ? <Loader2 className="animate-spin" /> : <>Entrar <ArrowRight size={20} /></>}
            </button>
          </form>

          <div className="relative my-8">
            <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-gray-200 dark:border-gray-800"></div></div>
            <div className="relative flex justify-center text-sm"><span className="px-4 bg-white dark:bg-gray-900 text-gray-500 font-medium">ou continue com</span></div>
          </div>

          <button 
            onClick={() => setShowSocialModal(true)}
            className="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-200 font-bold py-3 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-700 transition-all flex items-center justify-center gap-3 shadow-sm"
          >
            <Chrome size={20} className="text-blue-500" />
            Entrar com Google
          </button>

          <div className="mt-8 text-center">
            <p className="text-gray-500 dark:text-gray-400">
              Novo por aqui? <Link href="/admin/register" className="text-orange-600 font-bold hover:underline">Criar conta grátis</Link>
            </p>
          </div>
        </div>
      </motion.div>

      {/* LADO DIREITO - IMAGEM LIFESTYLE */}
      <div className="hidden lg:flex w-1/2 bg-gray-900 relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('https://images.pexels.com/photos/1267320/pexels-photo-1267320.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1')] bg-cover bg-center opacity-40"></div>
        <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-transparent to-transparent"></div>
      </div>

      {/* MODAL DE LOGIN SOCIAL */}
      <AnimatePresence>
        {showSocialModal && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
            <motion.div 
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-white dark:bg-gray-800 w-full max-w-sm rounded-2xl shadow-2xl p-8 text-center relative"
            >
              <button onClick={() => setShowSocialModal(false)} className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 dark:hover:text-white">
                <X size={24} />
              </button>
              <div className="bg-blue-50 dark:bg-blue-900/20 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Chrome size={32} className="text-blue-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Login Social</h2>
              <p className="text-gray-500 dark:text-gray-400 text-sm mb-8">Utilize sua conta Google para acessar o MesaFlow instantaneamente.</p>
              
              <div id="google-btn-modal" className="w-full min-h-[44px]"></div>
              
              <p className="text-[10px] text-gray-400 mt-6 leading-relaxed">
                Ao continuar, você concorda com nossos Termos de Serviço e Política de Privacidade.
              </p>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}

const X = ({ size }: { size: number }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
);
