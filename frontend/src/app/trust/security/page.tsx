import React from "react";
import { Shield, Lock, Eye, FileText, AlertTriangle, Check } from "lucide-react";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Segurança | MesaFlow Trust Center",
  description: "Políticas de segurança, conformidade e proteção de dados.",
};

export default function SecurityPage() {
  return (
    <div className="space-y-12 animate-in fade-in duration-500">
      <div className="text-center max-w-3xl mx-auto">
        <h1 className="text-4xl font-black text-gray-900 mb-4">Segurança em Profundidade</h1>
        <p className="text-lg text-gray-600">
          Nossa arquitetura segue os princípios de "Security by Design". Protegemos seus dados com camadas de defesa redundantes.
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm">
          <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center text-blue-600 mb-6">
            <Shield size={24} />
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-4">Isolamento de Dados (RLS)</h3>
          <p className="text-gray-600 text-sm leading-relaxed mb-4">
            Utilizamos <strong>Row-Level Security</strong> nativo do PostgreSQL. Isso garante que os dados de cada cliente estejam isolados logicamente no nível do banco de dados. Mesmo em caso de falha na aplicação, o banco impede o acesso cruzado entre tenants.
          </p>
          <ul className="space-y-2 text-sm text-gray-500">
            <li className="flex items-center gap-2"><Check size={14} className="text-green-500"/> Políticas de acesso estritas</li>
            <li className="flex items-center gap-2"><Check size={14} className="text-green-500"/> Contexto de sessão obrigatório</li>
          </ul>
        </div>

        <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm">
          <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center text-green-600 mb-6">
            <Lock size={24} />
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-4">Criptografia</h3>
          <p className="text-gray-600 text-sm leading-relaxed mb-4">
            Todos os dados em trânsito são protegidos por <strong>TLS 1.2+</strong>. Dados sensíveis em repouso (como tokens e chaves de API) são criptografados utilizando algoritmos padrão de mercado (AES-256).
          </p>
          <ul className="space-y-2 text-sm text-gray-500">
            <li className="flex items-center gap-2"><Check size={14} className="text-green-500"/> HTTPS Forçado (HSTS Preload)</li>
            <li className="flex items-center gap-2"><Check size={14} className="text-green-500"/> Gestão de Segredos via Env Vars</li>
          </ul>
        </div>

        <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm">
          <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center text-purple-600 mb-6">
            <Eye size={24} />
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-4">Auditoria e Logs</h3>
          <p className="text-gray-600 text-sm leading-relaxed mb-4">
            Ações críticas (login, alteração de permissões, exclusão de dados) são registradas em logs de auditoria imutáveis. Mantemos rastreabilidade total de quem fez o quê e quando.
          </p>
        </div>

        <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm">
          <div className="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center text-orange-600 mb-6">
            <FileText size={24} />
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-4">Conformidade Legal</h3>
          <p className="text-gray-600 text-sm leading-relaxed mb-4">
            Estamos em conformidade com a <strong>LGPD</strong> (Lei Geral de Proteção de Dados). Respeitamos os direitos dos titulares e mantemos políticas claras de retenção e descarte de dados.
          </p>
          <a href="/privacy" className="text-orange-600 font-bold text-sm hover:underline">Ler Política de Privacidade</a>
        </div>
      </div>

      <div className="bg-gray-900 text-white rounded-3xl p-8 md:p-12 flex flex-col md:flex-row items-center justify-between gap-8">
        <div>
          <h3 className="text-2xl font-bold mb-2 flex items-center gap-3">
            <AlertTriangle className="text-yellow-500" /> Reportar Vulnerabilidade
          </h3>
          <p className="text-gray-400 max-w-xl">
            Levamos a segurança a sério. Se você encontrou uma vulnerabilidade em nossos sistemas, por favor, nos informe imediatamente.
          </p>
        </div>
        <a 
          href="mailto:security@mesaflow.com.br"
          className="bg-white text-gray-900 px-8 py-4 rounded-xl font-bold hover:bg-gray-100 transition-colors shadow-lg"
        >
          security@mesaflow.com.br
        </a>
      </div>
    </div>
  );
}