"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { registerSchema, RegisterSchema } from "@/lib/validations/auth";
import { register as registerApi } from "@/lib/api";
import { Store, Mail, Lock, ArrowRight, Loader2, Globe, Smartphone, ShieldCheck } from "lucide-react";
import Link from "next/link";
import { toast, Toaster } from "sonner";
import AuthInput from "@/components/ui/AuthInput";
import Logo from "@/components/ui/Logo";

export default function RegisterPage() {
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<RegisterSchema>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      segment: "gastro"
    }
  });

  const slug = watch("company_slug");

  const onSubmit = async (data: RegisterSchema) => {
    setLoading(true);
    try {
      const res = await registerApi(data);
      toast.success("Conta criada com sucesso!");
      router.push(`/admin/${res.company_slug}/dashboard`);
    } catch (error: any) {
      toast.error(error.message || "Erro ao criar conta. Tente outro link.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col lg:flex-row font-sans">
      <Toaster position="top-right" richColors />
      
      {/* Lado Esquerdo: Branding */}
      <div className="lg:w-1/2 bg-orange-600 p-12 flex flex-col justify-between relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-0 w-96 h-96 bg-white rounded-full -translate-x-1/2 -translate-y-1/2"></div>
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-white rounded-full translate-x-1/2 translate-y-1/2"></div>
        </div>
        
        <Link href="/">
          <Logo variant="light" size="lg" animated />
        </Link>

        <div className="relative z-10">
          <h2 className="text-5xl font-black text-white leading-tight mb-6">
            Sua operação em <br />outro nível.
          </h2>
          <ul className="space-y-4">
            {[
              "Cardápio Digital em 2 minutos",
              "KDS Nativo para Cozinha",
              "Pagamentos Pix Automáticos",
              "Gestão Multi-tenant Segura"
            ].map((item, i) => (
              <li key={i} className="flex items-center gap-3 text-orange-100 font-bold">
                <ShieldCheck size={24} className="text-white" /> {item}
              </li>
            ))}
          </ul>
        </div>

        <p className="text-orange-200 text-sm font-medium">
          Junte-se a mais de 500 estabelecimentos que confiam no MesaFlow.
        </p>
      </div>

      {/* Lado Direito: Formulário */}
      <div className="lg:w-1/2 p-8 lg:p-24 flex items-center justify-center bg-slate-900">
        <div className="w-full max-w-md space-y-8 animate-in fade-in slide-in-from-right-4 duration-700">
          <div>
            <h1 className="text-3xl font-black text-white tracking-tight">Criar minha conta</h1>
            <p className="text-slate-400 mt-2">Comece seu teste gratuito de 7 dias agora.</p>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            <AuthInput 
              label="Nome do Negócio" 
              icon={Store} 
              placeholder="Ex: Pizzaria do Bairro"
              {...register("company_name")}
              error={errors.company_name?.message}
            />

            <div className="space-y-1.5">
              <label className="block text-sm font-bold text-slate-400 uppercase tracking-wider">Link da sua loja</label>
              <div className="flex items-center bg-slate-800 border-2 border-slate-700 rounded-xl px-4 focus-within:border-orange-500 transition-all">
                <span className="text-slate-500 font-medium text-sm">mesaflow.com/</span>
                <input 
                  {...register("company_slug")}
                  className="flex-1 bg-transparent py-3.5 pl-1 text-white outline-none font-bold"
                  placeholder="seu-nome"
                />
              </div>
              {errors.company_slug && <p className="text-red-500 text-xs font-bold">{errors.company_slug.message}</p>}
            </div>

            <AuthInput 
              label="E-mail do Proprietário" 
              icon={Mail} 
              type="email"
              placeholder="seu@email.com"
              {...register("owner_email")}
              error={errors.owner_email?.message}
            />

            <AuthInput 
              label="Senha de Acesso" 
              icon={Lock} 
              type="password"
              placeholder="Mínimo 8 caracteres"
              {...register("password")}
              error={errors.password?.message}
            />

            <div className="pt-2">
              <button 
                type="submit" 
                disabled={loading}
                className="w-full bg-orange-600 hover:bg-orange-700 text-white font-black py-4 rounded-xl flex items-center justify-center gap-2 transition-all shadow-lg shadow-orange-900/20 active:scale-95 disabled:opacity-50"
              >
                {loading ? <Loader2 className="animate-spin" /> : <>Criar minha conta <ArrowRight size={20} /></>}
              </button>
            </div>
          </form>

          <p className="text-center text-slate-500 text-sm">
            Já tem uma conta?{" "}
            <Link href="/admin/login" className="text-orange-500 font-bold hover:underline">Fazer Login</Link>
          </p>

          <div className="pt-8 border-t border-slate-800">
            <p className="text-[10px] text-slate-600 text-center leading-relaxed">
              Ao se cadastrar, você concorda com nossos{" "}
              <Link href="/trust/security" className="underline">Termos de Serviço</Link> e{" "}
              <Link href="/trust/security" className="underline">Política de Privacidade</Link>.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
