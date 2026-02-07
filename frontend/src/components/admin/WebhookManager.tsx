"use client";

import { useState } from "react";
import { Webhook, Plus, Trash2, Copy, ShieldCheck, Check, X, Loader2 } from "lucide-react";
import { toast } from "sonner";
import Modal from "@/components/ui/Modal";
import { createWebhook, deleteWebhook } from "@/lib/api";

interface WebhookData {
  id: number;
  target_url: string;
  events: string[];
  secret: string;
  is_active: boolean;
}

interface WebhookManagerProps {
  webhooks: WebhookData[];
  onUpdate: () => void;
}

export default function WebhookManager({ webhooks, onUpdate }: WebhookManagerProps) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [newWebhook, setNewWebhook] = useState({
    target_url: "",
    events: ["order.created"]
  });

  const handleAdd = async () => {
    if (!newWebhook.target_url.startsWith("http")) {
      return toast.error("URL inválida. Deve começar com http:// ou https://");
    }

    setLoading(true);
    try {
      await createWebhook(newWebhook);
      toast.success("Webhook cadastrado com sucesso!");
      onUpdate();
      setIsModalOpen(false);
      setNewWebhook({ target_url: "", events: ["order.created"] });
    } catch (e) {
      toast.error("Erro ao cadastrar webhook.");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Deseja realmente remover este webhook?")) return;
    try {
      await deleteWebhook(id);
      toast.success("Webhook removido.");
      onUpdate();
    } catch (e) {
      toast.error("Erro ao remover.");
    }
  };

  const copySecret = (secret: string) => {
    navigator.clipboard.writeText(secret);
    toast.success("Segredo copiado!");
  };

  const availableEvents = ["order.created", "order.updated", "payment.updated"];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Webhook className="text-blue-500" /> Webhooks de Saída
          </h3>
          <p className="text-gray-400 text-sm">Notifique sistemas externos sobre eventos em tempo real.</p>
        </div>
        <button 
          onClick={() => setIsModalOpen(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-bold text-sm flex items-center gap-2 transition-colors"
        >
          <Plus size={16} /> Novo Webhook
        </button>
      </div>

      <div className="grid gap-4">
        {webhooks.length === 0 ? (
          <div className="text-center py-12 border-2 border-dashed border-gray-700 rounded-2xl text-gray-500">
            Nenhum webhook configurado.
          </div>
        ) : (
          webhooks.map((w) => (
            <div key={w.id} className="bg-gray-900 p-5 rounded-2xl border border-gray-700 space-y-4">
              <div className="flex justify-between items-start">
                <div className="flex-1 min-w-0">
                  <p className="text-white font-mono text-sm truncate">{w.target_url}</p>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {w.events.map(ev => (
                      <span key={ev} className="bg-blue-900/30 text-blue-400 text-[10px] font-bold px-2 py-0.5 rounded border border-blue-800">
                        {ev}
                      </span>
                    ))}
                  </div>
                </div>
                <button 
                  onClick={() => handleDelete(w.id)}
                  className="text-red-400 hover:text-red-300 p-2 hover:bg-red-900/20 rounded-lg transition-colors"
                >
                  <Trash2 size={18} />
                </button>
              </div>

              <div className="pt-4 border-t border-gray-800 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <ShieldCheck size={14} className="text-green-500" />
                  <span className="text-xs text-gray-500">Signing Secret: <span className="text-gray-300 font-mono">••••••••••••</span></span>
                </div>
                <button 
                  onClick={() => copySecret(w.secret)}
                  className="text-xs text-blue-400 font-bold flex items-center gap-1 hover:underline"
                >
                  <Copy size={12} /> Copiar Segredo
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Configurar Webhook">
        <div className="space-y-5">
          <div>
            <label className="block text-sm font-bold text-gray-400 mb-1">URL de Destino (Endpoint)</label>
            <input 
              type="url" 
              className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="https://seu-sistema.com/webhook"
              value={newWebhook.target_url}
              onChange={e => setNewWebhook({...newWebhook, target_url: e.target.value})}
            />
          </div>

          <div>
            <label className="block text-sm font-bold text-gray-400 mb-3">Eventos para assinar</label>
            <div className="grid gap-2">
              {availableEvents.map(ev => (
                <label key={ev} className="flex items-center gap-3 p-3 bg-gray-900 border border-gray-700 rounded-xl cursor-pointer hover:bg-gray-800 transition-colors">
                  <input 
                    type="checkbox" 
                    checked={newWebhook.events.includes(ev)}
                    onChange={e => {
                      const events = e.target.checked 
                        ? [...newWebhook.events, ev]
                        : newWebhook.events.filter(x => x !== ev);
                      setNewWebhook({...newWebhook, events});
                    }}
                    className="w-5 h-5 accent-blue-600"
                  />
                  <span className="text-sm text-gray-300 font-mono">{ev}</span>
                </label>
              ))}
            </div>
          </div>

          <button 
            onClick={handleAdd}
            disabled={loading || !newWebhook.target_url}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-4 rounded-xl font-bold shadow-lg transition-all disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {loading ? <Loader2 className="animate-spin" /> : <Check size={20} />}
            Ativar Webhook
          </button>
        </div>
      </Modal>
    </div>
  );
}
