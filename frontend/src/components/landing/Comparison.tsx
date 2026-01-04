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
                <th className="p-4 border-b-2 border-gray-100 text-gray-500 font-medium w-1/3">Recurso</th>
                <th className="p-4 border-b-2 border-gray-100 text-gray-400 font-medium text-center w-1/3">Sistemas Legados</th>
                <th className="p-4 border-b-2 border-orange-500 bg-orange-50 text-orange-700 font-bold text-center rounded-t-xl w-1/3">MesaFlow</th>
              </tr>
            </thead>
            <tbody className="text-gray-700">
              <tr>
                <td className="p-4 border-b border-gray-100 font-medium">Instalação</td>
                <td className="p-4 border-b border-gray-100 text-center text-sm">Dias (Visita técnica)</td>
                <td className="p-4 border-b border-orange-100 bg-orange-50 text-center font-bold text-green-600 text-sm">2 Minutos (Online)</td>
              </tr>
              <tr>
                <td className="p-4 border-b border-gray-100 font-medium">Custo de Setup</td>
                <td className="p-4 border-b border-gray-100 text-center text-sm">R$ 2.000 - R$ 5.000</td>
                <td className="p-4 border-b border-orange-100 bg-orange-50 text-center font-bold text-green-600 text-sm">R$ 0,00</td>
              </tr>
              <tr>
                <td className="p-4 border-b border-gray-100 font-medium">App para Cliente</td>
                <td className="p-4 border-b border-gray-100 text-center">
                  <div className="flex items-center justify-center gap-2 text-red-500 font-bold text-sm">
                    <div className="bg-red-100 p-1 rounded-full"><X size={16}/></div>
                    Obrigatório
                  </div>
                </td>
                <td className="p-4 border-b border-orange-100 bg-orange-50 text-center">
                  <div className="flex items-center justify-center gap-2 text-green-600 font-bold text-sm">
                    <div className="bg-green-100 p-1 rounded-full"><Check size={16}/></div>
                    Não precisa
                  </div>
                </td>
              </tr>
              <tr>
                <td className="p-4 border-b border-gray-100 font-medium">KDS (Cozinha)</td>
                <td className="p-4 border-b border-gray-100 text-center text-sm">Módulo Pago Extra</td>
                <td className="p-4 border-b border-orange-100 bg-orange-50 text-center font-bold text-green-600 text-sm">Incluso</td>
              </tr>
              <tr>
                <td className="p-4 border-b border-gray-100 font-medium">Taxas sobre Vendas</td>
                <td className="p-4 border-b border-gray-100 text-center text-sm">Sim (Marketplaces)</td>
                <td className="p-4 border-b border-orange-100 bg-orange-50 text-center font-bold text-green-600 text-sm">0% (Canal Próprio)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}