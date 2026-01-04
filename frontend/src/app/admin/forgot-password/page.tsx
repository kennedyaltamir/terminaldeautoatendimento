"use client";

import { useState } from "react";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { ChefHat, ArrowLeft, Mail, Loader2, CheckCircle2 } from "lucide-react";
import { Toaster, toast } from "sonner";
import AuthInput from "@/components/ui/AuthInput";

const forgotSchema = z.object({
  email: z.string().email("E-mail inválido"),
});

type ForgotSchema = z.infer<typeof forgotSchema>;

export default function ForgotPasswordPage() {
  const [isSent, setIsSent] = useState(false);
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<ForgotSchema>({
    resolver: zodResolver(forgotSchema)
  });

  const onSubmit = async (data: ForgotSchema) => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/forgot-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      
      if (res.ok) {
        setIsSent(true);
      } else {
        toast.error("Erro ao solicitar recuperação.");
      }
    } catch (e) {
      toast.error("Erro de conexão.");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4">
      <Toaster position="top-center" richColors />
      
      <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8">
        <div className="text-center mb-8">
          <div className="bg-orange-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 text-orange-600">
            <ChefHat size={32} />
          </div>
          <h1 className="text-2xl font-bold text-gray-900">Recuperar Senha</h1>
          <p className="text-gray-500 text-sm mt-2">Digite seu e-mail para receber o link de redefinição.</p>
        </div>

        {isSent ? (
          <div className="text-center animate-in fade-in">
            <div className="bg-green-100 text-green-700 p-4 rounded-xl mb-6 flex items-center gap-3">
              <CheckCircle2 size={24} />
              <p className="text-sm font-medium text-left">Se o e-mail estiver cadastrado, você receberá as instruções em instantes.</p>
            </div>
            <Link href="/admin/login" className="text-orange-600 font-bold hover:underline">Voltar para Login</Link>
          </div>
        ) : (
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <AuthInput 
              label="E-mail" 
              icon={Mail} 
              placeholder="seu@email.com" 
              error={errors.email?.message}
              {...register("email")}
            />
            
            <button 
              type="submit" 
              disabled={isSubmitting}
              className="w-full bg-orange-600 text-white py-3 rounded-xl font-bold hover:bg-orange-700 transition-colors flex items-center justify-center gap-2 disabled:opacity-70"
            >
              {isSubmitting ? <Loader2 className="animate-spin" /> : "Enviar Link"}
            </button>
            
            <div className="text-center">
              <Link href="/admin/login" className="text-gray-500 text-sm hover:text-gray-900 flex items-center justify-center gap-2">
                <ArrowLeft size={16} /> Voltar
              </Link>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}