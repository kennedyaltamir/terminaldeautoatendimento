"use client";

import { useEffect, useState, use } from "react";
import { getMenu, createCategory, deleteCategory, createProduct, updateProduct, deleteProduct } from "@/lib/api";
import { MenuResponse, Category, Product } from "@/types";
import { 
  Plus, Trash2, Edit2, ChevronDown, ChevronRight, 
  Image as ImageIcon, Loader2, AlertCircle, ExternalLink, Copy 
} from "lucide-react";
import { toast } from "sonner";
import Modal from "@/components/ui/Modal";
import ImageUpload from "@/components/ui/ImageUpload";
import { formatCurrency } from "@/lib/utils";

export default function AdminMenuPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = use(params);

  const [menu, setMenu] = useState<MenuResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [expandedCats, setExpandedCats] = useState<number[]>([]);
  
  const [isCatModalOpen, setIsCatModalOpen] = useState(false);
  const [isProdModalOpen, setIsProdModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [selectedCatId, setSelectedCatId] = useState<number | null>(null);

  const fetchMenu = async () => {
    try {
      const data = await getMenu(slug);
      setMenu(data);
      // Mantém as categorias expandidas se já estiverem
      if (expandedCats.length === 0) {
      setExpandedCats(data.categories.map(c => c.id));
      }
        } catch (e) {
      toast.error("Erro ao carregar cardápio");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchMenu(); }, [slug]);

  const copyPublicLink = () => {
    const url = `${window.location.origin}/${slug}/menu`;
    navigator.clipboard.writeText(url);
    toast.success("Link do cardápio copiado!", {
      description: url
    });
  };

  const toggleCat = (id: number) => {
    setExpandedCats(prev => 
      prev.includes(id) ? prev.filter(c => c !== id) : [...prev, id]
    );
  };

  const handleCreateCategory = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    try {
      await createCategory({ name: formData.get("name") });
      toast.success("Categoria criada!");
      setIsCatModalOpen(false);
      fetchMenu();
    } catch (e) {
      toast.error("Erro ao criar categoria");
    }
  };

  const handleDeleteCategory = async (id: number) => {
    if (!confirm("Excluir categoria?")) return;
    try {
      await deleteCategory(id);
      toast.success("Categoria excluída");
      fetchMenu();
    } catch (e: any) {
      toast.error("Não foi possível excluir", {
        description: e.message || "Verifique se a categoria está vazia antes de excluir.",
        icon: <AlertCircle className="text-red-500" />
      });
    }
  };

  const handleSaveProduct = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const data = {
      category_id: selectedCatId,
      name: formData.get("name"),
      description: formData.get("description"),
      price: Math.round(parseFloat(formData.get("price") as string) * 100),
      image_url: formData.get("image_url"),
      is_available: true
    };

    try {
      if (editingProduct) {
        await updateProduct(editingProduct.id, data);
        toast.success("Produto atualizado!");
      } else {
        await createProduct(data);
        toast.success("Produto criado!");
      }
      setIsProdModalOpen(false);
      fetchMenu();
    } catch (e: any) {
      toast.error(e.message || "Erro ao salvar produto");
    }
  };

  const handleDeleteProduct = async (id: number) => {
    if (!confirm("Excluir produto?")) return;
    try {
      await deleteProduct(id);
      toast.success("Produto excluído");
      fetchMenu();
    } catch (e: any) {
      toast.error("Conflito de Integridade", {
        description: "Este produto possui pedidos ou vínculos e não pode ser removido. Tente desativá-lo.",
        icon: <AlertCircle className="text-orange-500" />
      });
    }
  };

  if (loading) return <div className="flex justify-center py-20"><Loader2 className="animate-spin text-orange-500" size={40} /></div>;

  return (
    <div className="space-y-8 p-6 animate-in fade-in">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
        <h1 className="text-3xl font-bold text-white">Gestão de Cardápio</h1>
          <p className="text-slate-400 text-sm">Organize seus produtos e categorias.</p>
        </div>
        
        <div className="flex gap-3">
          {/* 🔗 NOVO: BOTÃO DE LINK PÚBLICO */}
          <button 
            onClick={copyPublicLink}
            className="bg-slate-800 hover:bg-slate-700 text-slate-200 px-4 py-2 rounded-xl font-bold flex items-center gap-2 border border-slate-700 transition-all"
          >
            <Copy size={18} /> Copiar Link
          </button>
          
          <a 
            href={`/${slug}/menu`} 
            target="_blank"
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl font-bold flex items-center gap-2 shadow-lg transition-all"
          >
            <ExternalLink size={18} /> Ver Cardápio
          </a>

        <button 
          onClick={() => setIsCatModalOpen(true)}
            className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-xl font-bold flex items-center gap-2 shadow-lg transition-all"
        >
          <Plus size={20} /> Nova Categoria
        </button>
        </div>
      </div>

      <div className="space-y-4">
        {menu?.categories.map(cat => (
          <div key={cat.id} className="bg-gray-800 border border-gray-700 rounded-xl overflow-hidden">
            <div 
              className="p-4 flex justify-between items-center bg-gray-900/50 cursor-pointer hover:bg-gray-900 transition-colors"
              onClick={() => {
                setExpandedCats(prev => 
                  prev.includes(cat.id) ? prev.filter(c => c !== cat.id) : [...prev, cat.id]
                );
              }}
            >
              <div className="flex items-center gap-3">
                {expandedCats.includes(cat.id) ? <ChevronDown size={20} className="text-gray-500" /> : <ChevronRight size={20} className="text-gray-500" />}
                <h3 className="font-bold text-lg text-white">{cat.name}</h3>
                <span className="text-xs bg-gray-700 text-gray-300 px-2 py-0.5 rounded-full">{cat.products.length} itens</span>
              </div>
              <div className="flex gap-2">
                <button 
                  onClick={(e) => { e.stopPropagation(); setSelectedCatId(cat.id); setEditingProduct(null); setIsProdModalOpen(true); }}
                  className="p-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-white text-xs font-bold flex items-center gap-1"
                >
                  <Plus size={14} /> Add Produto
                </button>
                <button 
                  onClick={(e) => { e.stopPropagation(); handleDeleteCategory(cat.id); }}
                  className="p-2 hover:bg-red-900/30 rounded-lg text-red-400"
                >
                  <Trash2 size={18} />
                </button>
              </div>
            </div>

            {expandedCats.includes(cat.id) && (
              <div className="p-4 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {cat.products.map(prod => (
                  <div key={prod.id} className="bg-gray-900 border border-gray-700 p-4 rounded-xl flex gap-4 group hover:border-gray-600 transition-all">
                    <div className="w-20 h-20 bg-gray-800 rounded-lg shrink-0 overflow-hidden relative">
                      {prod.image_url ? (
                        <img src={prod.image_url} className="w-full h-full object-cover" alt={prod.name} />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center text-gray-600">
                          <ImageIcon size={24} />
                        </div>
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h4 className="font-bold text-white truncate">{prod.name}</h4>
                      <p className="text-orange-500 font-bold text-sm">{formatCurrency(prod.price)}</p>
                      <p className="text-gray-500 text-xs line-clamp-2 mt-1">{prod.description}</p>
                    </div>
                    <div className="flex flex-col gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button 
                        onClick={() => { setSelectedCatId(cat.id); setEditingProduct(prod); setIsProdModalOpen(true); }}
                        className="p-1.5 bg-gray-800 hover:bg-gray-700 rounded text-gray-400 hover:text-white"
                      >
                        <Edit2 size={16} />
                      </button>
                      <button 
                        onClick={() => handleDeleteProduct(prod.id)}
                        className="p-1.5 bg-gray-800 hover:bg-red-900/30 rounded text-red-400"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </div>
                ))}
                {cat.products.length === 0 && (
                  <div className="col-span-full text-center py-8 text-gray-600 text-sm italic">
                    Nenhum produto nesta categoria.
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      <Modal isOpen={isCatModalOpen} onClose={() => setIsCatModalOpen(false)} title="Nova Categoria">
        <form onSubmit={handleCreateCategory} className="space-y-4">
          <div>
            <label className="block text-sm font-bold text-gray-400 mb-1">Nome</label>
            <input name="name" required className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none" />
          </div>
          <button type="submit" className="w-full bg-orange-600 hover:bg-orange-700 text-white font-bold py-3 rounded-xl mt-4">Salvar</button>
        </form>
      </Modal>

      <Modal isOpen={isProdModalOpen} onClose={() => setIsProdModalOpen(false)} title={editingProduct ? "Editar Produto" : "Novo Produto"}>
        <form onSubmit={handleSaveProduct} className="space-y-4">
          <ImageUpload 
            label="Foto do Produto" 
            value={editingProduct?.image_url} 
            onChange={(url) => {
              const input = document.getElementById('img-url-input') as HTMLInputElement;
              if (input) input.value = url;
            }} 
          />
          <input type="hidden" name="image_url" id="img-url-input" defaultValue={editingProduct?.image_url || ""} />
          
          <div>
            <label className="block text-sm font-bold text-gray-400 mb-1">Nome</label>
            <input name="name" defaultValue={editingProduct?.name} required className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none" />
          </div>
          
          <div>
            <label className="block text-sm font-bold text-gray-400 mb-1">Descrição</label>
            <textarea name="description" defaultValue={editingProduct?.description || ""} className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none h-24" />
          </div>

          <div>
            <label className="block text-sm font-bold text-gray-400 mb-1">Preço (R$)</label>
            <input name="price" type="number" step="0.01" defaultValue={editingProduct ? editingProduct.price / 100 : ""} required className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white focus:ring-2 focus:ring-orange-500 outline-none" />
          </div>

          <button type="submit" className="w-full bg-orange-600 hover:bg-orange-700 text-white font-bold py-3 rounded-xl mt-4">Salvar Produto</button>
        </form>
      </Modal>
    </div>
  );
}
