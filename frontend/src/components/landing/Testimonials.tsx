import { Star, Quote } from "lucide-react";

const reviews = [
  { name: "Carlos M.", role: "Dono do Burger King (Franquia)", text: "Reduzimos o tempo de fila em 40% no primeiro mês. O KDS é instantâneo.", stars: 5 },
  { name: "Ana S.", role: "Produtora do Festival Verão", text: "O modo offline salvou nosso evento quando o 4G caiu. Incrível.", stars: 5 },
  { name: "Roberto F.", role: "Gerente Hotel Ibis", text: "O Room Service via QR Code aumentou o ticket médio em 25%.", stars: 5 },
  { name: "Julia P.", role: "CEO Food Hall SP", text: "A gestão multi-loja é perfeita. Consigo ver o faturamento de todos em tempo real.", stars: 5 },
  { name: "Marcos T.", role: "Arena Corinthians (Bar)", text: "Vendemos 5.000 cervejas em 2 horas sem travar o sistema.", stars: 5 },
];

export default function Testimonials() {
  return (
    <section className="py-24 bg-gray-50 overflow-hidden">
      <div className="max-w-7xl mx-auto px-6 text-center mb-16">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">Quem usa, escala.</h2>
        <p className="text-gray-600">Junte-se a operações de alto volume que confiam no MesaFlow.</p>
      </div>

      <div className="relative flex overflow-x-hidden group">
        <div className="animate-scroll whitespace-nowrap flex gap-6">
          {[...reviews, ...reviews, ...reviews].map((review, i) => (
            <div key={i} className="w-[350px] bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow whitespace-normal">
              <div className="flex gap-1 text-orange-500 mb-4">
                {[...Array(review.stars)].map((_, i) => <Star key={i} size={16} fill="currentColor" />)}
              </div>
              <p className="text-gray-700 mb-6 text-sm leading-relaxed">"{review.text}"</p>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center font-bold text-gray-500">
                  {review.name[0]}
                </div>
                <div className="text-left">
                  <p className="font-bold text-gray-900 text-sm">{review.name}</p>
                  <p className="text-xs text-gray-500">{review.role}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        {/* Fade Edges */}
        <div className="absolute top-0 left-0 w-32 h-full bg-gradient-to-r from-gray-50 to-transparent z-10"></div>
        <div className="absolute top-0 right-0 w-32 h-full bg-gradient-to-l from-gray-50 to-transparent z-10"></div>
      </div>
    </section>
  );
}