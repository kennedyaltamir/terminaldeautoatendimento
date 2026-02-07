"use client";

/**
 * DOMAIN: ADMIN / ONBOARDING
 * OBJECTIVE: Página de registro consolidada (Gold Master v20).
 * FIXES: 
 *  - React Warning: Eliminação de setState durante render.
 *  - Acessibilidade: Adição de atributos autoComplete.
 *  - UX: Feedback visual robusto.
 */

import { useState, useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Loader2, ArrowRight, CheckCircle2, Building2, Mail, Lock, Phone, User, 
  Store, Ticket, Briefcase, ChevronRight, Link as LinkIcon, Search, XCircle 
} from "lucide-react";
import { toast, Toaster } from "sonner";

import { register as registerApi, ApiError } from "@/lib/api";
import { setTokens, setUserRole } from "@/lib/auth";
import { registerSchema, RegisterSchema } from "@/lib/validations/auth";
import AuthInput from "@/components/ui/AuthInput";
import Logo from "@/components/ui/Logo";
import { cn } from "@/lib/utils";

// --- CONFIGURAÇÃO VISUAL POR SEGMENTO ---
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

// Hook de Debounce Isolado
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);
  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);
  return debouncedValue;
}

function RegisterForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const plan = searchParams.get("plan");
  
  const [step, setStep] = useState(1);
  const [passwordStrength, setPasswordStrength] = useState(0);
  
  // Estados para CNPJ e Slug
  const [cnpj, setCnpj] = useState("");
  const [isCheckingCnpj, setIsCheckingCnpj] = useState(false);
  const [slugStatus, setSlugStatus] = useState<'idle' | 'checking' | 'available' | 'unavailable'>('idle');
  const [slugManuallyEdited, setSlugManuallyEdited] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    trigger,
    formState: { errors, isSubmitting },
  } = useForm<RegisterSchema>({
    resolver: zodResolver(registerSchema),
    mode: "onChange",
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
  const companySlug = watch("company_slug");
  const watchedSegment = watch("segment") as keyof typeof segmentAssets;
  const watchedPassword = watch("password");

  const debouncedSlug = useDebounce(companySlug, 500);
  const debouncedCnpj = useDebounce(cnpj, 800);

  // 1. Geração Automática de Slug (Effect Safe)
  useEffect(() => {
    if (companyName && step === 1 && !slugManuallyEdited) {
      const slug = companyName
        .toLowerCase()
        .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
        .replace(/[^a-z0-9]/g, "-")
        .replace(/-+/g, "-")
        .replace(/^-|-$/g, "");
      setValue("company_slug", slug, { shouldValidate: true });
    }
  }, [companyName, setValue, step, slugManuallyEdited]);

  // 2. Validação de Slug em Tempo Real
  useEffect(() => {
    let isMounted = true;
    const checkSlug = async () => {
      if (!debouncedSlug || debouncedSlug.length < 3) {
        if (isMounted) setSlugStatus('idle');
        return;
      }
      if (isMounted) setSlugStatus('checking');
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/utils/check-slug?slug=${debouncedSlug}`);
        if (!isMounted) return;
        
        if (res.status === 409) {
          setSlugStatus('unavailable');
        } else if (res.ok) {
          setSlugStatus('available');
        } else {
          setSlugStatus('idle');
        }
      } catch (e) {
        if (isMounted) setSlugStatus('idle');
      }
    };
    checkSlug();
    return () => { isMounted = false; };
  }, [debouncedSlug]);

  // 3. Consulta de CNPJ
  useEffect(() => {
    let isMounted = true;
    const fetchCnpj = async () => {
      const cleanCnpj = debouncedCnpj.replace(/\D/g, "");
      if (cleanCnpj.length !== 14) return;

      if (isMounted) setIsCheckingCnpj(true);
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/utils/consult-cnpj/${cleanCnpj}`);
        if (!isMounted) return;

        if (res.ok) {
          const data = await res.json();
          setValue("company_name", data.name, { shouldValidate: true });
          if (data.email) setValue("owner_email", data.email);
          if (data.phone) setValue("owner_phone", data.phone);
          toast.success("Dados da empresa encontrados!");
        } else if (res.status === 429) {
          toast.warning("Muitas consultas. Preencha manualmente.");
        } else {
          toast.error("CNPJ não encontrado na base pública.");
        }
      } catch (e) {
        // Ignora erro de rede
      } finally {
        if (isMounted) setIsCheckingCnpj(false);
      }
    };
    fetchCnpj();
    return () => { isMounted = false; };
  }, [debouncedCnpj, setValue]);

  // 4. Medidor de Força de Senha
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

  // Handlers
  const handlePhoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    let val = e.target.value.replace(/\D/g, "");
    if (val.length > 11) val = val.slice(0, 11);
    if (val.length > 2) val = `(${val.slice(0, 2)}) ${val.slice(2)}`;
    if (val.length > 10) val = `${val.slice(0, 10)}-${val.slice(10)}`;
    setValue("owner_phone", val, { shouldValidate: true });
  };

  const handleCnpjChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    let val = e.target.value.replace(/\D/g, "");
    if (val.length > 14) val = val.slice(0, 14);
    val = val.replace(/^(\d{2})(\d)/, "$1.$2");
    val = val.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3");
    val = val.replace(/\.(\d{3})(\d)/, ".$1/$2");
    val = val.replace(/(\d{4})(\d)/, "$1-$2");
    setCnpj(val);
  };

  const handleNextStep = async () => {
    if (slugStatus === 'unavailable') {
      toast.error("Este link já está em uso. Escolha outro.");
      return;
    }
    const fieldsToValidate: (keyof RegisterSchema)[] = ["company_name", "company_slug", "segment"];
    const isValid = await trigger(fieldsToValidate);
    if (isValid) setStep(step + 1);
  };

  const onSubmit = async (data: RegisterSchema) => {
    try {
      const payload = {
        ...data,
        owner_phone: data.owner_phone?.replace(/\D/g, "")
      };

      const response = await registerApi(payload);
      
      setTokens(response.access_token, response.refresh_token);
      setUserRole(response.user_role);
      
      if (typeof window !== "undefined") {
        localStorage.setItem("mesaflow_user_name", response.user_name || "Admin");
        localStorage.setItem("mesaflow_company_slug", response.company_slug);
      }

      toast.success("Conta criada com sucesso! Bem-vindo ao MesaFlow.");
      
      const target = plan === 'pro' 
        ? `/admin/${response.company_slug}/settings/billing?auto_checkout=true`
        : `/admin/${response.company_slug}/dashboard`;
      
      setTimeout(() => {
        router.push(target);
      }, 1000);

    } catch (err: any) {
      const apiErr = err as ApiError;
      let message = "Ocorreu um erro inesperado no cadastro.";
      if (typeof apiErr.message === 'string') {
        message = apiErr.message;
      } else if ((apiErr as any).detail && typeof (apiErr as any).detail === 'string') {
        message = (apiErr as any).detail;
      }
      toast.error("Erro no cadastro", { description: message });
    }
  };

  const getStrengthColor = () => {
    const colors = ["bg-red-500", "bg-orange-500", "bg-yellow-500", "bg-blue-500", "bg-green-500"];
    return colors[passwordStrength] || "bg-slate-800";
  };

  return (
    <div className="min-h-screen flex bg-slate-950 font-sans overflow-hidden selection:bg-orange-500/30 selection:text-orange-200">
      <Toaster position="top-center" richColors theme="dark" />

      {/* --- LADO ESQUERDO: FORMULÁRIO --- */}
      <motion.div 
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6, ease: "circOut" }}
        className="w-full lg:w-1/2 flex flex-col justify-center px-8 sm:px-12 lg:px-24 py-12 relative z-10 bg-slate-950 border-r border-slate-900 overflow-y-auto"
      >
        <div className="max-w-md mx-auto w-full relative z-20">
          <div className="mb-10">
            <Link href="/" className="inline-block mb-8 hover:opacity-80 transition-opacity">
              <Logo size="lg" variant="color" animated={true} />
            </Link>
            <h1 className="text-3xl md:text-4xl font-black text-white mb-2 tracking-tight">
              Crie sua conta
            </h1>
            <p className="text-slate-400 text-base font-medium">
              Comece a transformar sua operação hoje.
            </p>
          </div>

          {/* Barra de Progresso */}
          <div className="flex gap-2 mb-8">
            <div className={`h-1 flex-1 rounded-full transition-all duration-500 ${step >= 1 ? "bg-orange-600" : "bg-slate-800"}`} />
            <div className={`h-1 flex-1 rounded-full transition-all duration-500 ${step >= 2 ? "bg-orange-600" : "bg-slate-800"}`} />
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <AnimatePresence mode="wait">
              {step === 1 && (
                <motion.div
                  key="step1"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="space-y-6"
                >
                  {/* CNPJ (Opcional) */}
                  <div className="relative group">
                    <label className="block text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] ml-1 mb-1">CNPJ (Opcional)</label>
                    <div className="relative">
                      <Search className="absolute left-4 top-3.5 text-slate-500" size={18} />
                      <input 
                        type="text"
                        value={cnpj}
                        onChange={handleCnpjChange}
                        placeholder="00.000.000/0000-00"
                        className="w-full bg-slate-900/50 border border-slate-800 rounded-xl pl-12 pr-10 py-3.5 text-white outline-none focus:border-orange-500 transition-all font-mono text-sm"
                        autoComplete="off"
                      />
                      {isCheckingCnpj && (
                        <div className="absolute right-4 top-3.5">
                          <Loader2 className="animate-spin text-orange-500" size={18} />
                        </div>
                      )}
                    </div>
                    <p className="text-[10px] text-slate-600 mt-1 ml-1">Preenchemos os dados automaticamente para você.</p>
                  </div>

                  {/* Seleção de Segmento */}
                  <div className="space-y-3">
                    <label className="block text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] ml-1">Tipo de Negócio</label>
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
                            "cursor-pointer border-2 rounded-xl p-4 flex flex-col items-center gap-2 transition-all hover:border-slate-700",
                            watchedSegment === seg.id 
                              ? "bg-orange-600/10 border-orange-600 text-orange-500 shadow-[0_0_15px_rgba(234,88,12,0.1)]" 
                              : "border-slate-800 bg-slate-900/50 text-slate-500"
                          )}
                        >
                          <input type="radio" value={seg.id} {...register('segment')} className="hidden" />
                          <seg.icon size={24} />
                          <span className="text-xs font-bold uppercase tracking-wide">{seg.label}</span>
                        </label>
                      ))}
                    </div>
                  </div>

                  <AuthInput 
                    label="Nome do Negócio" 
                    icon={Store} 
                    placeholder="Ex: Hamburgueria do Zé" 
                    error={errors.company_name?.message} 
                    autoComplete="organization"
                    {...register("company_name")} 
                  />

                  <div className="space-y-1.5">
                    <label className="block text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] ml-1">Link da sua loja</label>
                    <div className={cn(
                      "flex items-center bg-slate-900/50 border rounded-xl overflow-hidden transition-all relative",
                      errors.company_slug || slugStatus === 'unavailable' ? "border-red-500/50" : 
                      slugStatus === 'available' ? "border-green-500/50" : "border-slate-800 focus-within:border-orange-500"
                    )}>
                      <div className="bg-slate-900 px-4 py-3.5 border-r border-slate-800">
                        <span className="text-slate-500 font-bold text-sm">mesaflow.com/</span>
                      </div>
                      <input 
                        {...register("company_slug")} 
                        className="flex-1 bg-transparent py-3.5 px-4 text-white outline-none font-bold text-sm placeholder:text-slate-700" 
                        placeholder="link-da-loja" 
                        autoComplete="off"
                        onChange={(e) => {
                          setSlugManuallyEdited(true);
                          register("company_slug").onChange(e);
                        }}
                      />
                      <div className="absolute right-4">
                        {slugStatus === 'checking' && <Loader2 className="animate-spin text-slate-500" size={16} />}
                        {slugStatus === 'available' && <CheckCircle2 className="text-green-500" size={16} />}
                        {slugStatus === 'unavailable' && <XCircle className="text-red-500" size={16} />}
                      </div>
                    </div>
                    {slugStatus === 'unavailable' && <p className="text-red-400 text-xs font-bold ml-1 mt-1">Este link já está em uso.</p>}
                    {errors.company_slug && <p className="text-red-400 text-xs font-bold ml-1 mt-1">{errors.company_slug.message}</p>}
                  </div>

                  <button
                    type="button"
                    onClick={handleNextStep}
                    disabled={slugStatus === 'unavailable'}
                    className="w-full bg-orange-600 hover:bg-orange-500 text-white font-bold py-4 rounded-xl shadow-lg shadow-orange-900/20 hover:shadow-orange-900/40 active:scale-[0.98] transition-all flex items-center justify-center gap-2 mt-4 uppercase tracking-widest text-xs disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Próximo <ArrowRight size={18} />
                  </button>
                </motion.div>
              )}

              {step === 2 && (
                <motion.div
                  key="step2"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="space-y-5"
                >
                  <div className="grid grid-cols-2 gap-4">
                    <AuthInput 
                      label="Seu Cargo" 
                      icon={User} 
                      placeholder="Ex: Gerente" 
                      error={errors.owner_role?.message}
                      autoComplete="organization-title"
                      {...register("owner_role")} 
                    />
                    <AuthInput 
                      label="WhatsApp" 
                      icon={Phone} 
                      placeholder="(00) 00000-0000" 
                      error={errors.owner_phone?.message} 
                      autoComplete="tel"
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
                    autoComplete="email"
                    {...register("owner_email")} 
                  />

                  <div className="space-y-2">
                    <AuthInput 
                      label="Senha de Acesso" 
                      type="password" 
                      icon={Lock} 
                      placeholder="Mínimo 8 caracteres" 
                      error={errors.password?.message} 
                      autoComplete="new-password"
                      {...register("password")} 
                    />
                    {watchedPassword && (
                      <div className="flex gap-1 h-1.5 px-1 mt-2">
                        {[1, 2, 3, 4].map((s) => (
                          <div 
                            key={s} 
                            className={cn(
                              "flex-1 rounded-full transition-all duration-500",
                              s <= passwordStrength ? getStrengthColor() : "bg-slate-800"
                            )}
                          />
                        ))}
                      </div>
                    )}
                  </div>
                  
                  <div className="flex gap-3 mt-6">
                    <button
                      type="button"
                      onClick={() => setStep(1)}
                      className="flex-1 bg-slate-800 hover:bg-slate-700 text-white font-bold py-4 rounded-xl transition-all uppercase tracking-widest text-xs"
                    >
                      Voltar
                    </button>
                    <button
                      type="submit"
                      disabled={isSubmitting}
                      className="flex-[2] bg-orange-600 hover:bg-orange-500 text-white font-bold py-4 rounded-xl shadow-lg shadow-orange-900/20 hover:shadow-orange-900/40 active:scale-[0.98] transition-all flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed uppercase tracking-widest text-xs"
                    >
                      {isSubmitting ? <Loader2 className="animate-spin" size={18} /> : <>Finalizar <CheckCircle2 size={18} /></>}
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </form>

          <div className="mt-10 text-center">
            <p className="text-slate-500 text-sm font-medium">
              Já tem uma conta?{" "}
              <Link href="/admin/login" className="text-orange-500 font-bold hover:text-orange-400 transition-colors inline-flex items-center gap-1 hover:underline underline-offset-4 decoration-2">
                Fazer Login <ChevronRight size={14} />
              </Link>
            </p>
          </div>
        </div>
      </motion.div>

      {/* --- LADO DIREITO: VISUAL DINÂMICO --- */}
      <div className="hidden lg:flex lg:w-1/2 bg-slate-900 relative overflow-hidden border-l border-slate-800">
        <AnimatePresence mode="wait">
          <motion.div
            key={watchedSegment}
            initial={{ opacity: 0, scale: 1.05 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.8, ease: "easeInOut" }}
            className="absolute inset-0"
          >
            {/* Imagem de Fundo */}
            <div 
              className="absolute inset-0 bg-cover bg-center opacity-40" 
              style={{ backgroundImage: `url('${segmentAssets[watchedSegment].image}')` }} 
            />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/50 to-transparent" />
            
            {/* Conteúdo Flutuante */}
            <div className="relative z-10 flex flex-col justify-end p-20 h-full">
              <motion.div
                initial={{ y: 30, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.3, duration: 0.6 }}
              >
                <div className="inline-flex items-center gap-2 bg-orange-600/20 border border-orange-500/30 px-4 py-2 rounded-full text-orange-400 text-xs font-black uppercase tracking-widest mb-6 backdrop-blur-md">
                  <Store size={14} /> Solução Especializada
                </div>
                <h2 className="text-5xl xl:text-6xl font-black text-white mb-8 leading-[1.1] tracking-tight">
                  {segmentAssets[watchedSegment].title}
                </h2>
                <ul className="space-y-5">
                  {segmentAssets[watchedSegment].features.map((feat, i) => (
                    <motion.li 
                      key={i} 
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.5 + (i * 0.1) }}
                      className="flex items-center gap-4 text-slate-200 text-lg font-medium"
                    >
                      <div className="bg-emerald-500/20 p-1.5 rounded-full border border-emerald-500/30">
                        <CheckCircle2 className="text-emerald-500" size={20}/>
                      </div>
                      {feat}
                    </motion.li>
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

// FIX: Exportação Default Obrigatória para Next.js App Router
export default function RegisterPageWrapper() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-slate-950 flex items-center justify-center text-white font-bold">Carregando MesaFlow...</div>}>
      <RegisterForm />
    </Suspense>
  );
}
