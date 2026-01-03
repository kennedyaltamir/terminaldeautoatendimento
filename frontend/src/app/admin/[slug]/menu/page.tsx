"use client";

import { useEffect, useState } from "react";
import { 
  getMenu, 
  deleteProduct, 
  deleteCategory, 
  createCategory, 
  createProduct, 
  updateProduct, 
  createOptionGroup, 
  createOption, 
  deleteOptionGroup, 
  deleteOption 
} from "@/lib/api";
import { MenuResponse, Product } from "@/types";
import { Trash2, Plus, Edit2, Image as ImageIcon, Save, Settings2, ChevronDown, ChevronUp, X, Box, Link as LinkIcon, Utensils, Wine, Coffee, FileText, Hash } from "lucide-react";
import Modal from "@/components/ui/Modal";
import RecipeModal from "@/components/admin/RecipeModal";

export default function AdminMenuPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [menu, setMenu] = useState<MenuResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [expandedProduct, setExpandedProduct] = useState<number | null>(null);

  const [isCatModalOpen, setIsCatModalOpen] = useState(false);
  const [isProdModalOpen, setIsProdModalOpen] = useState(false);
  const [isGroupModalOpen, setIsGroupModalOpen] = useState(false);
  const [isOptModalOpen, setIsOptModalOpen] = useState(false);
  const [isRecipeModalOpen, setIsRecipeModalOpen] = useState(false);
  
  const [newCategoryName, setNewCategoryName] = useState("");
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [activeProductId, setActiveProductId] = useState<number | null>(null);
  const [activeGroupId, setActiveGroupId] = useState<number | null>(null);

  const [prodForm, setProdForm] = useState({ 
    category_id: 0, 
    name: "", 
    description: "", 
    price: "", 
    image_url: "",
    track_stock: false,
    stock_quantity: 0,
    station: "kitchen",
    short_code: "", // NOVO CAMPO
    recommended_ids: [] as number[]
  });
  const [groupForm, setGroupForm] = useState({ name: "", min_selection: 0, max_selection: 1 });
  const [optForm, setOptForm] = useState({ name: "", price: "0" });

  const fetchMenu = async () => {
    try {
      const data = await getMenu(slug);
      setMenu(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchMenu(); }, [slug]);

  const allProducts = menu?.categories.flatMap(c => c.products) || [];

  const handleCreateCategory = async () => {
    if (!newCategoryName) return;
    try {
      await createCategory(newCategoryName);
      setNewCategoryName("");
      setIsCatModalOpen(false);
      fetchMenu();
    } catch (e) {
      console.error(e);
    }
  };

  const handleSaveProduct = async () => {
    if (!prodForm.name) return alert("Nome do produto é obrigatório");
    if (!prodForm.category_id) return alert("Selecione uma categoria");
    
    const priceFloat = parseFloat(prodForm.price.replace(",", "."));
    if (isNaN(priceFloat)) return alert("Preço inválido");

    const payload = { 
      ...prodForm, 
      price: priceFloat,
      image_url: prodForm.image_url || null,
      short_code: prodForm.short_code || null // Envia null se vazio
    };

    try {
      if (editingProduct) await updateProduct(editingProduct.id, payload);
      else await createProduct(payload);
      setIsProdModalOpen(false);
      fetchMenu();
    } catch (e: any) {
      console.error(e);
      alert("Erro ao salvar produto: " + (e.message || "Verifique os dados"));
    }
  };

  const handleAddGroup = async () => {
    if (!activeProductId) return;
    try {
      await createOptionGroup(activeProductId, groupForm);
      setIsGroupModalOpen(false);
      setGroupForm({ name: "", min_selection: 0, max_selection: 1 });
      fetchMenu();
    } catch (e) {
      console.error(e);
    }
  };

  const handleAddOption = async () => {
    if (!activeGroupId) return;
    try {
      await createOption(activeGroupId, { ...optForm, price: parseFloat(optForm.price.replace(",", ".")) || 0 });
      setIsOptModalOpen(false);
      setOptForm({ name: "", price: "0" });
      fetchMenu();
    } catch (e) {
      console.error(e);
    }
  };

  const toggleRecommendation = (id: number) => {
    setProdForm(prev => {
      const exists = prev.recommended_ids.includes(id);
      return {
        ...prev,
        recommended_ids: exists 
          ? prev.recommended_ids.filter(rid => rid !== id)
          : [...prev.recommended_ids, id]
      };
    });
  };

  if (loading) return <div className="p-10 text-center text-gray-500">Carregando gestão...</div>;

  return (
    <div className="space-y-8 pb-20">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-white">Configurar Cardápio</h1>
        <button onClick={() => setIsCatModalOpen(true)} className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 font-bold transition-all">
          <Plus size={20} /> Nova Categoria
        </button>
      </div>

      <div className="grid gap-6">
        {menu?.categories.map((category) => (
          <div key={category.id} className="bg-gray-800 border border-gray-700 rounded-xl overflow-hidden shadow-xl">
            <div className="p-4 bg-gray-700/30 border-b border-gray-700 flex justify-between items-center">
              <h2 className="text-xl font-bold text-orange-500">{category.name}</h2>
              <button onClick={() => { if(confirm("Excluir categoria?")) deleteCategory(category.id).then(fetchMenu) }} className="text-red-400 hover:text-red-300 p-2 hover:bg-red-900/20 rounded-lg transition-all">
                <Trash2 size={18} />
              </button>
            </div>

            <div className="p-4 space-y-4">
              {category.products.map((product) => (
                <div key={product.id} className="space-y-2">
                  <div className="flex items-center justify-between bg-gray-900/40 p-4 rounded-lg border border-gray-700 hover:border-gray-600 transition-all group">
                    <div className="flex items-center gap-4">
                      {product.image_url ? <img src={product.image_url} className="w-14 h-14 rounded-lg object-cover shadow-md" /> : <div className="w-14 h-14 bg-gray-800 rounded-lg flex items-center justify-center"><ImageIcon className="text-gray-600" /></div>}
                      <div>
                        <h3 className="font-bold text-gray-100 text-lg flex items-center gap-2">
                            {product.name}
                            {product.short_code && <span className="text-xs bg-gray-700 text-gray-300 px-1.5 py-0.5 rounded font-mono">#{product.short_code}</span>}
                        </h3>
                        <div className="flex items-center gap-3">
                          <p className="text-orange-500 font-mono font-bold">R$ {Number(product.price).toFixed(2)}</p>
                          {product.track_stock && (
                            <span className={`text-xs px-2 py-0.5 rounded font-bold ${product.stock_quantity > 0 ? 'bg-green-900 text-green-400' : 'bg-red-900 text-red-400'}`}>
                              {product.stock_quantity > 0 ? `${product.stock_quantity} em estoque` : 'ESGOTADO'}
                            </span>
                          )}
                          <span className="text-xs bg-gray-700 text-gray-300 px-2 py-0.5 rounded font-bold uppercase">
                            {product.station === 'kitchen' ? 'Cozinha' : product.station === 'bar' ? 'Bar' : product.station}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <button onClick={() => { setEditingProduct(product); setIsRecipeModalOpen(true); }} className="p-2 bg-blue-900/20 hover:bg-blue-900/40 rounded-lg text-blue-400" title="Ficha Técnica">
                        <FileText size={18} />
                      </button>
                      <button onClick={() => setExpandedProduct(expandedProduct === product.id ? null : product.id)} className="flex items-center gap-1 px-3 py-2 bg-gray-800 text-gray-300 rounded-lg text-xs font-bold hover:bg-gray-700">
                        <Settings2 size={14} /> Adicionais {expandedProduct === product.id ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                      </button>
                      <button onClick={() => { 
                        setEditingProduct(product); 
                        setProdForm({ 
                          category_id: category.id, 
                          name: product.name, 
                          description: product.description || "", 
                          price: product.price.toString(), 
                          image_url: product.image_url || "",
                          track_stock: product.track_stock,
                          stock_quantity: product.stock_quantity,
                          station: product.station,
                          short_code: product.short_code || "", // Carrega o código existente
                          recommended_ids: product.recommendations?.map(r => r.id) || []
                        }); 
                        setIsProdModalOpen(true); 
                      }} className="p-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-gray-300"><Edit2 size={18} /></button>
                      <button onClick={() => { if(confirm("Excluir produto?")) deleteProduct(product.id).then(fetchMenu) }} className="p-2 bg-red-900/20 hover:bg-red-900/40 rounded-lg text-red-400"><Trash2 size={18} /></button>
                    </div>
                  </div>

                  {expandedProduct === product.id && (
                    <div className="ml-8 p-4 bg-gray-900/60 border-l-2 border-orange-500 rounded-r-lg space-y-4 animate-in slide-in-from-top-2">
                      <div className="flex justify-between items-center">
                        <h4 className="text-sm font-bold text-gray-400 uppercase tracking-widest">Grupos de Adicionais</h4>
                        <button onClick={() => { setActiveProductId(product.id); setIsGroupModalOpen(true); }} className="text-xs bg-orange-600/20 text-orange-500 px-2 py-1 rounded hover:bg-orange-600/30 font-bold">+ Novo Grupo</button>
                      </div>
                      
                      <div className="grid gap-4">
                        {product.option_groups.map(group => (
                          <div key={group.id} className="bg-gray-800/50 p-3 rounded-lg border border-gray-700">
                            <div className="flex justify-between items-center mb-3">
                              <span className="font-bold text-gray-200">{group.name} <span className="text-[10px] text-gray-500 ml-2">(Min: {group.min_selection} / Max: {group.max_selection})</span></span>
                              <button onClick={() => { if(confirm("Excluir grupo?")) deleteOptionGroup(group.id).then(fetchMenu) }} className="text-red-500 hover:text-red-400"><Trash2 size={14} /></button>
                            </div>
                            <div className="flex flex-wrap gap-2">
                              {group.options.map(opt => (
                                <div key={opt.id} className="flex items-center gap-2 bg-gray-900 px-2 py-1 rounded border border-gray-700 text-xs">
                                  <span className="text-gray-300">{opt.name}</span>
                                  <span className="text-orange-500 font-bold">R$ {Number(opt.price).toFixed(2)}</span>
                                  <button onClick={() => deleteOption(opt.id).then(fetchMenu)} className="text-gray-500 hover:text-red-500"><X size={12} /></button>
                                </div>
                              ))}
                              <button onClick={() => { setActiveGroupId(group.id); setIsOptModalOpen(true); }} className="text-[10px] border border-dashed border-gray-600 text-gray-500 px-2 py-1 rounded hover:text-orange-500 hover:border-orange-500">+ Opção</button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
              <button onClick={() => { setEditingProduct(null); setProdForm({ category_id: category.id, name: "", description: "", price: "", image_url: "", track_stock: false, stock_quantity: 0, station: "kitchen", short_code: "", recommended_ids: [] }); setIsProdModalOpen(true); }} className="w-full py-4 border-2 border-dashed border-gray-700 rounded-lg text-gray-500 hover:text-orange-500 hover:border-orange-500/50 transition-all font-bold text-sm">+ Adicionar Produto em {category.name}</button>
            </div>
          </div>
        ))}
      </div>

      {/* MODAIS EXISTENTES */}
      <Modal isOpen={isCatModalOpen} onClose={() => setIsCatModalOpen(false)} title="Nova Categoria">
        <div className="space-y-4">
          <input type="text" className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white mb-4 outline-none focus:ring-2 focus:ring-orange-500" placeholder="Nome da Categoria" value={newCategoryName} onChange={e => setNewCategoryName(e.target.value)} />
          <button onClick={handleCreateCategory} className="w-full bg-orange-600 py-3 rounded-lg font-bold">Criar</button>
        </div>
      </Modal>

      <Modal isOpen={isGroupModalOpen} onClose={() => setIsGroupModalOpen(false)} title="Novo Grupo de Adicionais">
        <div className="space-y-4">
          <input type="text" className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" placeholder="Nome do Grupo (ex: Escolha o Ponto)" value={groupForm.name} onChange={e => setGroupForm({...groupForm, name: e.target.value})} />
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-[10px] font-bold text-gray-500 uppercase">Mínimo</label>
              <input type="number" className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2 text-white" value={groupForm.min_selection} onChange={e => setGroupForm({...groupForm, min_selection: parseInt(e.target.value)})} />
            </div>
            <div>
              <label className="text-[10px] font-bold text-gray-500 uppercase">Máximo</label>
              <input type="number" className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2 text-white" value={groupForm.max_selection} onChange={e => setGroupForm({...groupForm, max_selection: parseInt(e.target.value)})} />
            </div>
          </div>
          <button onClick={handleAddGroup} className="w-full bg-orange-600 py-3 rounded-lg font-bold">Criar Grupo</button>
        </div>
      </Modal>

      <Modal isOpen={isOptModalOpen} onClose={() => setIsOptModalOpen(false)} title="Nova Opção">
        <div className="space-y-4">
          <input type="text" className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" placeholder="Nome da Opção (ex: Bacon)" value={optForm.name} onChange={e => setOptForm({...optForm, name: e.target.value})} />
          <input type="number" className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" placeholder="Preço Adicional" value={optForm.price} onChange={e => setOptForm({...optForm, price: e.target.value})} />
          <button onClick={handleAddOption} className="w-full bg-orange-600 py-3 rounded-lg font-bold">Adicionar Opção</button>
        </div>
      </Modal>

      <Modal isOpen={isProdModalOpen} onClose={() => setIsProdModalOpen(false)} title={editingProduct ? "Editar Produto" : "Novo Produto"}>
        <div className="space-y-4 max-h-[70vh] overflow-y-auto pr-2">
          <input type="text" className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" placeholder="Nome" value={prodForm.name} onChange={e => setProdForm({...prodForm, name: e.target.value})} />
          
          <div className="grid grid-cols-2 gap-4">
            <input type="number" className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" placeholder="Preço" value={prodForm.price} onChange={e => setProdForm({...prodForm, price: e.target.value})} />
            
            {/* NOVO INPUT DE CÓDIGO */}
            <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Hash className="h-4 w-4 text-gray-500" />
                </div>
                <input 
                    type="text" 
                    className="w-full bg-gray-900 border border-gray-700 rounded-lg pl-9 pr-3 py-3 text-white outline-none focus:ring-2 focus:ring-orange-500" 
                    placeholder="Cód. Rápido (ex: 10)" 
                    value={prodForm.short_code} 
                    onChange={e => setProdForm({...prodForm, short_code: e.target.value})} 
                />
            </div>
          </div>

          <textarea className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500 h-24 resize-none" placeholder="Descrição" value={prodForm.description} onChange={e => setProdForm({...prodForm, description: e.target.value})} />
          <input type="text" className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" placeholder="URL da Imagem" value={prodForm.image_url} onChange={e => setProdForm({...prodForm, image_url: e.target.value})} />
          
          {/* Seletor de Estação */}
          <div>
            <label className="block text-xs font-bold text-gray-500 uppercase mb-2">Estação de Preparo</label>
            <div className="grid grid-cols-4 gap-2">
              {[
                { id: 'kitchen', label: 'Cozinha', icon: Utensils },
                { id: 'bar', label: 'Bar', icon: Wine },
                { id: 'dessert', label: 'Sobremesa', icon: Coffee },
                { id: 'other', label: 'Outros', icon: Box },
              ].map((st) => (
                <button
                  key={st.id}
                  onClick={() => setProdForm({...prodForm, station: st.id})}
                  className={`flex flex-col items-center justify-center p-3 rounded-lg border transition-all ${prodForm.station === st.id ? 'bg-orange-600 text-white border-orange-600' : 'bg-gray-900 text-gray-400 border-gray-700 hover:bg-gray-800'}`}
                >
                  <st.icon size={20} />
                  <span className="text-[10px] font-bold mt-1">{st.label}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="bg-gray-900 p-4 rounded-lg border border-gray-700">
            <div className="flex items-center justify-between mb-2">
              <label className="text-sm font-bold text-gray-400 flex items-center gap-2"><Box size={16} /> Controle de Estoque</label>
              <input type="checkbox" className="w-5 h-5 accent-orange-600" checked={prodForm.track_stock} onChange={e => setProdForm({...prodForm, track_stock: e.target.checked})} />
            </div>
            {prodForm.track_stock && (
              <div className="animate-in slide-in-from-top-2">
                <label className="text-[10px] font-bold text-gray-500 uppercase">Quantidade Disponível</label>
                <input type="number" className="w-full bg-gray-800 border border-gray-600 rounded-lg p-2 text-white mt-1" value={prodForm.stock_quantity} onChange={e => setProdForm({...prodForm, stock_quantity: parseInt(e.target.value)})} />
              </div>
            )}
          </div>

          <div className="bg-gray-900 p-4 rounded-lg border border-gray-700">
            <label className="text-sm font-bold text-gray-400 flex items-center gap-2 mb-3"><LinkIcon size={16} /> Recomendações (Upsell)</label>
            <div className="max-h-40 overflow-y-auto space-y-2">
              {allProducts.filter(p => p.id !== editingProduct?.id).map(p => (
                <div key={p.id} onClick={() => toggleRecommendation(p.id)} className={`flex items-center gap-2 p-2 rounded cursor-pointer border ${prodForm.recommended_ids.includes(p.id) ? 'bg-orange-900/30 border-orange-500' : 'bg-gray-800 border-gray-700 hover:bg-gray-700'}`}>
                  <div className={`w-4 h-4 rounded border flex items-center justify-center ${prodForm.recommended_ids.includes(p.id) ? 'bg-orange-500 border-orange-500' : 'border-gray-500'}`}>
                    {prodForm.recommended_ids.includes(p.id) && <div className="w-2 h-2 bg-white rounded-full" />}
                  </div>
                  <span className="text-sm text-gray-300">{p.name}</span>
                </div>
              ))}
            </div>
          </div>

          <button onClick={handleSaveProduct} className="w-full bg-orange-600 py-3 rounded-lg font-bold flex items-center justify-center gap-2"><Save size={20} /> Salvar Produto</button>
        </div>
      </Modal>

      <RecipeModal 
        isOpen={isRecipeModalOpen} 
        onClose={() => setIsRecipeModalOpen(false)} 
        product={editingProduct} 
      />
    </div>
  );
}