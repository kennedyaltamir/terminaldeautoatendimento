import { Printer, Smartphone, Tablet, Monitor } from "lucide-react";

export default function Hardware() {
  return (
    <section className="py-16 border-t border-gray-100 bg-white">
      <div className="max-w-7xl mx-auto px-6 text-center">
        <p className="text-sm font-bold text-gray-400 uppercase tracking-widest mb-8">Funciona no equipamento que você já tem</p>
        <div className="flex flex-wrap justify-center gap-12 opacity-60 grayscale hover:grayscale-0 transition-all duration-500">
          <div className="flex flex-col items-center gap-2">
            <Printer size={40} />
            <span className="text-xs font-bold">Epson / Bematech</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <Tablet size={40} />
            <span className="text-xs font-bold">iPad / Android</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <Smartphone size={40} />
            <span className="text-xs font-bold">Qualquer Celular</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <Monitor size={40} />
            <span className="text-xs font-bold">PC / Mac</span>
          </div>
        </div>
      </div>
    </section>
  );
}