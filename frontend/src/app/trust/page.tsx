import React from "react";
import Link from "next/link";
import { Activity, Shield, FileText, CheckCircle2, Server, Lock } from "lucide-react";
import { Metadata } from "next";

// FIX: Importação correta do SovereignPageFactory não é necessária aqui pois é uma página estática/server component simples.
// Se houver erro de "is not a function" aqui, é porque algum componente filho ou layout está tentando usar algo quebrado.
// Vamos garantir que esta página seja simples e robusta.

export const metadata: Metadata = {
  title: "Trust Center | MesaFlow",
  description: "Transparência sobre segurança, privacidade e disponibilidade do MesaFlow.",
};

export default function TrustCenterPage() {
  return (
    <div className="space-y-12 animate-in fade-in duration-500">
      <div className="text-center max-w-2xl mx-auto">
        <h1 className="text-4xl font-black text-gray-900 mb-4">Segurança e Confiança</h1>
        <p className="text-lg text-gray-600">
          O MesaFlow é construído com segurança em primeiro lugar. Aqui você encontra informações em tempo real sobre nossa infraestrutura, conformidade e políticas.
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Card Status */}
        <Link href="/trust/status" className="group bg-white p-8 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-all hover:border-orange-200">
          <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center text-green-600 mb-6 group-hover:scale-110 transition-transform">
            <Activity size={24} />
          </div>
          <h2 className="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
            Status Operacional <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">Ao Vivo</span>
          </h2>
          <p className="text-gray-500 mb-4">
            Verifique a disponibilidade dos nossos serviços, API e latência em tempo real.
          </p>
          <span className="text-orange-600 font-bold text-sm group-hover:underline">Ver status do sistema &rarr;</span>
        </Link>

        {/* Card Segurança */}
        <Link href="/trust/security" className="group bg-white p-8 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-all hover:border-blue-200">
          <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center text-blue-600 mb-6 group-hover:scale-110 transition-transform">
            <Shield size={24} />
          </div>
          <h2 className="text-xl font-bold text-gray-900 mb-2">Segurança & Compliance</h2>
          <p className="text-gray-500 mb-4">
            Detalhes sobre nossa arquitetura de segurança, criptografia, LGPD e políticas de proteção de dados.
          </p>
          <span className="text-blue-600 font-bold text-sm group-hover:underline">Ler políticas de segurança &rarr;</span>
        </Link>
      </div>

      <div className="bg-gray-900 text-white rounded-3xl p-8 md:p-12">
        <div className="grid md:grid-cols-3 gap-8">
          <div>
            <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
              <Server className="text-orange-500" /> Infraestrutura
            </h3>
            <ul className="space-y-3 text-gray-400 text-sm">
              <li className="flex items-center gap-2"><CheckCircle2 size={16} className="text-green-500"/> Hospedagem em Tier 1 (AWS/Render)</li>
              <li className="flex items-center gap-2"><CheckCircle2 size={16} className="text-green-500"/> Banco de Dados com RLS</li>
              <li className="flex items-center gap-2"><CheckCircle2 size={16} className="text-green-500"/> Backups Automáticos (PITR)</li>
            </ul>
          </div>
          <div>
            <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
              <Lock className="text-blue-500" /> Proteção de Dados
            </h3>
            <ul className="space-y-3 text-gray-400 text-sm">
              <li className="flex items-center gap-2"><CheckCircle2 size={16} className="text-green-500"/> Criptografia TLS 1.2+</li>
              <li className="flex items-center gap-2"><CheckCircle2 size={16} className="text-green-500"/> Dados em Repouso Criptografados</li>
              <li className="flex items-center gap-2"><CheckCircle2 size={16} className="text-green-500"/> Isolamento Multi-tenant Lógico</li>
            </ul>
          </div>
          <div>
            <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
              <FileText className="text-purple-500" /> Conformidade
            </h3>
            <ul className="space-y-3 text-gray-400 text-sm">
              <li className="flex items-center gap-2"><CheckCircle2 size={16} className="text-green-500"/> LGPD Ready</li>
              <li className="flex items-center gap-2"><CheckCircle2 size={16} className="text-green-500"/> PCI-DSS Compliant (Pagamentos)</li>
              <li className="flex items-center gap-2"><CheckCircle2 size={16} className="text-green-500"/> Auditoria de Logs Imutável</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
