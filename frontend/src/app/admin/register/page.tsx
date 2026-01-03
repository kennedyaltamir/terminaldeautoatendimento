"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { register as registerApi } from "@/lib/api";
import { setToken } from "@/lib/auth";
import { registerSchema, RegisterSchema } from "@/lib/validations/auth";
import { ChefHat, ArrowRight, Loader2, Mail, Lock, Store, Link as LinkIcon, CheckCircle2, Phone, User } from "lucide-react";
import { Toaster, toast } from "sonner";
import AuthInput from "@/components/ui/AuthInput";
import { motion } from "framer-motion";

export default function RegisterPage() {
  const router = useRouter();

  // CORREÇÃO: Removida a tipagem explícita <RegisterSchema> para permitir
  // que o TypeScript infira os tipos corretamente através do zodResolver,
  // evitando conflitos com campos que possuem .default() no Zod.
  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm({
    resolver: zodResolver(registerSchema),
    defaultValues: {
        company_name: "",
        company_slug: "",
        owner_email: "",
        password: "",
        owner_phone: "",
        owner_role: "",
        segment: "gastro" // Valor padrão alinhado com o Zod
    }
  });

  const companyName = watch("company_name");

  // Auto-gerar slug quando o nome muda
  useEffect(() => {
    if (companyName) {
      const slug = companyName
        .toLowerCase()
        .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
        .replace(/[^a-z0-9]/g, "-")
        .replace(/-+/g, "-")
        .replace(/^-|-$/g, "");
      
      setValue("company_slug", slug, { shouldValidate: true });
    }
  }, [companyName, setValue]);

  // CORREÇÃO: Removida tipagem explícita : SubmitHandler<RegisterSchema>
  // O TypeScript infere o tipo 'data' automaticamente do schema do useForm.
  const onSubmit = async (data: any) => {
    try {
      // Casting seguro para garantir que data segue a interface esperada pela API
      const payload = data as RegisterSchema;
      
      const response = await registerApi(payload);
      setToken(response.access_token);
      toast.success("Conta criada com sucesso!");
      
      setTimeout(() => {
        router.push(`/admin/${response.company_slug}/dashboard`);
      }, 500);
    } catch (err: any) {
      toast.error(err.message || "Erro ao criar conta. Verifique os dados.");
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
        className="w-full lg:w-1/2 flex flex-col justify-center px-8 sm:px-12 lg:px-24 py-12 relative z-10 overflow-y-auto max-h-screen"
      >
        <div className="max-w-md mx-auto w-full py-8">
          <div className="mb-8">
            <Link href="/" className="flex items-center gap-2 mb-8 group w-fit">
              <div className="bg-orange-600 p-2.5 rounded-xl shadow-lg shadow-orange-500/20 group-hover:scale-110 transition-transform">
                <ChefHat className="text-white w-6 h-6" />
              </div>
              <span className="text-2xl font-bold text-gray-900 dark:text-white tracking-tight">MesaFlow</span>
            </Link>
            <h1 className="text-4xl font-black text-gray-900 dark:text-white mb-2 tracking-tight">Crie sua conta grátis</h1>
            <p className="text-gray-500 dark:text-gray-400 text-lg">Comece a vender em minutos. Sem cartão.</p>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            
            {/* Segmento */}
            <div>
              <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-1.5">Qual seu tipo de negócio?</label>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { id: 'gastro', label: 'Restaurante / Bar' },
                  { id: 'event', label: 'Eventos / Estádio' },
                  { id: 'hotel', label: 'Hotelaria' },
                  { id: 'corp', label: 'Corporativo' }
                ].map((seg) => (
                  <label key={seg.id} className={`cursor-pointer border rounded-xl p-3 text-center text-sm font-medium transition-all ${watch('segment') === seg.id ? 'bg-orange-50 border-orange-500 text-orange-700' : 'border-gray-200 hover:bg-gray-50'}`}>
                    <input type="radio" value={seg.id} {...register('segment')} className="hidden" />
                    {seg.label}
                  </label>
                ))}
              </div>
            </div>

            <AuthInput
              label="Nome do Negócio"
              icon={Store}
              placeholder="Ex: Pizzaria do João"
              error={errors.company_name?.message as string}
              {...register("company_name")}
            />

            <div>
              <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-1.5">Link do Cardápio</label>
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <LinkIcon className={`h-5 w-5 ${errors.company_slug ? "text-red-500" : "text-gray-400 group-focus-within:text-orange-500"}`} />
                </div>
                <div className={`flex items-center w-full bg-gray-50 dark:bg-gray-800 border rounded-xl overflow-hidden transition-all ${errors.company_slug ? "border-red-300 focus-within:ring-2 focus-within:ring-red-200" : "border-gray-200 dark:border-gray-700 focus-within:ring-2 focus-within:ring-orange-100 focus-within:border-orange-500"}`}>
                  <span className="pl-10 pr-1 text-gray-500 text-sm font-medium select-none">mesaflow.com/</span>
                  <input
                    {...register("company_slug")}
                    className="flex-1 py-3 bg-transparent text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none font-bold"
                    placeholder="pizzaria-joao"
                  />
                </div>
              </div>
              {errors.company_slug && <p className="text-xs text-red-500 font-medium mt-1">{errors.company_slug.message as string}</p>}
            </div>

            <div className="grid grid-cols-2 gap-4">
              <AuthInput
                label="Seu Nome/Cargo"
                icon={User}
                placeholder="Gerente"
                {...register("owner_role")}
              />
              <AuthInput
                label="WhatsApp"
                icon={Phone}
                placeholder="(11) 99999-9999"
                error={errors.owner_phone?.message as string}
                {...register("owner_phone")}
              />
            </div>

            <AuthInput
              label="Email Corporativo"
              type="email"
              icon={Mail}
              placeholder="admin@restaurante.com"
              error={errors.owner_email?.message as string}
              {...register("owner_email")}
            />

            <AuthInput
              label="Senha"
              type="password"
              icon={Lock}
              placeholder="Mínimo 8 caracteres (Letras + Números)"
              error={errors.password?.message as string}
              {...register("password")}
            />

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full bg-orange-600 hover:bg-orange-700 text-white font-bold py-3.5 rounded-xl transition-all shadow-lg shadow-orange-500/30 hover:shadow-orange-500/50 hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-2 mt-2"
            >
              {isSubmitting ? <Loader2 className="animate-spin" /> : <>Criar Conta Grátis <ArrowRight size={20} /></>}
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
      </motion.div>

      {/* LADO DIREITO - FEATURES */}
      <div className="hidden lg:flex w-1/2 bg-gray-900 relative overflow-hidden">
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