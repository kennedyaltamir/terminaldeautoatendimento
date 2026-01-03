"use client";

import { useState, useEffect } from "react";
import { X, Plus, Trash2, Save, Search } from "lucide-react";
import { Product, Ingredient, RecipeItem } from "@/types";
import { getIngredients, updateProductRecipe } from "@/lib/api";
import Modal from "@/components/ui/Modal";
import { toast } from "sonner";

interface RecipeModalProps {
  isOpen: boolean;
  onClose: () => void;
  product: Product | null;
}

export default function RecipeModal({ isOpen, onClose, product }: RecipeModalProps) {
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);
  const [recipeItems, setRecipeItems] = useState<RecipeItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    if (isOpen && product) {
      setLoading(true);
      getIngredients()
        .then((data) => {
          setIngredients(data);
          // Se o produto já tiver receita (precisaria vir do backend, por enquanto simulamos vazio ou carregamos se tiver)
          // O endpoint de produtos atual não retorna recipe_items por padrão para economizar banda.
          // Idealmente, faríamos um fetch específico da receita aqui.
          // Para simplificar, vamos assumir que recipe_items vem vazio e o usuário monta.
          // Se quisermos persistência real na edição, precisamos que o getMenu ou getProduct traga isso.
          // Vamos usar o estado local por enquanto.
          setRecipeItems(product.recipe_items || []);
        })
        .catch(() => toast.error("Erro ao carregar ingredientes"))
        .finally(() => setLoading(false));
    }
  }, [isOpen, product]);

  const handleAddIngredient = (ing: Ingredient) => {
    if (recipeItems.some(item => item.ingredient_id === ing.id)) return;
    
    setRecipeItems([...recipeItems, {
      ingredient_id: ing.id,
      quantity_required: 0,
      ingredient: ing
    }]);
  };

  const handleRemoveItem = (index: number) => {
    setRecipeItems(prev => prev.filter((_, i) => i !== index));
  };

  const handleUpdateQuantity = (index: number, qty: number) => {
    setRecipeItems(prev => {
      const newItems = [...prev];
      newItems[index].quantity_required = qty;
      return newItems;
    });
  };

  const handleSave = async () => {
    if (!product) return;
    try {
      await updateProductRecipe(product.id, recipeItems);
      toast.success("Ficha técnica salva!");
      onClose();
    } catch (e) {
      toast.error("Erro ao salvar ficha técnica");
    }
  };

  const filteredIngredients = ingredients.filter(i => 
    i.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const totalCost = recipeItems.reduce((acc, item) => {
    const cost = item.ingredient ? Number(item.ingredient.cost_per_unit) : 0;
    return acc + (cost * item.quantity_required);
  }, 0);

  if (!isOpen || !product) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`Ficha Técnica: ${product.name}`}>
      <div className="space-y-6">
        
        {/* Lista de Ingredientes da Receita */}
        <div className="bg-gray-50 p-4 rounded-xl border border-gray-200">
          <h4 className="font-bold text-gray-700 mb-3 text-sm uppercase">Composição do Prato</h4>
          
          {recipeItems.length === 0 ? (
            <p className="text-sm text-gray-400 text-center py-4">Nenhum ingrediente adicionado.</p>
          ) : (
            <div className="space-y-2">
              {recipeItems.map((item, idx) => (
                <div key={idx} className="flex items-center gap-2 bg-white p-2 rounded border border-gray-200">
                  <span className="flex-1 text-sm font-medium">{item.ingredient?.name}</span>
                  <div className="flex items-center gap-1">
                    <input 
                      type="number" 
                      className="w-20 p-1 border rounded text-sm text-right"
                      value={item.quantity_required}
                      onChange={e => handleUpdateQuantity(idx, parseFloat(e.target.value))}
                      step="0.001"
                    />
                    <span className="text-xs text-gray-500 w-6">{item.ingredient?.unit}</span>
                  </div>
                  <button onClick={() => handleRemoveItem(idx)} className="text-red-400 hover:text-red-600 p-1">
                    <Trash2 size={16} />
                  </button>
                </div>
              ))}
            </div>
          )}

          <div className="mt-4 pt-3 border-t border-gray-200 flex justify-between items-center">
            <span className="text-sm font-bold text-gray-600">Custo Estimado (CMV)</span>
            <span className="text-lg font-black text-green-600">R$ {totalCost.toFixed(2)}</span>
          </div>
        </div>

        {/* Seletor de Ingredientes */}
        <div>
          <div className="relative mb-2">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={16} />
            <input 
              type="text" 
              placeholder="Buscar ingrediente para adicionar..." 
              className="w-full pl-9 pr-4 py-2 border border-gray-300 rounded-lg text-sm outline-none focus:ring-2 focus:ring-orange-500"
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
            />
          </div>
          
          <div className="max-h-40 overflow-y-auto border border-gray-200 rounded-lg">
            {filteredIngredients.map(ing => (
              <button 
                key={ing.id}
                onClick={() => handleAddIngredient(ing)}
                className="w-full text-left px-4 py-2 text-sm hover:bg-orange-50 flex justify-between items-center border-b last:border-0"
              >
                <span>{ing.name}</span>
                <span className="text-xs text-gray-400">{ing.unit}</span>
              </button>
            ))}
          </div>
        </div>

        <button onClick={handleSave} className="w-full bg-orange-600 text-white py-3 rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-orange-700 transition-colors">
          <Save size={18} /> Salvar Ficha Técnica
        </button>
      </div>
    </Modal>
  );
}