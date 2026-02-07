"use client";

import { useEffect, useState } from "react";
import { CheckCircle2, XCircle, Loader2, Server, Database, Activity } from "lucide-react";

// FIX: Remoção de dependências quebradas. Página autossuficiente.

interface HealthData {
  status: string;
  timestamp: number;
  services: {
    database: string;
    redis: string;
  };
}

export default function StatusPage() {
  const [health, setHealth] = useState<HealthData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/health`);
        if (!res.ok) throw new Error("Falha no health check");
        const data = await res.json();
        setHealth(data);
        setError(false);
      } catch (e) {
        console.error("Health Check Error:", e);
        setError(true);
      } finally {
        setLoading(false);
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const StatusIndicator = ({ status }: { status: string | undefined }) => {
    const isUp = status === "up" || status === "healthy";
    return (
      <span className={`flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold uppercase ${isUp ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
        {isUp ? <CheckCircle2 size={14} /> : <XCircle size={14} />}
        {isUp ? "Operacional" : "Instabilidade"}
      </span>
    );
  };

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4">
      <div className="text-center mb-12">
        <h1 className="text-3xl font-bold text-gray-900">Status do Sistema</h1>
        <p className="text-gray-500 mt-2">Monitoramento em tempo real da infraestrutura MesaFlow.</p>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-20 text-gray-400">
          <Loader2 className="animate-spin mb-4" size={48} />
          <p>Verificando sinais vitais...</p>
        </div>
      ) : error ? (
        <div className="bg-red-50 border border-red-200 rounded-2xl p-8 text-center">
          <XCircle className="text-red-500 w-16 h-16 mx-auto mb-4" />
          <h3 className="text-xl font-bold text-red-700">Sistema Indisponível</h3>
          <p className="text-red-600 mt-2">Não foi possível conectar aos servidores de monitoramento.</p>
        </div>
      ) : (
        <div className="grid gap-6 max-w-2xl mx-auto">
          <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="bg-green-100 p-3 rounded-full text-green-600">
                <Activity size={24} />
              </div>
              <div>
                <h3 className="font-bold text-gray-900">API Gateway</h3>
                <p className="text-xs text-gray-500">Latência normal</p>
              </div>
            </div>
            <StatusIndicator status={health?.status} />
          </div>

          <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="bg-blue-100 p-3 rounded-full text-blue-600">
                <Database size={24} />
              </div>
              <div>
                <h3 className="font-bold text-gray-900">Banco de Dados (PostgreSQL)</h3>
                <p className="text-xs text-gray-500">Neon Serverless</p>
              </div>
            </div>
            <StatusIndicator status={health?.services?.database} />
          </div>

          <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="bg-red-100 p-3 rounded-full text-red-600">
                <Server size={24} />
              </div>
              <div>
                <h3 className="font-bold text-gray-900">Real-time (Redis)</h3>
                <p className="text-xs text-gray-500">WebSockets & Pub/Sub</p>
              </div>
            </div>
            <StatusIndicator status={health?.services?.redis} />
          </div>

          <p className="text-center text-xs text-gray-400 mt-8">
            Última verificação: {new Date(health?.timestamp ? health.timestamp * 1000 : Date.now()).toLocaleString()}
          </p>
        </div>
      )}
    </div>
  );
}
