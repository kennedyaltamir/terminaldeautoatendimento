"use client";
/**
 * @sentinel-title: Redefinir Senha
 * @sentinel-description: Criação de nova credencial de acesso após validação de token de segurança.
 */
import { useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Lock, Loader2, CheckCircle2, ArrowLeft } from "lucide-react";
import { Toaster, toast } from "sonner";
import AuthInput from "@/components/ui/AuthInput";
import Logo from "@/components/ui/Logo";
import Link from "next/link";

const resetSchema = z.object({
  new_password: z.string().min(8, "A senha deve ter no mínimo 8 caracteres"),
  confirm_password: z.string()
}).refine((data) => data.new_password === data.confirm_password, {
  message: "As senhas não conferem",
  path: ["confirm_password"],
});

type ResetSchema = z.infer<typeof resetSchema>;

function ResetForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
  const [success, setSuccess] = useState(false);

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<ResetSchema>({
    resolver: zodResolver(resetSchema)
  });

  const onSubmit = async (data: ResetSchema) => {
    if (!token) {
      toast.error("Token de recuperação ausente ou inválido.");
      return;
    }

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/reset-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token, new_password: data.new_password })
      });

      if (res.ok) {
        setSuccess(true);
        toast.success("Senha alterada com sucesso!");
        setTimeout(() => router.push("/admin/login"), 3000);
      } else {
        const err = await res.json();
        toast.error(err.detail || "Erro ao redefinir senha. O link pode ter expirado.");
      }
    } catch (e) {
      toast.error("Falha na conexão com o servidor.");
    }
  };

  if (!token) {
    return (
      <div className="text-center space-y-4 animate-in fade-in">
        <p className="text-red-500 font-bold">Link de recuperação inválido ou expirado.</p>
        <Link href="/admin/forgot-password" className="text-orange-500 hover:underline text-sm font-bold">
          Solicitar novo link
        </Link>
      </div>
    );
  }

  if (success) {
    return (
      <div className="text-center animate-in zoom-in duration-300">
        <div className="w-20 h-20 bg-emerald-500/10 text-emerald-500 rounded-full flex items-center justify-center mx-auto mb-6">
          <CheckCircle2 size={40} />
        </div>
        <h2 className="text-2xl font-black text-white">Senha Alterada!</h2>
        <p className="text-slate-400 text-sm mt-2">Sua nova credencial foi salva. Redirecionando para o login...</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="space-y-4">
        <AuthInput 
          label="Nova Senha" 
          type="password" 
          icon={Lock} 
          placeholder="••••••••" 
          error={errors.new_password?.message}
          {...register("new_password")}
        />
        <AuthInput 
          label="Confirmar Nova Senha" 
          type="password" 
          icon={Lock} 
          placeholder="••••••••" 
          error={errors.confirm_password?.message}
          {...register("confirm_password")}
        />
      </div>

      <button 
        type="submit" 
        disabled={isSubmitting}
        className="w-full bg-orange-600 hover:bg-orange-700 text-white font-black py-4 rounded-2xl shadow-lg shadow-orange-900/20 transition-all active:scale-[0.98] flex items-center justify-center gap-2 disabled:opacity-70"
      >
        {isSubmitting ? <Loader2 className="animate-spin" /> : "SALVAR NOVA SENHA"}
      </button>
    </form>
  );
}

export default function ResetPasswordPage() {
  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-6">
      <Toaster position="top-center" richColors />
      
      <div className="mb-12">
        <Logo size="lg" variant="light" animated />
      </div>

      <div className="w-full max-w-md bg-slate-900 border border-slate-800 p-8 rounded-[2.5rem] shadow-2xl">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-black text-white tracking-tight">Redefinir Senha</h1>
          <p className="text-slate-500 text-sm mt-1">Crie uma senha forte para proteger sua conta.</p>
        </div>

        <Suspense fallback={
          <div className="flex flex-col items-center py-10 gap-4">
            <Loader2 className="animate-spin text-orange-500" size={32} />
            <p className="text-slate-500 text-sm font-bold">Validando token...</p>
          </div>
        }>
          <ResetForm />
        </Suspense>

        <div className="mt-8 text-center">
          <Link href="/admin/login" className="text-xs font-bold text-slate-600 hover:text-slate-400 transition-colors flex items-center justify-center gap-2">
            <ArrowLeft size={14} /> Voltar para o Login
          </Link>
        </div>
      </div>
    </div>
  );
}