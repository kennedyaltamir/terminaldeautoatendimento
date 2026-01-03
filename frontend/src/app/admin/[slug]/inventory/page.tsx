"use client";

import { useEffect, useState } from "react";
import { getIngredients, createIngredient, updateIngredient, deleteIngredient } from "@/lib/api";
import { Ingredient } from "@/types";
import { Plus, Search, Edit2, Trash2, Save, X, Package } from "lucide-react";
import { toast, Toaster } from "sonner";
import Modal from "@/components/ui/Modal";

export default function InventoryPage() {
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  
  const [form, setForm] = useState<{
    name: string;
    unit: Ingredient['unit'];
    current_stock: number;
    min_stock_alert: number;
    cost_per_unit: number;
  }>({
    name: "",
    unit: "un",
    current_stock: 0,
    min_stock_alert: 0,
    cost_per_unit: 0
  });

  const fetchIngredients = async () => {
    try {
      const data = await getIngredients();
      setIngredients(data);
    } catch (e) {
      toast.error("Erro ao carregar estoque");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchIngredients(); }, []);

  const handleSubmit = async () => {
    try {
      if (editingId) {
        await updateIngredient(editingId, form);
        toast.success("Ingrediente atualizado!");
      } else {
        await createIngredient(form);
        toast.success("Ingrediente criado!");
      }
      setIsModalOpen(false);
      fetchIngredients();
      resetForm();
    } catch (e) {
      toast.error("Erro ao salvar");
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Tem certeza? Isso pode afetar fichas técnicas.")) return;
    try {
      await deleteIngredient(id);
      toast.success("Ingrediente removido");
      fetchIngredients();
    } catch (e) {
      toast.error("Erro ao remover");
    }
  };

  const openEdit = (ing: Ingredient) => {
    setEditingId(ing.id);
    setForm({
      name: ing.name,
      unit: ing.unit,
      current_stock: Number(ing.current_stock),
      min_stock_alert: Number(ing.min_stock_alert),
      cost_per_unit: Number(ing.cost_per_unit)
    });
    setIsModalOpen(true);
  };

  const resetForm = () => {
    setEditingId(null);
    setForm({ name: "", unit: "un", current_stock: 0, min_stock_alert: 0, cost_per_unit: 0 });
  };

  const filtered = ingredients.filter(i => i.name.toLowerCase().includes(searchTerm.toLowerCase()));

  return (
    <div className="space-y-6 pb-20">
      <Toaster position="top-right" richColors />
      
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Gestão de Estoque</h1>
          <p className="text-gray-400 text-sm">Controle de insumos e custos.</p>
        </div>
        <button 
          onClick={() => { resetForm(); setIsModalOpen(true); }}
          className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-xl font-bold flex items-center gap-2 transition-colors"
        >
          <Plus size={20} /> Novo Ingrediente
        </button>
      </div>

      <div className="bg-gray-800 border border-gray-700 rounded-xl p-4">
        <div className="relative mb-4">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <input 
            type="text" 
            placeholder="Buscar ingrediente..." 
            className="w-full bg-gray-900 border border-gray-700 rounded-lg pl-10 pr-4 py-3 text-white focus:ring-2 focus:ring-orange-500 outline-none"
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-gray-300">
            <thead className="bg-gray-900 text-xs uppercase font-bold text-gray-500">
              <tr>
                <th className="px-4 py-3 rounded-tl-lg">Nome</th>
                <th className="px-4 py-3">Unidade</th>
                <th className="px-4 py-3">Estoque Atual</th>
                <th className="px-4 py-3">Custo Unit.</th>
                <th className="px-4 py-3 rounded-tr-lg text-right">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {loading ? (
                <tr><td colSpan={5} className="text-center py-8">Carregando...</td></tr>
              ) : filtered.length === 0 ? (
                <tr><td colSpan={5} className="text-center py-8 text-gray-500">Nenhum ingrediente encontrado.</td></tr>
              ) : (
                filtered.map(ing => (
                  <tr key={ing.id} className="hover:bg-gray-700/50 transition-colors">
                    <td className="px-4 py-3 font-medium text-white">{ing.name}</td>
                    <td className="px-4 py-3">
                      <span className="bg-gray-700 px-2 py-1 rounded text-xs font-mono">{ing.unit}</span>
                    </td>
                    <td className="px-4 py-3">
                      <span className={`font-bold ${Number(ing.current_stock) <= Number(ing.min_stock_alert) ? 'text-red-500' : 'text-green-500'}`}>
                        {Number(ing.current_stock).toFixed(3)}
                      </span>
                    </td>
                    <td className="px-4 py-3">R$ {Number(ing.cost_per_unit).toFixed(2)}</td>
                    <td className="px-4 py-3 text-right flex justify-end gap-2">
                      <button onClick={() => openEdit(ing)} className="p-2 bg-blue-900/30 text-blue-400 rounded hover:bg-blue-900/50"><Edit2 size={16}/></button>
                      <button onClick={() => handleDelete(ing.id)} className="p-2 bg-red-900/30 text-red-400 rounded hover:bg-red-900/50"><Trash2 size={16}/></button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={editingId ? "Editar Ingrediente" : "Novo Ingrediente"}>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-1">Nome</label>
            <input type="text" className="w-full border rounded-lg p-2" value={form.name} onChange={e => setForm({...form, name: e.target.value})} />
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-1">Unidade</label>
              <select 
                className="w-full border rounded-lg p-2 bg-white" 
                value={form.unit} 
                onChange={e => setForm({...form, unit: e.target.value as Ingredient['unit']})}
              >
                <option value="un">Unidade (un)</option>
                <option value="kg">Quilo (kg)</option>
                <option value="g">Grama (g)</option>
                <option value="l">Litro (l)</option>
                <option value="ml">Mililitro (ml)</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-1">Custo por Unidade</label>
              <input type="number" step="0.01" className="w-full border rounded-lg p-2" value={form.cost_per_unit} onChange={e => setForm({...form, cost_per_unit: parseFloat(e.target.value)})} />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-1">Estoque Inicial</label>
              <input type="number" step="0.001" className="w-full border rounded-lg p-2" value={form.current_stock} onChange={e => setForm({...form, current_stock: parseFloat(e.target.value)})} />
            </div>
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-1">Alerta Mínimo</label>
              <input type="number" step="0.001" className="w-full border rounded-lg p-2" value={form.min_stock_alert} onChange={e => setForm({...form, min_stock_alert: parseFloat(e.target.value)})} />
            </div>
          </div>

          <button onClick={handleSubmit} className="w-full bg-orange-600 text-white py-3 rounded-xl font-bold hover:bg-orange-700 transition-colors">
            Salvar
          </button>
        </div>
      </Modal>
    </div>
  );
}