import { Check, X } from "lucide-react";

export default function Comparison() {
  return (
    <section className="py-24 bg-white">
      <div className="max-w-5xl mx-auto px-6">
        <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">Por que escolher o MesaFlow?</h2>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr>
                <th className="p-4 border-b-2 border-gray-100 text-gray-500 font-medium">Recurso</th>
                <th className="p-4 border-b-2 border-gray-100 text-gray-400 font-medium text-center">Sistemas Legados</th>
                <th className="p-4 border-b-2 border-orange-500 bg-orange-50 text-orange-700 font-bold text-center rounded-t-xl">MesaFlow</th>
              </tr>
            </thead>
            <tbody className="text-gray-700">
              <tr>
                <td className="p-4 border-b border-gray-100 font-medium">Instalação</td>
                <td className="p-4 border-b border-gray-100 text-center">Dias (Visita técnica)</td>
                <td className="p-4 border-b border-orange-100 bg-orange-50 text-center font-bold text-green-600">2 Minutos (Online)</td>
              </tr>
              <tr>
                <td className="p-4 border-b border-gray-100 font-medium">Custo de Setup</td>
                <td className="p-4 border-b border-gray-100 text-center">R$ 2.000 - R$ 5.000</td>
                <td className="p-4 border-b border-orange-100 bg-orange-50 text-center font-bold text-green-600">R$ 0,00</td>
              </tr>
              <tr>
                <td className="p-4 border-b border-gray-100 font-medium">App para Cliente</td>
                <td className="p-4 border-b border-gray-100 text-center text-red-500 flex justify-center gap-1"><X size={20}/> Obrigatório</td>
                <td className="p-4 border-b border-orange-100 bg-orange-50 text-center text-green-600 font-bold flex justify-center gap-1"><Check size={20}/> Não precisa</td>
              </tr>
              <tr>
                <td className="p-4 border-b border-gray-100 font-medium">KDS (Cozinha)</td>
                <td className="p-4 border-b border-gray-100 text-center">Módulo Pago Extra</td>
                <td className="p-4 border-b border-orange-100 bg-orange-50 text-center font-bold text-green-600">Incluso</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}