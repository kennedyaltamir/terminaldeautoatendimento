"use client";

import { useState, useEffect } from "react";
import { Printer, Smartphone, CheckCircle2, Settings2 } from "lucide-react";
import { printTest } from "@/lib/printer/driver";
import { toast } from "sonner";

export default function PrinterSettings() {
  const [width, setWidth] = useState<58 | 80>(58);

  useEffect(() => {
    const saved = localStorage.getItem("mesaflow_printer_width");
    if (saved === "80") setWidth(80);
  }, []);

  const handleSave = (newWidth: 58 | 80) => {
    setWidth(newWidth);
    localStorage.setItem("mesaflow_printer_width", newWidth.toString());
    toast.success(`Largura definida para ${newWidth}mm`);
  };

  const handleTest = () => {
    printTest();
    toast.info("Comando de teste enviado!");
  };

  return (
    <div className="space-y-6 animate-in fade-in">
      <div className="bg-gray-800 border border-gray-700 rounded-xl p-6">
        <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <Printer className="text-orange-500" /> Configuração de Impressão (App)
        </h3>
        
        <div className="bg-gray-900/50 p-4 rounded-xl border border-gray-700 mb-6">
          <p className="text-xs text-gray-400 leading-relaxed">
            Estas configurações afetam a impressão via <b>App Android (RawBT)</b>. 
            Se você usa PC/Windows, configure diretamente no driver do sistema operacional.
          </p>
        </div>

        <div className="space-y-4">
          <label className="block text-sm font-bold text-gray-300">Largura do Papel</label>
          <div className="grid grid-cols-2 gap-4">
            <button
              onClick={() => handleSave(58)}
              className={`p-4 rounded-xl border-2 flex flex-col items-center gap-2 transition-all ${
                width === 58 
                  ? "border-orange-500 bg-orange-500/10 text-white" 
                  : "border-gray-700 bg-gray-800 text-gray-400 hover:bg-gray-700"
              }`}
            >
              <Smartphone size={24} />
              <span className="font-bold">58mm (Padrão)</span>
              <span className="text-xs opacity-70">32 Colunas</span>
            </button>

            <button
              onClick={() => handleSave(80)}
              className={`p-4 rounded-xl border-2 flex flex-col items-center gap-2 transition-all ${
                width === 80 
                  ? "border-orange-500 bg-orange-500/10 text-white" 
                  : "border-gray-700 bg-gray-800 text-gray-400 hover:bg-gray-700"
              }`}
            >
              <Printer size={24} />
              <span className="font-bold">80mm (Largo)</span>
              <span className="text-xs opacity-70">48 Colunas</span>
            </button>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-gray-700 flex justify-end">
          <button 
            onClick={handleTest}
            className="bg-white text-gray-900 hover:bg-gray-200 font-bold py-3 px-6 rounded-xl flex items-center gap-2 transition-colors"
          >
            <Settings2 size={18} /> Imprimir Teste
          </button>
        </div>
      </div>
    </div>
  );
}
