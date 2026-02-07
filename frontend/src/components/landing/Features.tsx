import { Smartphone, Zap, CreditCard, BarChart3, ShieldCheck, Users } from "lucide-react";

export default function Features() {
  return (
    <section id="recursos" className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-6">
        <div className="mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Tecnologia invisível. <br/>Resultados visíveis.</h2>
          <p className="text-gray-600 max-w-2xl">Tudo o que você precisa para operar com eficiência máxima, em uma única plataforma.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Card Grande */}
          <div className="md:col-span-2 bg-gray-900 rounded-3xl p-8 text-white relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-64 h-64 bg-orange-500/20 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 group-hover:bg-orange-500/30 transition-all duration-700"></div>
            <div className="relative z-10">
              <div className="bg-white/10 w-fit p-3 rounded-xl mb-6 backdrop-blur-sm">
                <Zap className="text-orange-400" size={32} />
              </div>
              <h3 className="text-2xl font-bold mb-3">KDS em Tempo Real</h3>
              <p className="text-gray-400 max-w-md">
                Esqueça as impressoras barulhentas. Os pedidos chegam instantaneamente nas telas de produção (Cozinha/Bar) com alertas sonoros e organização automática por tempo de espera.
              </p>
            </div>
          </div>

          {/* Card Médio */}
          <div className="bg-orange-50 rounded-3xl p-8 border border-orange-100 group hover:border-orange-200 transition-all">
            <div className="bg-white w-fit p-3 rounded-xl mb-6 shadow-sm">
              <CreditCard className="text-orange-600" size={32} />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Pagamento Integrado</h3>
            <p className="text-gray-600 text-sm">
              Pix Automático e Cartão. O cliente paga no próprio celular e o pedido já sai com status "Pago". Fim do calote.
            </p>
          </div>

          {/* Card Médio */}
          <div className="bg-gray-50 rounded-3xl p-8 border border-gray-100 group hover:border-gray-200 transition-all">
            <div className="bg-white w-fit p-3 rounded-xl mb-6 shadow-sm">
              <Smartphone className="text-blue-600" size={32} />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Zero App Download</h3>
            <p className="text-gray-600 text-sm">
              Ninguém quer baixar mais um app. O MesaFlow roda direto no navegador, rápido e leve como uma página web.
            </p>
          </div>

          {/* Card Grande */}
          <div className="md:col-span-2 bg-gray-50 rounded-3xl p-8 border border-gray-100 relative overflow-hidden group">
            <div className="relative z-10">
              <div className="bg-white w-fit p-3 rounded-xl mb-6 shadow-sm">
                <Users className="text-purple-600" size={32} />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Fidelidade Automática</h3>
              <p className="text-gray-600 max-w-md">
                Retenha clientes sem esforço. O sistema identifica o cliente pelo telefone e acumula cashback automaticamente. O cliente volta para gastar o saldo.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}