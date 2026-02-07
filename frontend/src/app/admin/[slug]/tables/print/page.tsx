/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 14.1.0 (Diamond Print Master)
 * DNA_ID: MF-TABLES-PRINT-V14-1
 * Objective: Resolve TS7006 and unwrap async params for Next.js 16 compliance.
 */
"use client";

import React, { useEffect, useState, use } from "react";
import { 
  getTablesDashboard, 
  getCompanySettings, 
  updateCompanySettings 
} from "@/lib/api";
import { TableDashboard, Company } from "@/types";
import { QRCodeSVG } from "qrcode.react";
import { 
  Loader2, Printer, ArrowLeft, FileDown, 
  Wifi, Instagram, Smartphone, MousePointer2, 
  CreditCard, Moon, Sun, Scissors, Settings2, Save,
  Crown
} from "lucide-react";
import Link from "next/link";
import { toast } from "sonner";
import { cn } from "@/lib/utils";
import html2canvas from "html2canvas";
import { jsPDF } from "jspdf";

interface QRConfig {
  show_wifi: boolean;
  show_instagram: boolean;
  show_steps: boolean;
  show_logo: boolean;
  dark_mode: boolean;
  custom_color: string;
}

export default function PrintTablesPage({ params: paramsPromise }: { params: Promise<{ slug: string }> }) {
  // 🛡️ Next.js 15/16 Compliance: Unwrap Promise params
  const { slug } = use(paramsPromise);
  
  const [tables, setTables] = useState<TableDashboard[]>([]);
  const [company, setCompany] = useState<Company | null>(null);
  const [loading, setLoading] = useState(true);
  const [isExporting, setIsExporting] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  const [config, setConfig] = useState<QRConfig>({
    show_wifi: true,
    show_instagram: true,
    show_steps: true,
    show_logo: true,
    dark_mode: false,
    custom_color: "#ea580c"
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [tablesData, companyData] = await Promise.all([
          getTablesDashboard(),
          getCompanySettings()
        ]);

        // 🛡️ FIX TS7006: Explicitly typing sort parameters
        const sortedTables = [...tablesData].sort((a: TableDashboard, b: TableDashboard) => 
          a.table_number - b.table_number
        );
        
        setTables(sortedTables);
        setCompany(companyData);
        
        if (companyData.qr_config) {
          setConfig({
            ...companyData.qr_config,
            custom_color: companyData.qr_config.custom_color ?? companyData.primary_color ?? "#ea580c"
          });
        } else if (companyData.primary_color) {
          setConfig(prev => ({ ...prev, custom_color: companyData.primary_color }));
        }
      } catch (e) {
        console.error("[Print] Boot Error:", e);
        toast.error("Falha ao sincronizar dados do salão.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // --- ACTIONS ---
  const handleSaveConfig = async () => {
    setIsSaving(true);
    try {
      await updateCompanySettings({ qr_config: config });
      toast.success("Preferências de impressão salvas no servidor!");
    } catch (e) {
      toast.error("Erro ao persistir configurações.");
    } finally {
      setIsSaving(false);
    }
  };

  const downloadPDF = async () => {
    const pages = document.querySelectorAll(".pdf-page-container");
    if (pages.length === 0) return;

    setIsExporting(true);
    const toastId = toast.loading(`Gerando PDF de Alta Resolução...`);

    try {
      const pdf = new jsPDF("p", "mm", "a4");
      
      for (let i = 0; i < pages.length; i++) {
        const canvas = await html2canvas(pages[i] as HTMLElement, {
          scale: 3, // Premium quality scaling
          useCORS: true,
          allowTaint: true,
          backgroundColor: config.dark_mode ? "#000000" : "#ffffff"
        });

        if (i > 0) pdf.addPage();
        const imgData = canvas.toDataURL("image/png");
        pdf.addImage(imgData, "PNG", 0, 0, 210, 297);
      }

      pdf.save(`mesaflow-qrcodes-${slug}-${Date.now()}.pdf`);
      toast.success("Arquivo pronto para impressão!", { id: toastId });
    } catch (error) {
      console.error("PDF Engine Error:", error);
      toast.error("Falha na geração do documento.", { id: toastId });
    } finally {
      setIsExporting(false);
    }
  };

  if (loading || !company) return (
    <div className="flex h-screen flex-col items-center justify-center bg-white gap-4">
      <Loader2 className="animate-spin text-orange-600" size={48} />
      <p className="text-slate-400 font-black uppercase text-[10px] tracking-[0.3em]">Preparando Gráficos...</p>
    </div>
  );

  // Group tables in 6 per page (A4 Layout)
  const chunks = [];
  for (let i = 0; i < tables.length; i += 6) {
    chunks.push(tables.slice(i, i + 6));
  }

  const activeColor = config.custom_color;

  return (
    <div className={cn("min-h-screen flex flex-col md:flex-row", config.dark_mode ? "bg-black text-white" : "bg-slate-100 text-slate-900")}>
      <style jsx global>{`
        @media print {
          html, body { height: auto !important; overflow: visible !important; }
          @page { margin: 0; size: A4 portrait; }
          .no-print { display: none !important; }
          #print-area { position: absolute; left: 0; top: 0; width: 210mm; }
          .pdf-page-container { page-break-after: always; }
        }
      `}</style>

      {/* 🛠️ SIDEBAR: CONFIGURAÇÃO TÁTICA */}
      <aside className="w-full md:w-80 bg-white dark:bg-slate-950 border-r border-slate-200 dark:border-white/5 p-6 no-print flex flex-col gap-8 h-screen sticky top-0 overflow-y-auto shadow-2xl z-50">
        <div className="flex items-center gap-3 border-b border-slate-100 dark:border-white/5 pb-4">
          <Settings2 className="text-orange-600" />
          <h2 className="font-black uppercase tracking-tighter">Estilo dos Cards</h2>
        </div>

        <div className="space-y-6">
          <div className="space-y-4">
            <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Elementos Visíveis</p>
            {[
              { id: 'show_wifi', label: 'Wi-Fi da Loja', icon: Wifi },
              { id: 'show_instagram', label: 'Instagram', icon: Instagram },
              { id: 'show_steps', label: 'Guia do Usuário', icon: Smartphone },
              { id: 'show_logo', label: 'Branding no QR', icon: Crown },
              { id: 'dark_mode', label: 'Inverter Cores', icon: Moon },
            ].map((item) => (
              <label key={item.id} className="flex items-center justify-between cursor-pointer group">
                <div className="flex items-center gap-2 text-sm font-bold text-slate-700 dark:text-slate-300 group-hover:text-orange-600 transition-colors">
                  <item.icon size={16} /> {item.label}
                </div>
                <input 
                  type="checkbox" 
                  className="w-5 h-5 accent-orange-600"
                  checked={(config as any)[item.id]}
                  onChange={(e) => setConfig({...config, [item.id]: e.target.checked})}
                />
           </label>
            ))}
          </div>

          <div className="space-y-3">
            <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Cromatismo</p>
            <div className="flex gap-2">
              <input 
                type="color" 
                className="w-12 h-12 rounded-lg cursor-pointer border-0 p-0 overflow-hidden shadow-inner"
                value={activeColor}
                onChange={(e) => setConfig({...config, custom_color: e.target.value})}
              />
              <input 
                type="text" 
                className="flex-1 bg-slate-50 dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-lg px-3 text-xs font-mono uppercase text-center"
                value={activeColor}
                onChange={(e) => setConfig({...config, custom_color: e.target.value})}
              />
            </div>
          </div>
        </div>

        <div className="mt-auto pt-6 border-t border-slate-100 dark:border-white/5 space-y-3">
          <button onClick={handleSaveConfig} disabled={isSaving} className="w-full bg-slate-100 dark:bg-white/5 text-slate-900 dark:text-white py-3 rounded-xl font-bold text-xs flex items-center justify-center gap-2 hover:bg-slate-200 transition-all disabled:opacity-50">
            {isSaving ? <Loader2 className="animate-spin" size={16} /> : <Save size={16} />} SALVAR PREFERÊNCIAS
           </button>
          <button onClick={downloadPDF} disabled={isExporting} className="w-full bg-blue-600 text-white py-3 rounded-xl font-bold text-xs flex items-center justify-center gap-2 hover:bg-blue-700 transition-all shadow-lg shadow-blue-900/20">
            {isExporting ? <Loader2 className="animate-spin" size={16} /> : <FileDown size={16} />} EXPORTAR PDF
          </button>
          <button onClick={() => window.print()} className="w-full bg-orange-600 text-white py-4 rounded-xl font-black text-sm flex items-center justify-center gap-2 hover:bg-orange-700 transition-all shadow-lg shadow-orange-900/40 active:scale-95">
            <Printer size={20} /> IMPRIMIR AGORA
           </button>
        </div>
      </aside>

      {/* 📑 PREVIEW AREA */}
      <main className="flex-1 overflow-y-auto p-4 md:p-10 flex justify-center">
        <div id="print-area" className={cn("shadow-2xl transition-colors duration-500", config.dark_mode ? "bg-black" : "bg-white")}>
          {chunks.map((chunk, chunkIndex) => (
            <div 
              key={chunkIndex} 
              className="pdf-page-container mx-auto relative overflow-hidden bg-inherit"
              style={{ width: '210mm', height: '297mm', padding: '10mm' }}
            >
              {/* Header de Página */}
              <div className={cn("text-center mb-6 border-b pb-4 mx-4", config.dark_mode ? "border-white/10" : "border-slate-200")}>
                <h1 className="text-xl font-black uppercase tracking-[0.4em]">{company.name}</h1>
                <p className="text-[8px] font-bold uppercase tracking-widest opacity-40">MesaFlow Sovereign Identity • Página {chunkIndex + 1}</p>
              </div>

              <div className="grid grid-cols-2 gap-4 px-4">
                {chunk.map((table) => {
                  const url = `${window.location.origin}/${slug}/menu?table=${table.table_number}&token=${table.qr_token}`;
                  
                  return (
                    <div 
                      key={table.id} 
                      className={cn(
                        "border-2 rounded-[2rem] p-6 flex flex-col items-center justify-between text-center relative overflow-hidden",
                        config.dark_mode ? "border-white/10 bg-slate-900" : "border-slate-900 bg-white"
                      )}
                      style={{ height: '9cm' }}
                    >
                      {/* Top Bar Card */}
                      <div className="w-full flex justify-between items-center mb-2">
                        <span className="text-[9px] font-black uppercase tracking-widest opacity-20">MesaFlow OS</span>
                        <Scissors size={12} className="opacity-10" />
                      </div>

                      <div className="flex flex-col items-center gap-1">
                        <span className="text-[8px] font-black uppercase tracking-[0.5em] text-slate-400">Ambiente</span>
                        <h2 className="text-5xl font-black leading-none" style={{ color: activeColor }}>
                          #{table.table_number.toString().padStart(2, '0')}
                        </h2>
                      </div>
                      
                      {/* QR Core */}
                      <div className={cn(
                        "p-4 rounded-[2rem] border-2 shadow-inner my-4", 
                        config.dark_mode ? "bg-white border-transparent" : "bg-white border-slate-900"
                      )}>
                        <QRCodeSVG 
                          value={url} 
                          size={135} 
                          level="H" 
                          includeMargin={false}
                          imageSettings={config.show_logo && company.logo_url ? {
                            src: company.logo_url,
                            height: 24,
                            width: 24,
                            excavate: true,
                          } : undefined}
                        />
                      </div>
                      
                      {/* Instruction Set */}
                      {config.show_steps && (
                        <div className="flex justify-center gap-6 opacity-50 mb-4">
                          <div className="flex flex-col items-center gap-1">
                            <Smartphone size={14} />
                            <span className="text-[6px] font-black uppercase">Aponte</span>
                          </div>
                          <div className="flex flex-col items-center gap-1">
                            <MousePointer2 size={14} />
                            <span className="text-[6px] font-black uppercase">Peça</span>
                          </div>
                          <div className="flex flex-col items-center gap-1">
                            <CreditCard size={14} />
                            <span className="text-[6px] font-black uppercase">Pague</span>
                          </div>
                        </div>
                      )}

                      {/* Footer Info */}
                      <div className={cn("w-full pt-4 border-t", config.dark_mode ? "border-white/5" : "border-slate-100")}>
                        <div className="flex justify-between items-center px-2 mb-2">
                          {config.show_wifi && company.wifi_ssid && (
                            <div className="flex items-center gap-1 text-[7px] font-bold text-slate-500">
                              <Wifi size={10} className="text-orange-500" /> {company.wifi_ssid}
                            </div>
                          )}
                          {config.show_instagram && company.instagram_url && (
                            <div className="flex items-center gap-1 text-[7px] font-bold text-slate-500">
                              <Instagram size={10} className="text-pink-500" /> @{company.instagram_url.split('/').pop()}
                            </div>
                          )}
                        </div>
                        <p className="text-[6px] font-mono text-slate-400 uppercase tracking-tighter">
                          Token: {table.qr_token.slice(0,12)}...
                        </p>
                      </div>
                    </div>
                  );
                })}
                </div>
             </div>
           ))}
        </div>
      </main>
    </div>
  );
}