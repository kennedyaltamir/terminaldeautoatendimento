/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 2.0.0 (Enterprise Compliance)
 * Objective: Professional Privacy Policy with high-fidelity layout.
 */
import React from "react";
import { ShieldCheck, Lock, Eye, FileText, Globe, UserCheck, Mail } from "lucide-react";

export default function PrivacyPage() {
  const sections = [
    { id: "coleta", title: "1. Coleta de Dados", icon: Globe, content: "Coletamos dados de identificação (nome, telefone) e metadados de transação para garantir a segurança e a entrega dos pedidos realizados via cardápio digital ou totem." },
    { id: "uso", title: "2. Finalidade do Uso", icon: UserCheck, content: "Os dados são processados para: (a) Execução de contratos de compra e venda; (b) Gestão de programas de fidelidade; (c) Prevenção a fraudes financeiras no rito do Pix." },
    { id: "seguranca", title: "3. Segurança Soberana", icon: Lock, content: "Utilizamos criptografia de ponta a ponta (TLS 1.2+) e isolamento lógico de dados (Row-Level Security) para garantir que as informações de um restaurante nunca sejam acessíveis por outro." },
    { id: "direitos", title: "4. Seus Direitos (LGPD)", icon: ShieldCheck, content: "Você tem o direito de solicitar a exclusão, correção ou portabilidade dos seus dados a qualquer momento através dos nossos canais oficiais." }
  ];

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      <div className="max-w-6xl mx-auto px-6 py-20 grid md:grid-cols-4 gap-12">
        {/* Sidebar de Navegação */}
        <aside className="hidden md:block space-y-4 sticky top-20 h-fit">
          <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mb-6">Conteúdo</p>
          {sections.map(s => (
            <a key={s.id} href={`#${s.id}`} className="block text-sm font-bold text-slate-500 hover:text-orange-600 transition-colors">
              {s.title}
            </a>
          ))}
        </aside>

        {/* Conteúdo Principal */}
        <main className="md:col-span-3 space-y-16">
          <header className="border-b border-slate-200 pb-10">
            <div className="inline-flex p-3 bg-orange-600 text-white rounded-2xl mb-6 shadow-lg shadow-orange-200">
              <ShieldCheck size={32} />
            </div>
            <h1 className="text-5xl font-black tracking-tight text-slate-900 mb-4">Política de Privacidade</h1>
            <p className="text-slate-500 font-medium">MesaFlow OS • Versão 2026.1 • Atualizado em 03/02/2026</p>
          </header>

          <div className="space-y-12">
            {sections.map(s => (
              <section key={s.id} id={s.id} className="scroll-mt-24">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 bg-slate-100 rounded-lg text-slate-600">
                    <s.icon size={20} />
                  </div>
                  <h2 className="text-xl font-black uppercase tracking-tight">{s.title}</h2>
                </div>
                <p className="text-slate-600 leading-relaxed text-lg">
                  {s.content}
                </p>
              </section>
            ))}
          </div>

          <footer className="bg-slate-900 rounded-[2.5rem] p-10 text-white relative overflow-hidden">
            <div className="absolute top-0 right-0 p-10 opacity-10">
              <FileText size={120} />
            </div>
            <h3 className="text-2xl font-bold mb-4">Dúvidas sobre Privacidade?</h3>
            <p className="text-slate-400 mb-8 max-w-md">Nosso Encarregado de Proteção de Dados (DPO) está à disposição para esclarecimentos.</p>
            <a href="mailto:dpo@mesaflow.com.br" className="inline-flex items-center gap-2 bg-orange-600 px-6 py-3 rounded-xl font-bold hover:bg-orange-700 transition-all">
              <Mail size={18} /> dpo@mesaflow.com.br
            </a>
          </footer>
        </main>
      </div>
    </div>
  );
}
