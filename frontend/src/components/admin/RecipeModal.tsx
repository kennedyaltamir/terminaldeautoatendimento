
"use client";
import { useState, useEffect, useCallback } from "react";
import { Plus, Trash2, Loader2, Save } from "lucide-react";
import { Ingredient, RecipeItem, Product } from "@/types";
import { getIngredients, updateProductRecipe } from "@/lib/api";
import Modal from "@/components/ui/Modal";
import { toast } from "sonner";

interface RecipeModalProps {
  isOpen: boolean;
  onClose: () => void;
  product: Product;
}

export default function RecipeModal({ isOpen, onClose, product }: RecipeModalProps) {
  const [allIngredients, setAllIngredients] = useState<Ingredient[]>([]);
  const [recipeItems, setRecipeItems] = useState<RecipeItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getIngredients();
      setAllIngredients(data || []);
      setRecipeItems(product.recipe_items || []);
    } catch (e) {
      toast.error("Erro ao carregar ingredientes");
    } finally {
      setLoading(false);
    }
  }, [product.recipe_items]);

  useEffect(() => {
    if (isOpen) {
      loadData();
    }
  }, [isOpen, loadData]);

  const handleAddIngredient = () => {
    if (allIngredients.length === 0) {
      toast.warning("Cadastre ingredientes primeiro.");
      return;
    }
    setRecipeItems(prev => [...prev, { 
      ingredient_id: allIngredients[0].id, 
      quantity_required: 1 
    }]);
  };

  const handleRemove = (index: number) => {
    setRecipeItems(prev => prev.filter((_, i) => i !== index));
  };

  const handleSave = async () => {
    if (recipeItems.length === 0) {
      toast.error("Adicione ao menos um ingrediente.");
      return;
    }
    setSaving(true);
    try {
      await updateProductRecipe({
        product_id: product.id,
        ingredients: recipeItems.map(item => ({
          ingredient_id: item.ingredient_id,
          quantity_required: item.quantity_required
        }))
      });
      toast.success("Ficha técnica atualizada!");
      onClose();
    } catch (e) {
      toast.error("Erro ao salvar receita");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`Ficha Técnica: ${product.name}`}>
      <div className="space-y-6">
        {loading ? (
          <div className="flex flex-col items-center justify-center py-10 gap-2">
            <Loader2 className="animate-spin text-orange-500" />
            <p className="text-xs text-gray-500 font-bold uppercase">Sincronizando Insumos</p>
          </div>
        ) : (
          <>
            <div className="space-y-3 max-h-[50vh] overflow-y-auto pr-2 custom-scrollbar">
              {recipeItems.length === 0 && (
                <p className="text-center text-gray-500 text-sm py-4 italic">Nenhum ingrediente vinculado.</p>
              )}
              {recipeItems.map((item, index) => (
                <div key={index} className="flex gap-2 items-end bg-gray-900 p-3 rounded-xl border border-gray-700 animate-in fade-in slide-in-from-top-1">
                  <div className="flex-1">
                    <label className="block text-[10px] font-black text-gray-500 uppercase mb-1">Ingrediente</label>
                    <select 
                      className="w-full bg-gray-800 border border-gray-700 rounded-lg p-2 text-sm text-white outline-none focus:border-orange-500 transition-colors"
                      value={item.ingredient_id}
                      onChange={(e) => {
                        const newItems = [...recipeItems];
                        newItems[index].ingredient_id = parseInt(e.target.value);
                        setRecipeItems(newItems);
                      }}
                    >
                      {allIngredients.filter(Boolean).map(ing => (
                        <option key={ing.id} value={ing.id}>
                          {ing.name || "Sem nome"} ({ing.unit || "un"})
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="w-24">
                    <label className="block text-[10px] font-black text-gray-500 uppercase mb-1">Qtd</label>
                    <input 
                      type="number"
                      step="0.001"
                      className="w-full bg-gray-800 border border-gray-700 rounded-lg p-2 text-sm text-white outline-none focus:border-orange-500 transition-colors"
                      value={item.quantity_required}
                      onChange={(e) => {
                        const newItems = [...recipeItems];
                        newItems[index].quantity_required = parseFloat(e.target.value) || 0;
                        setRecipeItems(newItems);
                      }}
                    />
                  </div>
                  <button 
                    type="button"
                    onClick={() => handleRemove(index)} 
                    className="p-2 text-red-500 hover:bg-red-500/10 rounded-lg transition-colors"
                  >
                    <Trash2 size={18} />
                  </button>
                </div>
              ))}
            </div>
            <button 
              type="button"
              onClick={handleAddIngredient}
              className="w-full border-2 border-dashed border-gray-700 hover:border-orange-500 text-gray-500 hover:text-orange-500 py-3 rounded-xl font-bold text-sm transition-all flex items-center justify-center gap-2 active:scale-[0.98]"
            >
              <Plus size={18} /> Adicionar Ingrediente
            </button>
            <div className="flex gap-3 pt-4">
                <button 
                  type="button"
                  onClick={onClose} 
                  className="flex-1 bg-gray-700 hover:bg-gray-600 text-white py-3 rounded-xl font-bold transition-colors"
                >
                  Cancelar
                </button>
                <button 
                  type="button"
                  onClick={handleSave} 
                  disabled={saving}
                  className="flex-1 bg-orange-600 hover:bg-orange-700 text-white py-3 rounded-xl font-bold flex items-center justify-center gap-2 shadow-lg shadow-orange-900/20 disabled:opacity-50 active:scale-[0.98] transition-all"
                >
                  {saving ? <Loader2 className="animate-spin" /> : <Save size={18} />}
                  Salvar Ficha
                </button>
            </div>
          </>
        )}
      </div>
    </Modal>
  );
}
