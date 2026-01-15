"use client";
import { useEffect, useState } from "react";
import { 
  getMenu, deleteProduct, deleteCategory, createCategory, 
  createProduct, updateProduct, createOptionGroup, createOption, 
  deleteOptionGroup, deleteOption 
} from "@/lib/api";
import { MenuResponse, Product, Category } from "@/types";
import { Trash2, Plus, Edit2, Image as ImageIcon, Save, Settings2, ChevronDown, ChevronUp, X, Box, Link as UrlIcon, Utensils, Wine, Coffee, FileText, Hash, Copy, ExternalLink, Search, GripVertical } from "lucide-react";
import Modal from "@/components/ui/Modal";
import RecipeModal from "@/components/admin/RecipeModal";
import ImageUpload from "@/components/ui/ImageUpload";
import { toast, Toaster } from "sonner";
import MenuAdminSkeleton from "@/components/admin/MenuAdminSkeleton";
import { formatCurrency, parseCurrencyInput, centsToInput } from "@/lib/utils";

export default function AdminMenuPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [menu, setMenu] = useState<MenuResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [expandedProduct, setExpandedProduct] = useState<number | null>(null);
  const [expandedCategories, setExpandedCategories] = useState<number[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  
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
    category_id: 0, name: "", description: "", price: "", image_url: "",
    track_stock: false, stock_quantity: 0, station: "kitchen", short_code: "", recommended_ids: [] as number[]
  });
  const [groupForm, setGroupForm] = useState({ name: "", min_selection: 0, max_selection: 1 });
  const [optForm, setOptForm] = useState({ name: "", price: "0" });

  const fetchMenu = async () => {
    try {
      const data = await getMenu(slug);
      setMenu(data);
      setExpandedCategories(data.categories.map((c: Category) => c.id));
    } catch (error) {
      console.error(error);
      toast.error("Erro ao carregar cardápio");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchMenu(); }, [slug]);

  const toggleCategory = (id: number) => {
    setExpandedCategories(prev => 
      prev.includes(id) ? prev.filter((c: number) => c !== id) : [...prev, id]
    );
  };

  if (loading) return <MenuAdminSkeleton />;

  const handleCreateCategory = async () => {
    if (!newCategoryName) return;
    try {
      await createCategory(newCategoryName);
      setNewCategoryName(""); setIsCatModalOpen(false); fetchMenu();
      toast.success("Categoria criada!");
    } catch (e) { toast.error("Erro ao criar categoria"); }
  };

  const handleSaveProduct = async () => {
    if (!prodForm.name) return toast.error("Nome obrigatório");
    const priceCents = parseCurrencyInput(prodForm.price);
    if (priceCents < 0) return toast.error("Preço inválido");
    
    const payload = { 
      ...prodForm, 
      price: priceCents, 
      image_url: prodForm.image_url || null, 
      short_code: prodForm.short_code || null 
    };

    try {
      if (editingProduct) await updateProduct(editingProduct.id, payload);
      else await createProduct(payload);
      setIsProdModalOpen(false); fetchMenu();
      toast.success(editingProduct ? "Produto atualizado!" : "Produto criado!");
    } catch (e: any) { toast.error("Erro ao salvar: " + (e.message || "Verifique os dados")); }
  };

  const handleAddGroup = async () => {
    if (!activeProductId) return;
    try {
      await createOptionGroup(activeProductId, groupForm);
      setIsGroupModalOpen(false); setGroupForm({ name: "", min_selection: 0, max_selection: 1 }); fetchMenu();
      toast.success("Grupo criado!");
    } catch (e) { toast.error("Erro ao criar grupo"); }
  };

  const handleAddOption = async () => {
    if (!activeGroupId) return;
    try {
      const priceCents = parseCurrencyInput(optForm.price);
      await createOption(activeGroupId, { ...optForm, price: priceCents });
      setIsOptModalOpen(false); setOptForm({ name: "", price: "0" }); fetchMenu();
      toast.success("Opção adicionada!");
    } catch (e) { toast.error("Erro ao adicionar opção"); }
  };

  const copyPublicLink = () => {
    const url = `${window.location.origin}/${slug}/menu`;
    navigator.clipboard.writeText(url);
    toast.success("Link copiado!");
  };

  const filteredCategories = menu?.categories.map(cat => ({
    ...cat,
    products: cat.products.filter(p => 
      p.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
      p.short_code?.toLowerCase().includes(searchTerm.toLowerCase())
    )
  })).filter(cat => cat.products.length > 0 || searchTerm === "");

  return (
    <div className="space-y-8 pb-20 animate-in fade-in duration-500">
      <Toaster position="top-right" richColors />
      <div className="bg-gradient-to-r from-gray-800 to-gray-900 p-4 rounded-xl border border-gray-700 flex flex-col md:flex-row justify-between items-center gap-4 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="bg-green-500/20 p-2 rounded-lg text-green-400"><UrlIcon size={20} /></div>
          <div>
            <p className="text-xs text-gray-400 font-bold uppercase tracking-wider">Link Público</p>
            <p className="text-white font-mono text-sm truncate max-w-[300px]">{typeof window !== 'undefined' ? window.location.origin : ''}/{slug}/menu</p>
          </div>
        </div>
        <div className="flex gap-2">
          <button type="button" onClick={copyPublicLink} className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg text-xs font-bold flex items-center gap-2 transition-colors"><Copy size={14} /> Copiar</button>
          <a href={`/${slug}/menu`} target="_blank" className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-lg text-xs font-bold flex items-center gap-2 transition-colors"><ExternalLink size={14} /> Abrir</a>
        </div>
      </div>

      <div className="flex flex-col md:flex-row justify-between items-center gap-4">
        <h1 className="text-3xl font-bold text-white">Gestão de Produtos</h1>
        <div className="flex gap-3 w-full md:w-auto">
          <div className="relative flex-1 md:w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
            <input 
              type="text" 
              placeholder="Buscar produto..." 
              className="w-full bg-gray-800 border border-gray-700 rounded-lg pl-10 pr-4 py-2 text-white focus:ring-2 focus:ring-orange-500 outline-none"
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
            />
          </div>
          <button type="button" onClick={() => setIsCatModalOpen(true)} className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 font-bold transition-all shadow-lg shadow-orange-900/20 whitespace-nowrap"><Plus size={20} /> Categoria</button>
        </div>
      </div>

      <div className="grid gap-6">
        {filteredCategories?.map((category) => (
          <div key={category.id} className="bg-gray-800 border border-gray-700 rounded-xl overflow-hidden shadow-xl">
            <div 
              className="p-4 bg-gray-700/30 border-b border-gray-700 flex justify-between items-center cursor-pointer hover:bg-gray-700/50 transition-colors"
              onClick={() => toggleCategory(category.id)}
            >
              <div className="flex items-center gap-3">
                {expandedCategories.includes(category.id) ? <ChevronUp size={20} className="text-gray-400"/> : <ChevronDown size={20} className="text-gray-400"/>}
                <h2 className="text-xl font-bold text-orange-500">{category.name}</h2>
                <span className="text-xs bg-gray-700 text-gray-300 px-2 py-0.5 rounded-full">{category.products.length} itens</span>
              </div>
              <button type="button" onClick={(e) => { e.stopPropagation(); if(confirm("Excluir categoria?")) deleteCategory(category.id).then(fetchMenu) }} className="text-red-400 hover:text-red-300 p-2 hover:bg-red-900/20 rounded-lg transition-all"><Trash2 size={18} /></button>
            </div>

            {expandedCategories.includes(category.id) && (
              <div className="p-4 space-y-4 animate-in slide-in-from-top-2">
                {category.products.map((product) => (
                  <div key={product.id} className="space-y-2">
                    <div className="flex items-center justify-between bg-gray-900/40 p-4 rounded-lg border border-gray-700 hover:border-gray-600 transition-all group">
                      <div className="flex items-center gap-4">
                        <div className="cursor-grab text-gray-600 hover:text-gray-400"><GripVertical size={20} /></div>
                        {product.image_url ? <img src={product.image_url} className="w-14 h-14 rounded-lg object-cover shadow-md" alt={product.name} /> : <div className="w-14 h-14 bg-gray-800 rounded-lg flex items-center justify-center"><ImageIcon className="text-gray-600" /></div>}
                        <div>
                          <h3 className="font-bold text-gray-100 text-lg flex items-center gap-2">{product.name} {product.short_code && <span className="text-xs bg-gray-700 text-gray-300 px-1.5 py-0.5 rounded font-mono">#{product.short_code}</span>}</h3>
                          <div className="flex items-center gap-3">
                            <p className="text-orange-500 font-mono font-bold">{formatCurrency(product.price)}</p>
                            {product.track_stock && <span className={`text-xs px-2 py-0.5 rounded font-bold ${product.stock_quantity > 0 ? 'bg-green-900 text-green-400' : 'bg-red-900 text-red-400'}`}>{product.stock_quantity > 0 ? `${product.stock_quantity} un` : 'ESGOTADO'}</span>}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <button type="button" onClick={() => { setEditingProduct(product); setIsRecipeModalOpen(true); }} className="p-2 bg-blue-900/20 hover:bg-blue-900/40 rounded-lg text-blue-400" title="Ficha Técnica"><FileText size={18} /></button>
                        <button type="button" onClick={() => setExpandedProduct(expandedProduct === product.id ? null : product.id)} className={`flex items-center gap-1 px-3 py-2 rounded-lg text-xs font-bold transition-colors ${expandedProduct === product.id ? 'bg-orange-600 text-white' : 'bg-gray-800 text-gray-300 hover:bg-gray-700'}`}><Settings2 size={14} /> Adicionais {expandedProduct === product.id ? <ChevronUp size={14} /> : <ChevronDown size={14} />}</button>
                        <button type="button" onClick={() => { 
                            setEditingProduct(product); 
                            setProdForm({ 
                                ...product, 
                                description: product.description || "", 
                                price: centsToInput(product.price),
                                category_id: category.id, 
                                image_url: product.image_url || "", 
                                short_code: product.short_code || "", 
                                recommended_ids: product.recommendations?.map(r => r.id) || [] 
                            }); 
                            setIsProdModalOpen(true); 
                        }} className="p-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-gray-300" title="Editar"><Edit2 size={18} /></button>
                        <button type="button" onClick={() => { if(confirm("Excluir produto?")) deleteProduct(product.id).then(fetchMenu) }} className="p-2 bg-red-900/20 hover:bg-red-900/40 rounded-lg text-red-400" title="Excluir"><Trash2 size={18} /></button>
                      </div>
                    </div>
                    {expandedProduct === product.id && (
                      <div className="ml-8 p-4 bg-gray-900/60 border-l-2 border-orange-500 rounded-r-lg space-y-4 animate-in slide-in-from-top-2">
                        <div className="flex justify-between items-center">
                          <h4 className="text-sm font-bold text-gray-400 uppercase tracking-widest">Grupos de Adicionais</h4>
                          <button type="button" onClick={() => { setActiveProductId(product.id); setIsGroupModalOpen(true); }} className="text-xs bg-orange-600/20 text-orange-500 px-3 py-1.5 rounded hover:bg-orange-600/30 font-bold transition-colors">+ Novo Grupo</button>
                        </div>
                        {product.option_groups.length === 0 ? <p className="text-xs text-gray-500 italic">Nenhum grupo configurado.</p> : (
                          <div className="grid gap-4">
                            {product.option_groups.map(group => (
                              <div key={group.id} className="bg-gray-800/50 p-3 rounded-lg border border-gray-700">
                                <div className="flex justify-between items-center mb-3">
                                  <span className="font-bold text-gray-200 flex items-center gap-2">{group.name} <span className="text-[10px] bg-gray-700 px-2 py-0.5 rounded text-gray-300">Min: {group.min_selection} / Max: {group.max_selection}</span></span>
                                  <button type="button" onClick={() => { if(confirm("Excluir grupo?")) deleteOptionGroup(group.id).then(fetchMenu) }} className="text-red-500 hover:text-red-400 p-1"><Trash2 size={14} /></button>
                                </div>
                                <div className="flex flex-wrap gap-2">
                                  {group.options.map(opt => (
                                    <div key={opt.id} className="flex items-center gap-2 bg-gray-900 px-3 py-1.5 rounded border border-gray-700 text-xs group/opt">
                                      <span className="text-gray-300">{opt.name}</span>
                                      <span className="text-orange-500 font-bold">+ {formatCurrency(opt.price)}</span>
                                      <button type="button" onClick={() => deleteOption(opt.id).then(fetchMenu)} className="text-gray-600 hover:text-red-500 ml-1 opacity-0 group-hover/opt:opacity-100 transition-opacity"><X size={12} /></button>
                                    </div>
                                  ))}
                                  <button type="button" onClick={() => { setActiveGroupId(group.id); setIsOptModalOpen(true); }} className="text-[10px] border border-dashed border-gray-600 text-gray-500 px-3 py-1.5 rounded hover:text-orange-500 hover:border-orange-500 transition-colors">+ Opção</button>
                                </div>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ))}
                <button type="button" onClick={() => { setEditingProduct(null); setProdForm({ category_id: category.id, name: "", description: "", price: "", image_url: "", track_stock: false, stock_quantity: 0, station: "kitchen", short_code: "", recommended_ids: [] }); setIsProdModalOpen(true); }} className="w-full py-4 border-2 border-dashed border-gray-700 rounded-lg text-gray-500 hover:text-orange-500 hover:border-orange-500/50 transition-all font-bold text-sm flex items-center justify-center gap-2"><Plus size={16} /> Adicionar Produto em {category.name}</button>
              </div>
            )}
          </div>
        ))}
      </div>

      <Modal isOpen={isCatModalOpen} onClose={() => setIsCatModalOpen(false)} title="Nova Categoria">
        <div className="space-y-4">
            <input className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" value={newCategoryName} onChange={e => setNewCategoryName(e.target.value)} placeholder="Nome da Categoria" autoFocus />
            <button type="button" onClick={handleCreateCategory} className="w-full bg-orange-600 text-white py-3 rounded-lg font-bold hover:bg-orange-700 transition-colors">Criar Categoria</button>
        </div>
      </Modal>

      <Modal isOpen={isProdModalOpen} onClose={() => setIsProdModalOpen(false)} title={editingProduct ? "Editar Produto" : "Novo Produto"}>
         <div className="space-y-4 max-h-[70vh] overflow-y-auto pr-2">
            <input className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" placeholder="Nome do Produto" value={prodForm.name} onChange={e => setProdForm({...prodForm, name: e.target.value})} />
            <div className="grid grid-cols-2 gap-4">
              <input type="number" step="0.01" className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" placeholder="Preço (R$)" value={prodForm.price} onChange={e => setProdForm({...prodForm, price: e.target.value})} />
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"><Hash className="h-4 w-4 text-gray-500" /></div>
                <input type="text" className="w-full bg-gray-900 border border-gray-700 rounded-lg pl-9 pr-3 py-3 text-white outline-none focus:ring-2 focus:ring-orange-500" placeholder="Cód. Rápido" value={prodForm.short_code} onChange={e => setProdForm({...prodForm, short_code: e.target.value})} />
              </div>
            </div>
            <textarea className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500 h-24 resize-none" placeholder="Descrição do produto..." value={prodForm.description} onChange={e => setProdForm({...prodForm, description: e.target.value})} />
            <ImageUpload 
              label="Foto do Produto" 
              value={prodForm.image_url} 
              onChange={(url) => setProdForm({...prodForm, image_url: url})} 
            />
            <div>
              <label className="block text-xs font-bold text-gray-500 uppercase mb-2">Estação de Preparo</label>
              <div className="grid grid-cols-4 gap-2">
                {[{ id: 'kitchen', label: 'Cozinha', icon: Utensils }, { id: 'bar', label: 'Bar', icon: Wine }, { id: 'dessert', label: 'Doce', icon: Coffee }, { id: 'other', label: 'Outros', icon: Box }].map((st) => (
                  <button key={st.id} type="button" onClick={() => setProdForm({...prodForm, station: st.id})} className={`flex flex-col items-center justify-center p-2 rounded-lg border transition-all ${prodForm.station === st.id ? 'bg-orange-600 text-white border-orange-600' : 'bg-gray-900 text-gray-400 border-gray-700 hover:bg-gray-800'}`}>
                    <st.icon size={18} />
                    <span className="text-[10px] font-bold mt-1">{st.label}</span>
                  </button>
                ))}
              </div>
            </div>
            <div className="bg-gray-900 p-4 rounded-lg border border-gray-700">
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm font-bold text-gray-400 flex items-center gap-2"><Box size={16} /> Controlar Estoque?</label>
                <input type="checkbox" className="w-5 h-5 accent-orange-600" checked={prodForm.track_stock} onChange={e => setProdForm({...prodForm, track_stock: e.target.checked})} />
              </div>
              {prodForm.track_stock && (
                <div className="animate-in slide-in-from-top-2">
                  <label className="text-[10px] font-bold text-gray-500 uppercase">Quantidade Disponível</label>
                  <input type="number" className="w-full bg-gray-800 border border-gray-600 rounded-lg p-2 text-white mt-1" value={prodForm.stock_quantity} onChange={e => setProdForm({...prodForm, stock_quantity: parseInt(e.target.value)})} />
                </div>
              )}
            </div>
            <button type="button" onClick={handleSaveProduct} className="w-full bg-orange-600 text-white py-3 rounded-lg font-bold flex items-center justify-center gap-2 hover:bg-orange-700 transition-colors"><Save size={20} /> Salvar Produto</button>
         </div>
      </Modal>

      <Modal isOpen={isGroupModalOpen} onClose={() => setIsGroupModalOpen(false)} title="Novo Grupo de Adicionais">
        <div className="space-y-4">
          <input className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" placeholder="Nome (ex: Escolha o Ponto)" value={groupForm.name} onChange={e => setGroupForm({...groupForm, name: e.target.value})} />
          <div className="grid grid-cols-2 gap-4">
            <div><label className="text-[10px] font-bold text-gray-500 uppercase">Mínimo</label><input type="number" className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2 text-white" value={groupForm.min_selection} onChange={e => setGroupForm({...groupForm, min_selection: parseInt(e.target.value)})} /></div>
            <div><label className="text-[10px] font-bold text-gray-500 uppercase">Máximo</label><input type="number" className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2 text-white" value={groupForm.max_selection} onChange={e => setGroupForm({...groupForm, max_selection: parseInt(e.target.value)})} /></div>
          </div>
          <button type="button" onClick={handleAddGroup} className="w-full bg-orange-600 py-3 rounded-lg font-bold text-white hover:bg-orange-700">Criar Grupo</button>
        </div>
      </Modal>

      <Modal isOpen={isOptModalOpen} onClose={() => setIsOptModalOpen(false)} title="Nova Opção">
        <div className="space-y-4">
          <input className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" placeholder="Nome da Opção (ex: Bacon)" value={optForm.name} onChange={e => setOptForm({...optForm, name: e.target.value})} />
          <input type="number" step="0.01" className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" placeholder="Preço Adicional (0 para grátis)" value={optForm.price} onChange={e => setOptForm({...optForm, price: e.target.value})} />
          <button type="button" onClick={handleAddOption} className="w-full bg-orange-600 py-3 rounded-lg font-bold text-white hover:bg-orange-700">Adicionar Opção</button>
        </div>
      </Modal>

      <RecipeModal isOpen={isRecipeModalOpen} onClose={() => setIsRecipeModalOpen(false)} product={editingProduct} />
    </div>
  );
}
