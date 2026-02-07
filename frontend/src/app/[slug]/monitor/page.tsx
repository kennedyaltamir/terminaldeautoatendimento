/**
 * Author: MESAFLOW_AI
 * Version: 11.1 (Next.js 16 Hardened)
 * DNA_ID: monitor-page-v11-1
 * Objective: Fix params.slug Promise access and prevent undefined API calls.
 */
import { use } from "react";
import PublicMonitorView from "@/components/menu/PublicMonitorView";

export default function PublicMonitorPage({ params: paramsPromise }: { params: Promise<{ slug: string }> }) {
  // 🛡️ PROTOCOLO NEXT 16: Unwrapping obrigatório da Promise de params
  const params = use(paramsPromise);
  const slug = params.slug;

  return (
    <main className="min-h-screen bg-black">
      {slug && slug !== "undefined" ? (
        <PublicMonitorView slug={slug} />
      ) : (
        <div className="flex h-screen items-center justify-center text-white font-mono">
          [ERROR] INVALID_TENANT_CONTEXT
        </div>
      )}
    </main>
  );
}