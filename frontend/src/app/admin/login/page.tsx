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
import { motion, AnimatePresence } from "framer-motion";

const testimonials = [
  {
    quote: "O MesaFlow transformou nossa operação. O KDS eliminou os gritos na cozinha e o faturamento subiu 30%.",
    author: "Ricardo Silva",
    role: "Hamburgueria Artesanal"
  },
  {
    quote: "A melhor decisão que tomamos. O autoatendimento reduziu nossas filas em dias de pico.",
    author: "Ana Souza",
    role: "Arena Food Park"
  },
  {
    quote: "Simples, rápido e eficiente. Meus clientes adoram não precisar baixar aplicativo.",
    author: "Carlos Mendez",
    role: "Pizzaria Napoli"
  }
];

export default function LoginPage() {
  const router = useRouter();
  const [activeTestimonial, setActiveTestimonial] = useState(0);

  useState(() => {
    const interval = setInterval(() => {
      setActiveTestimonial((prev) => (prev + 1) % testimonials.length);
    }, 5000);
    return () => clearInterval(interval);
  });

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginSchema>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginSchema) => {
    try {
      const response = await login(data.email, data.password);
      
      setToken(response.access_token);
      setUserRole(response.user_role); 
      
      toast.success(`Bem-vindo, ${response.user_name}!`);
      
      // --- ATUALIZAÇÃO: Redirecionamento para Driver ---
      setTimeout(() => {
        const slug = response.company_slug;
        const role = response.user_role;

        if (role === 'kitchen') {
          router.push(`/admin/${slug}/kitchen`);
        } else if (role === 'cashier') {
          router.push(`/admin/${slug}/waiter`);
        } else if (role === 'driver') {
          router.push(`/admin/${slug}/driver`); // Nova Rota
        } else {
          router.push(`/admin/${slug}/dashboard`);
        }
      }, 500);

    } catch (err: any) {
      toast.error(err.message || "Credenciais inválidas");
    }
  };

  return (
    <div className="min-h-screen flex bg-white dark:bg-gray-900 font-sans overflow-hidden">
      <Toaster position="top-center" richColors />

      {/* LADO ESQUERDO - FORMULÁRIO */}
      <motion.div 
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full lg:w-1/2 flex flex-col justify-center px-8 sm:px-12 lg:px-24 py-12 relative z-10"
      >
        <div className="max-w-md mx-auto w-full">
          <div className="mb-10">
            <Link href="/" className="flex items-center gap-2 mb-8 group w-fit">
              <div className="bg-orange-600 p-2.5 rounded-xl shadow-lg shadow-orange-500/20 group-hover:scale-110 transition-transform">
                <ChefHat className="text-white w-6 h-6" />
              </div>
              <span className="text-2xl font-bold text-gray-900 dark:text-white tracking-tight">MesaFlow</span>
            </Link>
            
            <h1 className="text-4xl font-black text-gray-900 dark:text-white mb-2 tracking-tight">Bem-vindo de volta!</h1>
            <p className="text-gray-500 dark:text-gray-400 text-lg">Acesse sua conta para continuar.</p>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <AuthInput
              label="Email"
              icon={Mail}
              placeholder="seu@email.com"
              error={errors.email?.message}
              {...register("email")}
            />

            <div>
              <div className="flex justify-end mb-1">
                <a href="#" className="text-xs font-semibold text-orange-600 hover:text-orange-700">Esqueceu a senha?</a>
              </div>
              <AuthInput
                label="Senha"
                type="password"
                icon={Lock}
                placeholder="••••••••"
                error={errors.password?.message}
                {...register("password")}
              />
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full bg-orange-600 hover:bg-orange-700 text-white font-bold py-3.5 rounded-xl transition-all shadow-lg shadow-orange-500/30 hover:shadow-orange-500/50 hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {isSubmitting ? <Loader2 className="animate-spin" /> : <>Acessar <ArrowRight size={20} /></>}
            </button>
          </form>

          <div className="mt-8 text-center">
            <p className="text-gray-500 dark:text-gray-400">
              Ainda não tem uma conta?{" "}
              <Link href="/admin/register" className="text-orange-600 font-bold hover:underline transition-colors">
                Criar conta grátis
              </Link>
            </p>
          </div>
        </div>
      </motion.div>

      {/* LADO DIREITO - CARROSSEL */}
      <div className="hidden lg:flex w-1/2 bg-gray-900 relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('https://images.pexels.com/photos/1267320/pexels-photo-1267320.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1')] bg-cover bg-center opacity-30"></div>
        <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-gray-900/60 to-transparent"></div>
        
        <div className="relative z-10 flex flex-col justify-end p-16 h-full text-white w-full">
          <div className="mb-8 min-h-[180px]">
            <div className="flex gap-1 text-orange-500 mb-6">
              {[1,2,3,4,5].map(i => <svg key={i} className="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>)}
            </div>
            
            <AnimatePresence mode="wait">
              <motion.div
                key={activeTestimonial}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.5 }}
              >
                <blockquote className="text-3xl font-medium leading-tight tracking-tight mb-6">
                  "{testimonials[activeTestimonial].quote}"
                </blockquote>
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-white/10 rounded-full flex items-center justify-center text-xl font-bold border border-white/20 backdrop-blur-sm">
                    {testimonials[activeTestimonial].author[0]}
                  </div>
                  <div>
                    <p className="font-bold text-lg">{testimonials[activeTestimonial].author}</p>
                    <p className="text-gray-400 text-sm">{testimonials[activeTestimonial].role}</p>
                  </div>
                </div>
              </motion.div>
            </AnimatePresence>
          </div>

          <div className="flex gap-2">
            {testimonials.map((_, idx) => (
              <button
                key={idx}
                onClick={() => setActiveTestimonial(idx)}
                className={`h-1 rounded-full transition-all duration-300 ${idx === activeTestimonial ? "w-8 bg-orange-500" : "w-2 bg-gray-700 hover:bg-gray-600"}`}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}