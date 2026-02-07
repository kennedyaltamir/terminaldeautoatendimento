"use client";

import { useEffect, useState, useCallback, use } from "react";
import { getIngredients, createIngredient, deleteIngredient, updateIngredient } from "@/lib/api";
import { Ingredient } from "@/types";
import { Plus, Trash2, Loader2, Package, Search, Edit2, Save } from "lucide-react";
import { toast } from "sonner";
import Modal from "@/components/ui/Modal";
import { formatCurrency } from "@/lib/utils";

export default function InventoryPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = use(params);
  
  // --- ESTADOS ---
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  
  // Modal States
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<Ingredient | null>(null);
  const [formData, setFormData] = useState({
    name: "",
    unit: "un",
    current_stock: "0",
    min_stock_alert: "5",
    cost_per_unit: "0"
  });
  const [saving, setSaving] = useState(false);

  // --- FETCH DATA ---
  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getIngredients();
      setIngredients(data || []);
    } catch (e) {
      console.error(e);
      toast.error("Erro ao carregar estoque. Verifique a conexão.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  // --- HANDLERS ---
  const handleOpenModal = (item?: Ingredient) => {
    if (item) {
      setEditingItem(item);
      setFormData({
        name: item.name,
        unit: item.unit,
        current_stock: item.current_stock.toString(),
        min_stock_alert: item.min_stock_alert.toString(),
        cost_per_unit: (item.cost_per_unit / 100).toString()
      });
    } else {
      setEditingItem(null);
      setFormData({
        name: "",
        unit: "un",
        current_stock: "0",
        min_stock_alert: "5",
        cost_per_unit: "0"
      });
    }
    setIsModalOpen(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);

    const payload = {
      name: formData.name,
      unit: formData.unit,
      current_stock: parseFloat(formData.current_stock),
      min_stock_alert: parseFloat(formData.min_stock_alert),
      cost_per_unit: Math.round(parseFloat(formData.cost_per_unit) * 100) // Centavos
    };

    try {
      if (editingItem) {
        await updateIngredient(editingItem.id, payload);
        toast.success("Insumo atualizado!");
      } else {
        await createIngredient(payload);
        toast.success("Insumo criado!");
      }
      setIsModalOpen(false);
      fetchData();
    } catch (e: any) {
      toast.error(e.message || "Erro ao salvar insumo");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Deseja realmente excluir este insumo?")) return;
    
    // Optimistic Update
    const previous = [...ingredients];
    setIngredients(prev => prev.filter(i => i.id !== id));

    try {
      await deleteIngredient(id);
      toast.success("Insumo removido.");
    } catch (e: any) {
      setIngredients(previous);
      toast.error(e.message || "Erro ao excluir. Pode estar em uso.");
    }
  };

  // --- FILTROS ---
  const filteredIngredients = ingredients.filter(i => 
    i.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6 p-6 animate-in fade-in">
      {/* HEADER */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center gap-2">
            <Package className="text-orange-500" /> Gestão de Estoque
          </h1>
          <p className="text-gray-400 text-sm">Gerencie ingredientes e insumos para fichas técnicas.</p>
        </div>
        <button 
          onClick={() => handleOpenModal()}
          className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-xl font-bold flex items-center gap-2 shadow-lg transition-all active:scale-95"
        >
          <Plus size={20} /> Novo Insumo
        </button>
      </div>

      {/* BUSCA */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={20} />
        <input 
          type="text" 
          placeholder="Buscar insumo..." 
          className="w-full bg-gray-900 border border-gray-700 rounded-xl pl-10 pr-4 py-3 text-white focus:ring-2 focus:ring-orange-500 outline-none"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {/* LISTA */}
      {loading ? (
        <div className="flex justify-center py-20">
          <Loader2 className="animate-spin text-orange-500" size={40} />
        </div>
      ) : filteredIngredients.length === 0 ? (
        <div className="text-center py-20 bg-gray-900/50 rounded-2xl border border-dashed border-gray-700">
          <Package size={48} className="mx-auto text-gray-600 mb-4" />
          <p className="text-gray-500 font-bold">Nenhum insumo encontrado.</p>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {filteredIngredients.map(ing => (
            <div key={ing.id} className="bg-gray-800 p-5 rounded-2xl border border-gray-700 flex justify-between items-center group hover:border-gray-600 transition-all">
              <div>
                <p className="font-bold text-white text-lg">{ing.name}</p>
                <div className="flex items-center gap-2 mt-1">
                  <span className={`text-xs font-bold px-2 py-0.5 rounded ${ing.current_stock <= ing.min_stock_alert ? 'bg-red-900/30 text-red-400' : 'bg-green-900/30 text-green-400'}`}>
                    {ing.current_stock} {ing.unit}
                  </span>
                  <span className="text-xs text-gray-500">
                    {formatCurrency(ing.cost_per_unit)} / {ing.unit}
                  </span>
                </div>
              </div>
              <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button 
                  onClick={() => handleOpenModal(ing)}
                  className="p-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-white transition-colors"
                >
                  <Edit2 size={16} />
                </button>
                <button 
                  onClick={() => handleDelete(ing.id)}
                  className="p-2 bg-red-900/20 hover:bg-red-900/40 text-red-400 rounded-lg transition-colors"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* MODAL */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={editingItem ? "Editar Insumo" : "Novo Insumo"}>
        <form onSubmit={handleSave} className="space-y-4">
          <div>
            <label className="block text-sm font-bold text-gray-400 mb-1">Nome</label>
            <input 
              name="name"
              required 
              className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:border-orange-500 outline-none"
              value={formData.name}
              onChange={e => setFormData({...formData, name: e.target.value})}
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-bold text-gray-400 mb-1">Unidade</label>
              <select 
                name="unit"
                className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:border-orange-500 outline-none"
                value={formData.unit}
                onChange={e => setFormData({...formData, unit: e.target.value})}
              >
                <option value="un">Unidade (un)</option>
                <option value="kg">Quilo (kg)</option>
                <option value="g">Grama (g)</option>
                <option value="l">Litro (l)</option>
                <option value="ml">Mililitro (ml)</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-bold text-gray-400 mb-1">Custo Unit. (R$)</label>
              <input 
                name="cost_per_unit"
                type="number" step="0.01" required 
                className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:border-orange-500 outline-none"
                value={formData.cost_per_unit}
                onChange={e => setFormData({...formData, cost_per_unit: e.target.value})}
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-bold text-gray-400 mb-1">Estoque Atual</label>
              <input 
                name="current_stock"
                type="number" step="0.001" required 
                className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:border-orange-500 outline-none"
                value={formData.current_stock}
                onChange={e => setFormData({...formData, current_stock: e.target.value})}
              />
            </div>
            <div>
              <label className="block text-sm font-bold text-gray-400 mb-1">Alerta Mínimo</label>
              <input 
                name="min_stock_alert"
                type="number" step="0.001" required 
                className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:border-orange-500 outline-none"
                value={formData.min_stock_alert}
                onChange={e => setFormData({...formData, min_stock_alert: e.target.value})}
              />
            </div>
          </div>
          <button 
            type="submit" 
            disabled={saving}
            className="w-full bg-orange-600 hover:bg-orange-700 text-white font-bold py-3 rounded-xl mt-4 flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {saving ? <Loader2 className="animate-spin" /> : <Save size={18} />}
            Salvar Insumo
          </button>
        </form>
      </Modal>
    </div>
  );
}
