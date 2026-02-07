/**
 * DOMAIN: FRONTEND
 * OBJECTIVE: Dashboard Logic Hook.
 * FIX: Unified Metrics type with @/types to resolve TS2345.
 */
import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { getDashboardMetrics } from "@/lib/api";
import { toast } from "sonner";
import { Metrics } from "@/types"; // 🛡️ FIX: Usando tipo centralizado

export type Period = "today" | "7d" | "30d" | "month";

export function useDashboardStats(slug: string) {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState<Period>("7d");
  const router = useRouter();

  const fetchMetrics = useCallback(async () => {
    setLoading(true);
    const now = new Date();
    let startDate = "";
    const endDate = now.toISOString().split("T")[0];

    if (period === "today") {
      startDate = endDate;
    } else if (period === "7d") {
      const past = new Date();
      past.setDate(now.getDate() - 6);
      startDate = past.toISOString().split("T")[0];
    } else if (period === "30d") {
      const past = new Date();
      past.setDate(now.getDate() - 29);
      startDate = past.toISOString().split("T")[0];
    } else if (period === "month") {
      const firstDay = new Date(now.getFullYear(), now.getMonth(), 1);
      startDate = firstDay.toISOString().split("T")[0];
    }

    try {
      const data = await getDashboardMetrics(startDate, endDate);
      setMetrics(data);
    } catch (err: any) {
      if (err.status === 401 || err.status === 403) {
        toast.error("Sessão expirada. Redirecionando...");
        router.push("/admin/login");
      } else {
        toast.error("Erro ao carregar métricas.");
      }
    } finally {
      setLoading(false);
    }
  }, [period, router]);

  const handleExport = async () => {
    try {
      const token = localStorage.getItem("mesaflow_access_token");
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/metrics/export`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) throw new Error();
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `vendas_${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      toast.success("Relatório exportado!");
    } catch (e) {
      toast.error("Erro na exportação.");
    }
  };

  useEffect(() => {
    if (slug) fetchMetrics();
  }, [slug, fetchMetrics]);

  return { metrics, loading, period, setPeriod, handleExport, refresh: fetchMetrics };
}
