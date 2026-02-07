
"use client";
import { useEffect, useState } from "react";
import { ShieldCheck, AlertTriangle, RefreshCw, Database, ArrowRightLeft, CheckCircle2, XCircle, Wrench } from "lucide-react";
import { toast } from "sonner";
import * as api from "@/lib/api";

export default function FinancialAuditPage() {
  const [ledger, setLedger] = useState<any[]>([]);
  const [recon, setRecon] = useState<any>(null);
  const [integrity, setIntegrity] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [fixing, setFixing] = useState<string | null>(null);

  const fetchAuditData = async () => {
    setLoading(true);
    try {
      const [ledgerRes, reconRes, integrityRes] = await Promise.all([
        api.getLedgerHistory(),
        api.getReconciliationReport(),
        api.verifyLedgerIntegrity()
      ]);
      setLedger(ledgerRes);
      setRecon(reconRes);
      setIntegrity(integrityRes);
    } catch (e) {
      toast.error("Falha ao carregar dados de auditoria.");
    } finally {
      setLoading(false);
    }
  };

  const handleFixOrphan = async (externalId: string) => {
    setFixing(externalId);
    try {
      await api.fixOrphanTransaction(externalId);
      toast.success("Transação conciliada com sucesso!");
      fetchAuditData();
    } catch (e) {
      toast.error("Erro ao corrigir transação.");
    } finally {
      setFixing(null);
    }
  };

  useEffect(() => { fetchAuditData(); }, []);

  if (loading) return <div className="p-10 text-center animate-pulse text-gray-500">Auditando integridade financeira L7...</div>;

  return (
    <div className="space-y-6 p-6 animate-in fade-in duration-500">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-black text-white flex items-center gap-3">
          <ShieldCheck className="text-green-500" size={32} /> Auditoria Financeira
        </h1>
        <button onClick={fetchAuditData} className="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-xl font-bold flex items-center gap-2 transition-all">
          <RefreshCw size={18} /> Atualizar
        </button>
      </div>

      {/* Status de Integridade */}
      <div className={`p-6 rounded-2xl border-2 flex items-center justify-between ${integrity?.is_integral ? 'bg-green-900/10 border-green-500/30' : 'bg-red-900/10 border-red-500/30'}`}>
        <div className="flex items-center gap-4">
          <Database className={integrity?.is_integral ? 'text-green-500' : 'text-red-500'} size={28} />
          <div>
            <p className="text-white font-bold">Cadeia de Custódia (Hash Chain)</p>
            <p className="text-sm text-gray-400">{integrity?.message}</p>
          </div>
        </div>
        <span className={`px-3 py-1 rounded-full text-[10px] font-black uppercase ${integrity?.is_integral ? 'bg-green-500 text-white' : 'bg-red-500 text-white'}`}>
          {integrity?.is_integral ? 'Sistema Íntegro' : 'Violado'}
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Conciliação */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 shadow-xl">
            <h3 className="text-xs font-black text-gray-500 uppercase tracking-widest mb-6 flex items-center gap-2">
              <ArrowRightLeft size={14} /> Conciliação Gateway
            </h3>
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="bg-gray-800/50 p-4 rounded-2xl border border-gray-700">
                <p className="text-[10px] text-gray-500 font-bold uppercase">Matched</p>
                <p className="text-3xl font-black text-green-500">{recon?.matched?.length || 0}</p>
              </div>
              <div className="bg-gray-800/50 p-4 rounded-2xl border border-gray-700">
                <p className="text-[10px] text-gray-500 font-bold uppercase">Divergentes</p>
                <p className="text-3xl font-black text-orange-500">{recon?.mismatches?.length || 0}</p>
              </div>
            </div>
            
            {recon?.orphans?.length > 0 && (
              <div className="space-y-3">
                <p className="text-[10px] text-red-400 font-black uppercase tracking-widest">Transações Órfãs (Gateway Only)</p>
                {recon.orphans.map((o: any) => (
                  <div key={o.external_id} className="bg-red-900/10 border border-red-500/20 p-3 rounded-xl flex justify-between items-center">
                    <div>
                      <p className="text-white text-xs font-bold">{o.external_id}</p>
                      <p className="text-[10px] text-gray-500">R$ {(o.amount_cents/100).toFixed(2)}</p>
                    </div>
                    <button 
                      onClick={() => handleFixOrphan(o.external_id)}
                      disabled={fixing === o.external_id}
                      className="p-2 bg-orange-600 hover:bg-orange-700 text-white rounded-lg transition-all disabled:opacity-50"
                    >
                      {fixing === o.external_id ? <RefreshCw className="animate-spin" size={14} /> : <Wrench size={14} />}
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Ledger */}
        <div className="lg:col-span-2 bg-gray-900 border border-gray-800 rounded-2xl overflow-hidden shadow-xl">
          <div className="p-5 border-b border-gray-800 bg-gray-800/30 flex justify-between items-center">
            <h3 className="text-xs font-black text-white uppercase tracking-widest">Extrato Imutável (Ledger)</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-gray-950 text-gray-500 font-bold uppercase">
                <tr>
                  <th className="p-4">Seq</th>
                  <th className="p-4">Tipo</th>
                  <th className="p-4">Valor</th>
                  <th className="p-4">Referência</th>
                  <th className="p-4">Hash</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800">
                {ledger.map((entry: any) => (
                  <tr key={entry.sequence_id} className="hover:bg-gray-800/30 transition-colors">
                    <td className="p-4 font-mono text-gray-500">{entry.sequence_id}</td>
                    <td className="p-4">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-black ${entry.entry_type === 'CREDIT' ? 'bg-green-900/30 text-green-500' : 'bg-red-900/30 text-red-500'}`}>
                        {entry.entry_type}
                      </span>
                    </td>
                    <td className="p-4 font-black text-white">R$ {(entry.amount / 100).toFixed(2)}</td>
                    <td className="p-4 text-gray-400 font-mono">{entry.reference_id}</td>
                    <td className="p-4 font-mono text-[10px] text-gray-600">{entry.integrity_hash.substring(0, 12)}...</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

