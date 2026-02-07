"use client";

import { X, Utensils, Building2, Ticket, Briefcase, ArrowRight } from "lucide-react";
import Link from "next/link";

interface DemoModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function DemoModal({ isOpen, onClose }: DemoModalProps) {
  if (!isOpen) return null;

  const demos = [
    {
      id: "gastro",
      title: "Restaurante & Bar",
      icon: Utensils,
      desc: "Cardápio digital, KDS e gestão de mesas.",
      color: "bg-orange-100 text-orange-600",
      link: "/hamburgueria-ze/menu"
    },
    {
      id: "hotel",
      title: "Hotelaria",
      icon: Building2,
      desc: "Room Service e pedidos na piscina.",
      color: "bg-blue-100 text-blue-600",
      link: "/demo-hotel/menu"
    },
    {
      id: "event",
      title: "Eventos & Estádios",
      icon: Ticket,
      desc: "Venda no assento e filas expressas.",
      color: "bg-purple-100 text-purple-600",
      link: "/demo-evento/menu"
    },
    {
      id: "corp",
      title: "Corporativo",
      icon: Briefcase,
      desc: "Coffee break e praças de alimentação.",
      color: "bg-green-100 text-green-600",
      link: "/demo-corp/menu"
    }
  ];

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in">
      <div className="bg-white w-full max-w-4xl rounded-3xl p-8 shadow-2xl relative overflow-hidden">
        <button onClick={onClose} className="absolute top-6 right-6 text-gray-400 hover:text-gray-600 transition-colors">
          <X size={24} />
        </button>

        <div className="text-center mb-10">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Escolha sua Experiência</h2>
          <p className="text-gray-500">Veja como o MesaFlow se adapta ao seu modelo de negócio.</p>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          {demos.map((demo) => (
            <Link 
              key={demo.id} 
              href={demo.link}
              target="_blank"
              className="flex items-center gap-4 p-6 rounded-2xl border border-gray-100 hover:border-gray-300 hover:shadow-lg transition-all group bg-gray-50 hover:bg-white"
            >
              <div className={`w-16 h-16 rounded-xl flex items-center justify-center ${demo.color} group-hover:scale-110 transition-transform`}>
                <demo.icon size={32} />
              </div>
              <div className="flex-1">
                <h3 className="font-bold text-lg text-gray-900 group-hover:text-orange-600 transition-colors">{demo.title}</h3>
                <p className="text-sm text-gray-500">{demo.desc}</p>
              </div>
              <ArrowRight className="text-gray-300 group-hover:text-orange-500 transition-colors" />
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}