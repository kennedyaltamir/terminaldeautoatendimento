"use client";
import { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";

export default function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const faqs = [
    { q: "Preciso comprar equipamentos específicos?", a: "Não. O MesaFlow roda em qualquer dispositivo com navegador (celular, tablet, notebook). Você pode usar o que já tem." },
    { q: "Funciona se a internet cair?", a: "O sistema precisa de internet para processar pagamentos e sincronizar a cozinha. Recomendamos ter um 4G de backup. O modo offline permite lançar pedidos, mas a sincronização ocorre quando a rede volta." },
    { q: "Emite Nota Fiscal?", a: "Sim, no plano Enterprise temos integração direta com emissores de NFC-e e SAT via parceiros (eNotas/Focus)." },
    { q: "Posso usar meu próprio domínio?", a: "Sim, oferecemos White Label completo no plano Enterprise (ex: pedidos.suamarca.com)." },
    { q: "Tem fidelidade ou multa de cancelamento?", a: "Não. Você pode cancelar a qualquer momento diretamente pelo painel administrativo, sem falar com ninguém." },
    { q: "Integra com iFood?", a: "A integração direta está em nosso roadmap para o próximo trimestre. Por enquanto, você pode usar o MesaFlow para sua operação de salão e delivery próprio." },
    { q: "Como funciona o suporte?", a: "Clientes Pro e Enterprise têm acesso a suporte prioritário via WhatsApp. Clientes Start contam com nossa base de conhecimento e suporte por e-mail." },
  ];

  return (
    <section className="py-24 bg-gray-50">
      <div className="max-w-3xl mx-auto px-6">
        <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">Perguntas Frequentes</h2>
        <div className="space-y-4">
          {faqs.map((faq, i) => (
            <div key={i} className="bg-white rounded-xl border border-gray-200 overflow-hidden">
              <button 
                onClick={() => setOpenIndex(openIndex === i ? null : i)}
                className="w-full flex justify-between items-center p-6 text-left font-bold text-gray-800 hover:bg-gray-50 transition-colors"
              >
                {faq.q}
                {openIndex === i ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
              </button>
              {openIndex === i && (
                <div className="p-6 pt-0 text-gray-600 leading-relaxed border-t border-gray-100">
                  {faq.a}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}