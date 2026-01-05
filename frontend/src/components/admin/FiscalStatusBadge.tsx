import { FileText, AlertCircle, CheckCircle2, Loader2, Download } from "lucide-react";

interface FiscalStatusBadgeProps {
  status: string;
  nfeUrl?: string | null;
  onEmit: () => void;
  loading: boolean;
}

export default function FiscalStatusBadge({ status, nfeUrl, onEmit, loading }: FiscalStatusBadgeProps) {
  if (loading) {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-bold bg-blue-100 text-blue-700">
        <Loader2 size={12} className="animate-spin" /> Processando
      </span>
    );
  }

  if (status === 'emitted' && nfeUrl) {
    return (
      <a 
        href={nfeUrl} 
        target="_blank" 
        rel="noopener noreferrer"
        className="inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-bold bg-green-100 text-green-700 hover:bg-green-200 transition-colors"
        title="Baixar Nota Fiscal"
      >
        <CheckCircle2 size={12} /> NFC-e
      </a>
    );
  }

  if (status === 'error') {
    return (
      <button 
        onClick={onEmit}
        className="inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-bold bg-red-100 text-red-700 hover:bg-red-200 transition-colors"
        title="Erro na emissão. Clique para tentar novamente."
      >
        <AlertCircle size={12} /> Erro (Reenviar)
      </button>
    );
  }

  if (status === 'processing') {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-bold bg-yellow-100 text-yellow-700">
        <Loader2 size={12} className="animate-spin" /> Emitindo...
      </span>
    );
  }

  // Default: Pending
  return (
    <button 
      onClick={onEmit}
      className="inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-bold bg-gray-100 text-gray-600 hover:bg-gray-200 transition-colors border border-gray-300"
    >
      <FileText size={12} /> Emitir Nota
    </button>
  );
}
