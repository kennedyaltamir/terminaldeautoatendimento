import React from "react";
import Link from "next/link";
import { ShieldCheck, Activity, Lock, ArrowLeft, ChefHat } from "lucide-react";

export default function TrustLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gray-50 font-sans text-gray-900">
      {/* Header Simplificado */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 group">
            <div className="bg-orange-600 p-1.5 rounded-lg group-hover:scale-105 transition-transform">
              <ChefHat className="text-white w-5 h-5" />
            </div>
            <span className="font-bold text-lg tracking-tight">MesaFlow <span className="text-gray-400 font-normal">Trust Center</span></span>
          </Link>

          <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-gray-600">
            <Link href="/trust" className="hover:text-orange-600 transition-colors">Visão Geral</Link>
            <Link href="/trust/status" className="hover:text-orange-600 transition-colors">Status do Sistema</Link>
            <Link href="/trust/security" className="hover:text-orange-600 transition-colors">Segurança & Compliance</Link>
          </nav>

          <Link href="/" className="text-sm font-medium text-gray-500 hover:text-gray-900 flex items-center gap-1">
            <ArrowLeft size={16} /> Voltar
          </Link>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-12">
        {children}
      </main>

      <footer className="bg-white border-t border-gray-200 py-12 mt-12">
        <div className="max-w-5xl mx-auto px-6 text-center">
          <div className="flex justify-center gap-8 mb-8">
            <div className="flex flex-col items-center gap-2">
              <ShieldCheck className="text-green-600" size={24} />
              <span className="text-xs font-bold text-gray-500">LGPD Compliant</span>
            </div>
            <div className="flex flex-col items-center gap-2">
              <Lock className="text-blue-600" size={24} />
              <span className="text-xs font-bold text-gray-500">TLS 1.2+ Encryption</span>
            </div>
            <div className="flex flex-col items-center gap-2">
              <Activity className="text-orange-600" size={24} />
              <span className="text-xs font-bold text-gray-500">99.9% Uptime SLA</span>
            </div>
          </div>
          <p className="text-sm text-gray-400">
            © 2026 MesaFlow Tecnologia. Segurança é nossa prioridade.
          </p>
        </div>
      </footer>
    </div>
  );
}