"use client";

import { useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Lock, Loader2, CheckCircle2 } from "lucide-react";
import { Toaster, toast } from "sonner";
import AuthInput from "@/components/ui/AuthInput";

const resetSchema = z.object({
  new_password: z.string().min(8, "Mínimo 8 caracteres"),
  confirm_password: z.string()
}).refine((data) => data.new_password === data.confirm_password, {
  message: "Senhas não conferem",
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
    if (!token) return toast.error("Token inválido.");

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/reset-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token, new_password: data.new_password })
      });

      if (res.ok) {
        setSuccess(true);
        setTimeout(() => router.push("/admin/login"), 3000);
      } else {
        const err = await res.json();
        toast.error(err.detail || "Erro ao redefinir senha.");
      }
    } catch (e) {
      toast.error("Erro de conexão.");
    }
  };

  if (!token) return <div className="text-red-500 text-center">Link inválido ou expirado.</div>;

  if (success) {
    return (
      <div className="text-center animate-in fade-in">
        <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4 text-green-600">
          <CheckCircle2 size={32} />
        </div>
        <h2 className="text-2xl font-bold text-gray-900">Senha Alterada!</h2>
        <p className="text-gray-500 mt-2">Redirecionando para o login...</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <AuthInput 
        label="Nova Senha" 
        type="password" 
        icon={Lock} 
        placeholder="******" 
        error={errors.new_password?.message}
        {...register("new_password")}
      />
      <AuthInput 
        label="Confirmar Senha" 
        type="password" 
        icon={Lock} 
        placeholder="******" 
        error={errors.confirm_password?.message}
        {...register("confirm_password")}
      />
      <button 
        type="submit" 
        disabled={isSubmitting}
        className="w-full bg-orange-600 text-white py-3 rounded-xl font-bold hover:bg-orange-700 transition-colors flex items-center justify-center gap-2 disabled:opacity-70"
      >
        {isSubmitting ? <Loader2 className="animate-spin" /> : "Salvar Nova Senha"}
      </button>
    </form>
  );
}

export default function ResetPasswordPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4">
      <Toaster position="top-center" richColors />
      <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8">
        <h1 className="text-2xl font-bold text-gray-900 text-center mb-8">Redefinir Senha</h1>
        <Suspense fallback={<div className="text-center">Carregando...</div>}>
          <ResetForm />
        </Suspense>
      </div>
    </div>
  );
}