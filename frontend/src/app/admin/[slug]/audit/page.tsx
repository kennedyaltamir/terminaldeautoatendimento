"use client";
import { useEffect, useState } from "react";
import { ShieldCheck, RefreshCw, Database, ArrowRightLeft, CheckCircle2, XCircle, Wrench, Eye } from "lucide-react";
import { toast } from "sonner";
import { getAuditLogs } from "@/lib/api";
import { AuditLog } from "@/types";
import Modal from "@/components/ui/Modal";

export default function AuditPage() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedLog, setSelectedLog] = useState<AuditLog | null>(null);

  const fetchLogs = async () => {
    setLoading(true);
    try {
      const data = await getAuditLogs();
      setLogs(data);
    } catch (e) {
      toast.error("Falha ao carregar logs de auditoria.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchLogs(); }, []);

  if (loading) return <div className="p-10 text-center animate-pulse text-gray-500">Carregando auditoria...</div>;

  return (
    <div className="space-y-6 p-6 animate-in fade-in duration-500">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-black text-white flex items-center gap-3">
          <ShieldCheck className="text-green-500" size={32} /> Auditoria do Sistema
        </h1>
        <button onClick={fetchLogs} className="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-xl font-bold flex items-center gap-2 transition-all">
          <RefreshCw size={18} /> Atualizar
        </button>
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-2xl overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-gray-950 text-gray-500 font-bold uppercase">
              <tr>
                <th className="p-4">Data</th>
                <th className="p-4">Usuário</th>
                <th className="p-4">Ação</th>
                <th className="p-4">Recurso</th>
                <th className="p-4">IP</th>
                <th className="p-4">Detalhes</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800">
              {logs.map((log) => (
                <tr key={log.id} className="hover:bg-gray-800/30 transition-colors">
                  <td className="p-4 text-gray-400">{new Date(log.created_at).toLocaleString()}</td>
                  <td className="p-4 font-bold text-white">{log.user_name} <span className="text-gray-600 font-normal">({log.user_role})</span></td>
                  <td className="p-4">
                    <span className={`px-2 py-1 rounded text-[10px] font-black uppercase ${
                      log.action === 'delete' ? 'bg-red-900/30 text-red-500' : 
                      log.action === 'create' ? 'bg-green-900/30 text-green-500' : 
                      'bg-blue-900/30 text-blue-500'
                    }`}>
                      {log.action}
                    </span>
                  </td>
                  <td className="p-4 text-gray-300">{log.resource} <span className="text-gray-600">#{log.resource_id}</span></td>
                  <td className="p-4 font-mono text-gray-500">{log.ip_address}</td>
                  <td className="p-4">
                    <button 
                      onClick={() => setSelectedLog(log)}
                      className="p-2 hover:bg-gray-700 rounded-lg text-gray-400 hover:text-white transition-colors"
                    >
                      <Eye size={16} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <Modal isOpen={!!selectedLog} onClose={() => setSelectedLog(null)} title="Detalhes do Log">
        {selectedLog && (
          <div className="space-y-4">
            <div className="bg-gray-950 p-4 rounded-xl border border-gray-800 font-mono text-xs text-green-400 overflow-x-auto">
              <pre>{JSON.stringify(selectedLog.details, null, 2)}</pre>
            </div>
            <button onClick={() => setSelectedLog(null)} className="w-full bg-gray-800 text-white py-3 rounded-xl font-bold">
              Fechar
            </button>
          </div>
        )}
      </Modal>
    </div>
  );
}
