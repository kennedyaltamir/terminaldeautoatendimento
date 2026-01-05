"use client";

import { useEffect, useState } from "react";
import { getAuditLogs } from "@/lib/api";
import { AuditLog } from "@/types";
import { ShieldCheck, Search, Clock, User, FileText, Loader2 } from "lucide-react";
import { toast, Toaster } from "sonner";

export default function AuditPage() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    getAuditLogs()
      .then(setLogs)
      .catch(() => toast.error("Erro ao carregar logs"))
      .finally(() => setLoading(false));
  }, []);

  const getActionColor = (action: string) => {
    switch(action) {
      case 'create': return 'bg-green-100 text-green-700 border-green-200';
      case 'update': return 'bg-blue-100 text-blue-700 border-blue-200';
      case 'delete': return 'bg-red-100 text-red-700 border-red-200';
      case 'login': return 'bg-purple-100 text-purple-700 border-purple-200';
      default: return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  const filteredLogs = logs.filter(log => 
    log.user_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    log.resource.toLowerCase().includes(searchTerm.toLowerCase()) ||
    log.action.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6 pb-20 animate-in fade-in">
      <Toaster position="top-right" richColors />

      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center gap-2">
            <ShieldCheck className="text-orange-500" /> Auditoria & Segurança
          </h1>
          <p className="text-gray-400 text-sm mt-1">Rastreabilidade total de ações no sistema.</p>
        </div>
        
        <div className="relative w-full md:w-64">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
          <input 
            type="text" 
            placeholder="Buscar logs..." 
            className="w-full bg-gray-800 border border-gray-700 rounded-xl pl-10 pr-4 py-2.5 text-white focus:ring-2 focus:ring-orange-500 outline-none"
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="bg-gray-800 border border-gray-700 rounded-xl overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-gray-300">
            <thead className="bg-gray-900 text-xs uppercase font-bold text-gray-500">
              <tr>
                <th className="px-6 py-4">Data/Hora</th>
                <th className="px-6 py-4">Usuário</th>
                <th className="px-6 py-4">Ação</th>
                <th className="px-6 py-4">Recurso</th>
                <th className="px-6 py-4">Detalhes</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {loading ? (
                <tr><td colSpan={5} className="text-center py-12"><Loader2 className="animate-spin mx-auto" /></td></tr>
              ) : filteredLogs.length === 0 ? (
                <tr><td colSpan={5} className="text-center py-12 text-gray-500">Nenhum registro encontrado.</td></tr>
              ) : (
                filteredLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-gray-700/30 transition-colors">
                    <td className="px-6 py-4 text-sm font-mono text-gray-400 flex items-center gap-2">
                      <Clock size={14} />
                      {new Date(log.created_at).toLocaleString()}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        <User size={14} className="text-gray-500" />
                        <span className="font-bold text-white">{log.user_name}</span>
                        <span className="text-xs bg-gray-700 px-2 py-0.5 rounded text-gray-400">{log.user_role}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 rounded text-xs font-bold uppercase border ${getActionColor(log.action)}`}>
                        {log.action}
                      </span>
                    </td>
                    <td className="px-6 py-4 font-medium text-gray-300">
                      {log.resource} <span className="text-gray-600 text-xs">#{log.resource_id}</span>
                    </td>
                    <td className="px-6 py-4">
                      {log.details ? (
                        <div className="group relative">
                          <FileText size={18} className="text-gray-500 cursor-help hover:text-white" />
                          <div className="absolute right-0 bottom-full mb-2 w-64 bg-black p-3 rounded-lg text-xs text-gray-300 shadow-xl hidden group-hover:block z-10 border border-gray-700">
                            <pre className="whitespace-pre-wrap">{JSON.stringify(log.details, null, 2)}</pre>
                          </div>
                        </div>
                      ) : (
                        <span className="text-gray-600">-</span>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
