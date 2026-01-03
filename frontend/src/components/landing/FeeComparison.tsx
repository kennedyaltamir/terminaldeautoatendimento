export default function FeeComparison() {
  return (
    <section className="py-24 bg-white">
      <div className="max-w-5xl mx-auto px-6">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900">Pare de ser sócio dos Apps.</h2>
          <p className="text-gray-600">Veja quanto você economiza trazendo o cliente para o seu canal próprio.</p>
        </div>

        <div className="bg-gray-50 rounded-3xl p-8 md:p-12 border border-gray-100">
          <div className="space-y-8">
            {/* iFood */}
            <div>
              <div className="flex justify-between text-sm font-bold text-gray-500 mb-2">
                <span>Apps de Delivery (Marketplace)</span>
                <span>27% de Taxa</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-12 relative overflow-hidden">
                <div className="absolute top-0 left-0 h-full bg-red-500 w-[80%] flex items-center px-4 text-white font-bold">
                  R$ 27.000 em taxas (Faturamento R$ 100k)
                </div>
              </div>
            </div>

            {/* MesaFlow */}
            <div>
              <div className="flex justify-between text-sm font-bold text-gray-500 mb-2">
                <span className="text-orange-600">MesaFlow (Canal Próprio)</span>
                <span className="text-orange-600">0% de Taxa</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-12 relative overflow-hidden">
                <div className="absolute top-0 left-0 h-full bg-green-500 w-[10%] flex items-center px-4 text-white font-bold">
                  R$ 149 (Fixo)
                </div>
              </div>
            </div>
          </div>
          
          <p className="text-center text-sm text-gray-400 mt-8">
            *Cálculo baseado em faturamento mensal de R$ 100.000,00.
          </p>
        </div>
      </div>
    </section>
  );
}