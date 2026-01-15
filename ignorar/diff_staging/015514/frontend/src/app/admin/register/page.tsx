"use client";

import { useEffect, useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { register as registerApi } from "@/lib/api";
import { setTokens } from "@/lib/auth";
import { registerSchema, RegisterSchema } from "@/lib/validations/auth";
import { 
  ChefHat, ArrowRight, Loader2, Mail, Lock, Store, 
  Link as LinkIcon, CheckCircle2, Phone, User, 
  Building2, Ticket, Briefcase, ShieldCheck 
} from "lucide-react";
import { Toaster, toast } from "sonner";
import AuthInput from "@/components/ui/AuthInput";
import Logo from "@/components/ui/Logo";
import { motion, AnimatePresence } from "framer-motion";

const segmentAssets = {
  gastro: {
    image: "https://images.pexels.com/photos/260922/pexels-photo-260922.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    title: "Revolucione seu Restaurante",
    features: ["Cardápio Digital QR", "KDS em Tempo Real", "Delivery Próprio"]
  },
  hotel: {
    image: "https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    title: "Room Service Moderno",
    features: ["Pedidos no Quarto", "Concierge Digital", "Check-out Express"]
  },
  event: {
    image: "https://images.pexels.com/photos/1190298/pexels-photo-1190298.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    title: "Agilidade para Eventos",
    features: ["Venda no Assento", "Fila Zero", "Gestão de Staff"]
  },
  corp: {
    image: "https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    title: "Gestão Corporativa",
    features: ["Refeitório Digital", "Coffee Break", "Saldo Centralizado"]
  }
};

function RegisterForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const plan = searchParams.get("plan");
  const [passwordStrength, setPasswordStrength] = useState(0);

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<RegisterSchema>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      segment: "gastro",
      company_name: "",
      company_slug: "",
      owner_email: "",
      password: "",
      owner_phone: "",
      owner_role: ""
    }
  });

  const companyName = watch("company_name");
  const watchedSegment = watch("segment") as keyof typeof segmentAssets;
  const watchedPassword = watch("password");

  // 1. Geração de Slug Automática
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

  // 2. Medidor de Força de Senha
  useEffect(() => {
    if (!watchedPassword) {
      setPasswordStrength(0);
      return;
    }
    let strength = 0;
    if (watchedPassword.length >= 8) strength += 1;
    if (/[A-Z]/.test(watchedPassword)) strength += 1;
    if (/[0-9]/.test(watchedPassword)) strength += 1;
    if (/[^A-Za-z0-9]/.test(watchedPassword)) strength += 1;
    setPasswordStrength(strength);
  }, [watchedPassword]);

  // 3. Máscara de Telefone
  const handlePhoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    let val = e.target.value.replace(/\D/g, "");
    if (val.length > 11) val = val.slice(0, 11);
    if (val.length > 2) val = `(${val.slice(0, 2)}) ${val.slice(2)}`;
    if (val.length > 10) val = `${val.slice(0, 10)}-${val.slice(10)}`;
    setValue("owner_phone", val, { shouldValidate: true });
  };

  const onSubmit = async (data: RegisterSchema) => {
    try {
      const payload = {
        ...data,
        owner_phone: data.owner_phone?.replace(/\D/g, "")
      };

      const response = await registerApi(payload);
      setTokens(response.access_token, response.refresh_token);
      toast.success("Bem-vindo ao MesaFlow!");
      
      const target = plan === 'pro' 
        ? `/admin/${response.company_slug}/settings/billing?auto_checkout=true`
        : `/admin/${response.company_slug}/dashboard`;
      
      router.push(target);
    } catch (err: any) {
      toast.error(err.message || "Erro ao criar conta.");
    }
  };

  const getStrengthColor = () => {
    const colors = ["bg-red-500", "bg-orange-500", "bg-yellow-500", "bg-blue-500", "bg-green-500"];
    return colors[passwordStrength];
  };

  return (
    <div className="flex min-h-screen bg-slate-950">
      {/* LADO ESQUERDO: FORMULÁRIO */}
      <motion.div 
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className="w-full lg:w-1/2 flex flex-col justify-center px-8 sm:px-12 lg:px-24 py-12 bg-slate-900 overflow-y-auto"
      >
        <div className="max-w-md mx-auto w-full">
          <Link href="/" className="inline-block mb-10">
            <Logo variant="light" size="lg" animated />
          </Link>

          <div className="mb-8">
            <h1 className="text-4xl font-black text-white tracking-tight mb-2">Comece agora.</h1>
            <p className="text-slate-400 text-lg">Sua operação digital em minutos.</p>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Seleção de Segmento */}
            <div className="space-y-3">
              <label className="block text-sm font-bold text-slate-400 uppercase tracking-wider">Tipo de Negócio</label>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { id: 'gastro', label: 'Restaurante', icon: Store },
                  { id: 'event', label: 'Eventos', icon: Ticket },
                  { id: 'hotel', label: 'Hotelaria', icon: Building2 },
                  { id: 'corp', label: 'Corporativo', icon: Briefcase }
                ].map((seg) => (
                  <label 
                    key={seg.id} 
                    className={cn(
                      "cursor-pointer border-2 rounded-xl p-3 flex flex-col items-center gap-2 transition-all",
                      watchedSegment === seg.id 
                        ? "bg-orange-600/10 border-orange-600 text-orange-500 shadow-[0_0_15px_rgba(234,88,12,0.1)]" 
                        : "border-slate-800 bg-slate-800/30 text-slate-500 hover:border-slate-700"
                    )}
                  >
                    <input type="radio" value={seg.id} {...register('segment')} className="hidden" />
                    <seg.icon size={20} />
                    <span className="text-xs font-bold uppercase">{seg.label}</span>
                  </label>
                ))}
              </div>
            </div>

            <AuthInput 
              label="Nome do Negócio" 
              icon={Store} 
              placeholder="Ex: Hamburgueria do Zé" 
              error={errors.company_name?.message} 
              {...register("company_name")} 
            />

            <div className="space-y-1.5">
              <label className="block text-sm font-bold text-slate-400 uppercase tracking-wider">Link da sua loja</label>
              <div className={cn(
                "flex items-center bg-slate-800/50 border-2 rounded-xl overflow-hidden transition-all",
                errors.company_slug ? "border-red-500/50" : "border-slate-700 focus-within:border-orange-500"
              )}>
                <div className="bg-slate-800 px-4 py-3.5 border-r border-slate-700">
                  <span className="text-slate-500 font-bold text-sm">mesaflow.com/</span>
                </div>
                <input 
                  {...register("company_slug")} 
                  className="flex-1 bg-transparent py-3.5 px-4 text-white outline-none font-bold text-sm" 
                  placeholder="link-da-loja" 
                />
              </div>
              {errors.company_slug && <p className="text-red-500 text-xs font-bold ml-1">{errors.company_slug.message}</p>}
            </div>

            <div className="grid grid-cols-2 gap-4">
              <AuthInput 
                label="Seu Cargo" 
                icon={User} 
                placeholder="Ex: Gerente" 
                {...register("owner_role")} 
              />
              <AuthInput 
                label="WhatsApp" 
                icon={Phone} 
                placeholder="(00) 00000-0000" 
                error={errors.owner_phone?.message} 
                {...register("owner_phone")}
                onChange={handlePhoneChange}
              />
            </div>

            <AuthInput 
              label="E-mail Profissional" 
              type="email" 
              icon={Mail} 
              placeholder="seu@email.com" 
              error={errors.owner_email?.message} 
              {...register("owner_email")} 
            />

            <div className="space-y-2">
              <AuthInput 
                label="Senha de Acesso" 
                type="password" 
                icon={Lock} 
                placeholder="Mínimo 8 caracteres" 
                error={errors.password?.message} 
                {...register("password")} 
              />
              {watchedPassword && (
                <div className="flex gap-1 h-1.5 px-1">
                  {[1, 2, 3, 4].map((step) => (
                    <div 
                      key={step} 
                      className={cn(
                        "flex-1 rounded-full transition-all duration-500",
                        step <= passwordStrength ? getStrengthColor() : "bg-slate-800"
                      )}
                    />
                  ))}
                </div>
              )}
            </div>

            <button 
              type="submit" 
              disabled={isSubmitting} 
              className="w-full bg-orange-600 hover:bg-orange-700 text-white font-black py-4 rounded-xl transition-all shadow-lg shadow-orange-900/20 active:scale-[0.98] disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {isSubmitting ? <Loader2 className="animate-spin" /> : <>Criar minha conta <ArrowRight size={20} /></>}
            </button>
          </form>

          <p className="mt-8 text-center text-slate-500 text-sm">
            Já tem uma conta? <Link href="/admin/login" className="text-orange-500 font-bold hover:underline">Fazer Login</Link>
          </p>
        </div>
      </motion.div>

      {/* LADO DIREITO: VISUAL DINÂMICO */}
      <div className="hidden lg:flex lg:w-1/2 bg-slate-900 relative overflow-hidden border-l border-slate-800">
        <AnimatePresence mode="wait">
          <motion.div
            key={watchedSegment}
            initial={{ opacity: 0, scale: 1.1 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.6 }}
            className="absolute inset-0"
          >
            <div 
              className="absolute inset-0 bg-cover bg-center opacity-40" 
              style={{ backgroundImage: `url('${segmentAssets[watchedSegment].image}')` }} 
            />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent" />
            
            <div className="relative z-10 flex flex-col justify-end p-20 h-full">
              <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.3 }}
              >
                <h2 className="text-5xl font-black text-white mb-6 leading-tight">
                  {segmentAssets[watchedSegment].title}
                </h2>
                <ul className="space-y-4">
                  {segmentAssets[watchedSegment].features.map((feat, i) => (
                    <li key={i} className="flex items-center gap-4 text-slate-200 text-xl font-medium">
                      <div className="bg-emerald-500/20 p-1 rounded-full">
                        <CheckCircle2 className="text-emerald-500" size={24}/>
                      </div>
                      {feat}
                    </li>
                  ))}
                </ul>
              </motion.div>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}

export default function RegisterPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-slate-950 flex items-center justify-center text-white font-bold">Carregando MesaFlow...</div>}>
      <RegisterForm />
    </Suspense>
  );
}
