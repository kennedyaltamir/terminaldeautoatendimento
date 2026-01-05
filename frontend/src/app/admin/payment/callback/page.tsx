"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { connectPaymentProvider } from "@/lib/api";
import { Loader2, CheckCircle2, XCircle } from "lucide-react";
import { toast, Toaster } from "sonner";

export default function PaymentCallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');

  useEffect(() => {
    const code = searchParams.get("code");
    const state = searchParams.get("state"); // ID da empresa (opcional validar)

    if (!code) {
      setStatus('error');
      return;
    }

    const connect = async () => {
      try {
        await connectPaymentProvider("mercadopago", code);
        setStatus('success');
        setTimeout(() => {
          // Redireciona de volta para as configurações da empresa
          // Precisamos descobrir o slug. Como não temos aqui, vamos para o dashboard e deixamos o middleware redirecionar se necessário
          // Ou melhor: voltamos para a última página visitada se possível, ou /admin/login que redireciona
          router.push("/admin/login"); 
        }, 2000);
      } catch (e) {
        console.error(e);
        setStatus('error');
      }
    };

    connect();
  }, [searchParams, router]);

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center text-white p-6">
      <Toaster position="top-center" richColors />
      
      <div className="bg-gray-800 p-8 rounded-2xl border border-gray-700 shadow-2xl text-center max-w-md w-full">
        {status === 'loading' && (
          <>
            <Loader2 className="w-16 h-16 text-blue-500 animate-spin mx-auto mb-6" />
            <h2 className="text-2xl font-bold mb-2">Conectando...</h2>
            <p className="text-gray-400">Estamos finalizando a integração com o Mercado Pago.</p>
          </>
        )}

        {status === 'success' && (
          <>
            <CheckCircle2 className="w-16 h-16 text-green-500 mx-auto mb-6" />
            <h2 className="text-2xl font-bold mb-2">Sucesso!</h2>
            <p className="text-gray-400">Sua conta foi conectada. Redirecionando...</p>
          </>
        )}

        {status === 'error' && (
          <>
            <XCircle className="w-16 h-16 text-red-500 mx-auto mb-6" />
            <h2 className="text-2xl font-bold mb-2">Erro na Conexão</h2>
            <p className="text-gray-400 mb-6">Não foi possível vincular sua conta. Tente novamente.</p>
            <button 
              onClick={() => router.back()}
              className="bg-gray-700 hover:bg-gray-600 text-white px-6 py-3 rounded-xl font-bold transition-colors"
            >
              Voltar
            </button>
          </>
        )}
      </div>
    </div>
  );
}