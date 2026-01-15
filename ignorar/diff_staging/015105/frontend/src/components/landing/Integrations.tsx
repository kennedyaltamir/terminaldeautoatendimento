import { 
  CreditCard, 
  Database, 
  Globe, 
  Server, 
  Activity, 
  Zap, 
  FileText, 
  Cloud 
} from "lucide-react";

export default function Integrations() {
  const partners = [
    { name: "Stripe", icon: CreditCard },
    { name: "Mercado Pago", icon: Globe },
    { name: "FocusNFe", icon: FileText },
    { name: "Sentry", icon: Activity },
    { name: "Neon", icon: Database },
    { name: "Redis", icon: Zap },
    { name: "Render", icon: Cloud },
  ];

  return (
    <section className="py-10 bg-white border-b border-gray-100 overflow-hidden">
      <p className="text-center text-sm font-bold text-gray-400 uppercase tracking-widest mb-8">
        Integrado ao melhor ecossistema Enterprise
      </p>
      <div className="relative flex overflow-x-hidden group">
        <div className="animate-scroll whitespace-nowrap flex gap-16">
          {[...partners, ...partners, ...partners].map((p, i) => (
            <div key={i} className="flex items-center gap-2 text-gray-400 font-bold text-xl grayscale hover:grayscale-0 transition-all duration-500">
              <p.icon size={24} />
              <span>{p.name}</span>
            </div>
          ))}
        </div>
        {/* Fade edges */}
        <div className="absolute top-0 left-0 w-32 h-full bg-gradient-to-r from-white to-transparent z-10"></div>
        <div className="absolute top-0 right-0 w-32 h-full bg-gradient-to-l from-white to-transparent z-10"></div>
      </div>
    </section>
  );
}
