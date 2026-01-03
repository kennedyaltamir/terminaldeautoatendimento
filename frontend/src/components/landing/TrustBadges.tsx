import { ShieldCheck, Lock, Server, Globe } from "lucide-react";

export default function TrustBadges() {
  const badges = [
    { icon: ShieldCheck, title: "LGPD Compliant", desc: "Seus dados protegidos" },
    { icon: Lock, title: "PCI-DSS Ready", desc: "Pagamentos criptografados" },
    { icon: Server, title: "99.99% Uptime", desc: "SLA Garantido em contrato" },
    { icon: Globe, title: "Edge Computing", desc: "Servidores no Brasil" },
  ];

  return (
    <section className="py-12 border-t border-gray-100 bg-white">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {badges.map((badge, i) => (
            <div key={i} className="flex items-center gap-4 opacity-70 hover:opacity-100 transition-opacity">
              <div className="bg-gray-100 p-3 rounded-full text-gray-600">
                <badge.icon size={24} />
              </div>
              <div>
                <h4 className="font-bold text-gray-900 text-sm">{badge.title}</h4>
                <p className="text-xs text-gray-500">{badge.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}