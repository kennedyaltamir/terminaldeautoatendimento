"use client";
import { useState } from "react";
import { Utensils, Ticket, Building2, Briefcase } from "lucide-react";

export default function UseCases() {
  const [activeTab, setActiveTab] = useState("restaurantes");

  const cases = {
    restaurantes: {
      icon: Utensils,
      title: "Gastronomia & Bares",
      desc: "Transforme mesas em pontos de venda autônomos. Aumente o giro de mesa e o ticket médio com upsell automático.",
      features: ["Cardápio Digital QR", "KDS de Cozinha", "Fidelidade Integrada"]
    },
    eventos: {
      icon: Ticket,
      title: "Estádios & Eventos",
      desc: "Venda alimentos e bebidas diretamente da cadeira ou camarote. Reduza filas nos intervalos e aumente a receita.",
      features: ["Mapeamento de Assentos", "Fila Expressa", "Pagamento Pix Instantâneo"]
    },
    hoteis: {
      icon: Building2,
      title: "Hotéis & Resorts",
      desc: "Room Service moderno. O hóspede pede da piscina ou do quarto sem precisar ligar para a recepção.",
      features: ["Pedidos por Quarto", "Agendamento", "Cardápio Multilíngue"]
    },
    corporativo: {
      icon: Briefcase,
      title: "Food Halls & Corporativo",
      desc: "Centralize múltiplos restaurantes em um único sistema de pagamento e gestão para praças de alimentação.",
      features: ["Split de Pagamento", "Gestão Multi-loja", "Totem de Autoatendimento"]
    }
  };

  return (
    <section id="solucoes" className="py-24 bg-gray-50">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Um sistema, múltiplos cenários.</h2>
          <p className="text-gray-600 max-w-2xl mx-auto">O MesaFlow se adapta ao fluxo do seu negócio, não o contrário.</p>
        </div>

        <div className="grid md:grid-cols-12 gap-8">
          {/* Menu Lateral */}
          <div className="md:col-span-4 space-y-2">
            {Object.entries(cases).map(([key, value]) => {
              const Icon = value.icon;
              const isActive = activeTab === key;
              return (
                <button
                  key={key}
                  onClick={() => setActiveTab(key)}
                  className={`w-full text-left p-4 rounded-xl flex items-center gap-4 transition-all duration-300 ${isActive ? 'bg-white shadow-lg border-l-4 border-orange-500' : 'hover:bg-white/50 text-gray-600'}`}
                >
                  <div className={`p-2 rounded-lg ${isActive ? 'bg-orange-100 text-orange-600' : 'bg-gray-100'}`}>
                    <Icon size={24} />
                  </div>
                  <span className={`font-bold ${isActive ? 'text-gray-900' : 'text-gray-600'}`}>{value.title}</span>
                </button>
              );
            })}
          </div>

          {/* Conteúdo */}
          <div className="md:col-span-8 bg-white rounded-2xl p-8 md:p-12 shadow-xl border border-gray-100 flex flex-col justify-center min-h-[400px] animate-in fade-in slide-in-from-right-4 duration-500 key={activeTab}">
            {/* @ts-ignore */}
            <h3 className="text-3xl font-bold text-gray-900 mb-4">{cases[activeTab].title}</h3>
            {/* @ts-ignore */}
            <p className="text-lg text-gray-600 mb-8 leading-relaxed">{cases[activeTab].desc}</p>
            
            <div className="grid sm:grid-cols-3 gap-4">
              {/* @ts-ignore */}
              {cases[activeTab].features.map((feature, i) => (
                <div key={i} className="bg-gray-50 p-4 rounded-xl border border-gray-100 font-medium text-gray-700 flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-orange-500"></div>
                  {feature}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}