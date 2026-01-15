
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { login } from "@/lib/api";
import { setToken, setUserRole } from "@/lib/auth";
import { loginSchema, LoginSchema } from "@/lib/validations/auth";
import { ChefHat, ArrowRight, Loader2, Mail, Lock } from "lucide-react";
import { Toaster, toast } from "sonner";
import AuthInput from "@/components/ui/AuthInput";
import { motion } from "framer-motion";

export default function LoginPage() {
  const router = useRouter();
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginSchema>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginSchema) => {
    try {
      const response = await login(data.email, data.password);
      setToken(response.access_token);
      setUserRole(response.user_role); 
      toast.success(`Bem-vindo!`);
      router.push(`/admin/${response.company_slug}/dashboard`);
    } catch (err: any) {
      toast.error(err.message || "Credenciais inválidas");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-white dark:bg-gray-900 p-4">
      <Toaster position="top-center" richColors />
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-md w-full space-y-8 bg-white dark:bg-gray-800 p-8 rounded-3xl shadow-xl border border-gray-100 dark:border-gray-700"
      >
        <div className="text-center">
          <Link href="/" className="inline-flex items-center gap-2 mb-6">
            <div className="bg-orange-600 p-2 rounded-xl text-white">
              <ChefHat size={32} />
            </div>
            <span className="text-2xl font-black dark:text-white">MesaFlow</span>
          </Link>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Acesse sua conta</h1>
          <p className="text-gray-500 mt-2">Gestão profissional para seu negócio.</p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6" data-testid="login-form">
          <AuthInput 
            label="Email" 
            icon={Mail} 
            placeholder="seu@email.com" 
            error={errors.email?.message} 
            {...register("email")}
            data-testid="login-email"
          />
          
          <div className="relative">
            <AuthInput 
              label="Senha" 
              type="password" 
              icon={Lock} 
              placeholder="••••••••" 
              error={errors.password?.message} 
              {...register("password")}
              data-testid="login-password"
            />
            <Link href="/admin/forgot-password" title="Recuperar Senha" className="absolute right-0 top-0 text-xs font-bold text-orange-600 hover:underline">
              Esqueceu a senha?
            </Link>
          </div>

          <button 
            type="submit" 
            disabled={isSubmitting}
            data-testid="login-submit"
            className="w-full bg-orange-600 hover:bg-orange-700 text-white font-bold py-4 rounded-2xl transition-all flex items-center justify-center gap-2 shadow-lg shadow-orange-600/20"
          >
            {isSubmitting ? <Loader2 className="animate-spin" /> : <>Entrar <ArrowRight size={20} /></>}
          </button>
        </form>

        <div className="text-center pt-4">
          <p className="text-sm text-gray-500">
            Novo por aqui? <Link href="/admin/register" className="text-orange-600 font-bold hover:underline">Criar conta grátis</Link>
          </p>
        </div>
      </motion.div>
    </div>
  );
}

