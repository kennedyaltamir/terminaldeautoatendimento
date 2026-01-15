## Resumo Executivo
- **Arquivos com Interação:** 52
- **Total de Elementos:** 223
---

# 🖱️ Inventário Completo de Elementos Interativos
**Data:** nt.times_result(user=0.046875, system=0.03125, children_user=0.0, children_system=0.0, elapsed=0.0)

Este documento lista todos os pontos de interação detectados estaticamente no código.
Use-o para validar se todos os botões, links e inputs estão mapeados e funcionais.

## 📄 `app\admin\forgot-password\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 61 | **Link** | `&lt;Link href="/admin/login" className="text-orange-600 font-bold hover:underline"&gt;Voltar para Login&lt;/Link&gt;` |
| 64 | **Form** | `&lt;form onSubmit={handleSubmit(onSubmit)} className="space-y-6"&gt;` |
| 82 | **Link** | `&lt;Link href="/admin/login" className="text-gray-500 text-sm hover:text-gray-900 flex items-center justify-center gap-2"&gt;` |

## 📄 `app\admin\login\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 44 | **Link** | `&lt;Link href="/" className="inline-flex items-center gap-2 mb-6"&gt;` |
| 54 | **Form** | `&lt;form onSubmit={handleSubmit(onSubmit)} className="space-y-6" data-testid="login-form"&gt;` |
| 74 | **Link** | `&lt;Link href="/admin/forgot-password" title="Recuperar Senha" className="absolute right-0 top-0 text-xs font-bold text-orange-600 hover:underline"&gt;` |
| 91 | **Link** | `Novo por aqui? &lt;Link href="/admin/register" className="text-orange-600 font-bold hover:underline"&gt;Criar conta grátis&lt;/Link&gt;` |

## 📄 `app\admin\register\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 145 | **Link** | `&lt;Link href="/" className="inline-block mb-10"&gt;` |
| 154 | **Form** | `&lt;form onSubmit={handleSubmit(onSubmit)} className="space-y-6"&gt;` |
| 174 | **Input** | `&lt;input type="radio" value={seg.id} {...register('segment')} className="hidden" /&gt;` |
| 268 | **Link** | `Já tem uma conta? &lt;Link href="/admin/login" className="text-orange-500 font-bold hover:underline"&gt;Fazer Login&lt;/Link&gt;` |

## 📄 `app\admin\reset-password\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 69 | **Form** | `&lt;form onSubmit={handleSubmit(onSubmit)} className="space-y-6"&gt;` |

## 📄 `app\admin\support\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 68 | **Form** | `&lt;form onSubmit={handleImpersonate} className="space-y-6"&gt;` |

## 📄 `app\admin\[slug]\layout.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 108 | **Link** | `&lt;Link href={'/admin/${slug}/dashboard'}&gt;` |

## 📄 `app\admin\[slug]\audit\financial\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 56 | **Button** | `&lt;button onClick={fetchAuditData} className="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-xl font-bold flex items-center gap-2 transition...` |

## 📄 `app\admin\[slug]\counter\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 172 | **Button** | `&lt;button onClick={clearCart} className="text-xs text-red-400 hover:text-red-300 font-bold uppercase"&gt;Limpar&lt;/button&gt;` |
| 191 | **Button** | `&lt;button onClick={() =&gt; removeFromCart(idx)} className="text-red-400 hover:text-red-300 opacity-0 group-hover:opacity-100 transition-opacity"&gt;&lt;Trash2 s...` |
| 217 | **Button** | `&lt;button onClick={() =&gt; handleCheckout('cash')} disabled={processing} className="bg-green-600 hover:bg-green-700 text-white p-3 rounded-lg flex flex-co...` |
| 220 | **Button** | `&lt;button onClick={() =&gt; handleCheckout('card')} disabled={processing} className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg flex flex-col ...` |
| 223 | **Button** | `&lt;button onClick={() =&gt; handleCheckout('pix')} disabled={processing} className="bg-purple-600 hover:bg-purple-700 text-white p-3 rounded-lg flex flex-c...` |

## 📄 `app\admin\[slug]\dashboard\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 112 | **Button** | `&lt;button onClick={fetchMetrics} className="mt-4 text-orange-500 hover:underline"&gt;Tentar novamente&lt;/button&gt;` |
| 159 | **Button** | `&lt;button onClick={handleExport} className="bg-white dark:bg-gray-800 hover:bg-slate-50 dark:hover:bg-gray-700 text-slate-700 dark:text-white px-4 py-2 ...` |

## 📄 `app\admin\[slug]\driver\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 186 | **Button** | `&lt;button onClick={fetchMyOrders} className="p-2 bg-blue-700 rounded-full hover:bg-blue-800" title="Atualizar"&gt;&lt;RefreshCw size={20}/&gt;&lt;/button&gt;` |
| 187 | **Button** | `&lt;button onClick={handleLogout} className="p-2 bg-red-500/20 rounded-full hover:bg-red-500/40" title="Sair"&gt;&lt;LogOut size={20}/&gt;&lt;/button&gt;` |

## 📄 `app\admin\[slug]\franchise\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 146 | **Link** | `&lt;Link href={'/admin/${store.slug}/dashboard'} className="text-orange-500 hover:text-orange-400 font-bold flex items-center justify-end gap-1"&gt;` |

## 📄 `app\admin\[slug]\inventory\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 156 | **Button** | `&lt;button onClick={() =&gt; openEdit(ing)} className="p-2 bg-blue-900/30 text-blue-400 rounded hover:bg-blue-900/50"&gt;&lt;Edit2 size={16}/&gt;&lt;/button&gt;` |
| 157 | **Button** | `&lt;button onClick={() =&gt; handleDelete(ing.id)} className="p-2 bg-red-900/30 text-red-400 rounded hover:bg-red-900/50"&gt;&lt;Trash2 size={16}/&gt;&lt;/button&gt;` |
| 172 | **Input** | `&lt;input type="text" className="w-full border rounded-lg p-2" value={form.name} onChange={e =&gt; setForm({...form, name: e.target.value})} /&gt;` |
| 192 | **Input** | `&lt;input type="number" step="0.01" className="w-full border rounded-lg p-2" value={form.cost_per_unit} onChange={e =&gt; setForm({...form, cost_per_unit: p...` |
| 199 | **Input** | `&lt;input type="number" step="0.001" className="w-full border rounded-lg p-2" value={form.current_stock} onChange={e =&gt; setForm({...form, current_stock: ...` |
| 203 | **Input** | `&lt;input type="number" step="0.001" className="w-full border rounded-lg p-2" value={form.min_stock_alert} onChange={e =&gt; setForm({...form, min_stock_ale...` |
| 207 | **Button** | `&lt;button onClick={handleSubmit} className="w-full bg-orange-600 text-white py-3 rounded-xl font-bold hover:bg-orange-700 transition-colors"&gt;` |

## 📄 `app\admin\[slug]\kitchen\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 183 | **Button** | `&lt;button onClick={() =&gt; handleTabChange('all')} className={'px-6 py-3 rounded-full text-sm font-bold flex items-center gap-2 transition-all whitespace-...` |
| 184 | **Button** | `&lt;button onClick={() =&gt; handleTabChange('kitchen')} className={'px-6 py-3 rounded-full text-sm font-bold flex items-center gap-2 transition-all whitesp...` |
| 185 | **Button** | `&lt;button onClick={() =&gt; handleTabChange('bar')} className={'px-6 py-3 rounded-full text-sm font-bold flex items-center gap-2 transition-all whitespace-...` |
| 198 | **Button** | `&lt;button onClick={toggleFullscreen} className={'p-4 rounded-xl transition-all border ${isFullscreen ? 'bg-blue-600 text-white border-blue-500' : 'bg-gr...` |
| 201 | **Button** | `&lt;button onClick={() =&gt; setIsAggregatorOpen(true)} className="p-4 bg-gray-800 rounded-xl hover:bg-gray-700 transition-all text-green-400 border border-...` |
| 202 | **Button** | `&lt;button onClick={() =&gt; setIsStockOpen(true)} className="p-4 bg-gray-800 rounded-xl hover:bg-gray-700 transition-all text-orange-400 border border-gray...` |
| 203 | **Button** | `&lt;button onClick={fetchOrders} className="p-4 bg-gray-800 rounded-xl hover:bg-gray-700 transition-all border border-gray-700 text-gray-300" title="Reca...` |
| 204 | **Button** | `&lt;button onClick={() =&gt; { removeToken(); router.push("/admin/login"); }} className="p-4 bg-red-900/20 text-red-400 rounded-xl hover:bg-red-900/40 trans...` |

## 📄 `app\admin\[slug]\marketing\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 254 | **Button** | `&lt;button onClick={() =&gt; handleDeletePromo(promo.id)} className="text-red-400 hover:text-red-300 p-2 hover:bg-red-900/20 rounded-lg transition-colors"&gt;` |
| 277 | **Anchor** | `&lt;a href="settings" className="bg-gray-700 hover:bg-gray-600 text-white px-6 py-2 rounded-lg font-bold text-sm transition-colors"&gt;` |

## 📄 `app\admin\[slug]\menu\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 140 | **Button** | `&lt;button type="button" onClick={copyPublicLink} className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg text-xs font-bold flex items-c...` |
| 141 | **Anchor** | `&lt;a href={'/${slug}/menu'} target="_blank" className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-lg text-xs font-bold flex items-ce...` |
| 158 | **Button** | `&lt;button type="button" onClick={() =&gt; setIsCatModalOpen(true)} className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-lg flex items-...` |
| 174 | **Button** | `&lt;button type="button" onClick={(e) =&gt; { e.stopPropagation(); if(confirm("Excluir categoria?")) deleteCategory(category.id).then(fetchMenu) }} classNam...` |
| 194 | **Button** | `&lt;button type="button" onClick={() =&gt; { setEditingProduct(product); setIsRecipeModalOpen(true); }} className="p-2 bg-blue-900/20 hover:bg-blue-900/40 r...` |
| 195 | **Button** | `&lt;button type="button" onClick={() =&gt; setExpandedProduct(expandedProduct === product.id ? null : product.id)} className={'flex items-center gap-1 px-3 ...` |
| 196 | **Button** | `&lt;button type="button" onClick={() =&gt; {` |
| 209 | **Button** | `&lt;button type="button" onClick={() =&gt; { if(confirm("Excluir produto?")) deleteProduct(product.id).then(fetchMenu) }} className="p-2 bg-red-900/20 hover...` |
| 216 | **Button** | `&lt;button type="button" onClick={() =&gt; { setActiveProductId(product.id); setIsGroupModalOpen(true); }} className="text-xs bg-orange-600/20 text-orange-5...` |
| 224 | **Button** | `&lt;button type="button" onClick={() =&gt; { if(confirm("Excluir grupo?")) deleteOptionGroup(group.id).then(fetchMenu) }} className="text-red-500 hover:text...` |
| 231 | **Button** | `&lt;button type="button" onClick={() =&gt; deleteOption(opt.id).then(fetchMenu)} className="text-gray-600 hover:text-red-500 ml-1 opacity-0 group-hover/opt:...` |
| 234 | **Button** | `&lt;button type="button" onClick={() =&gt; { setActiveGroupId(group.id); setIsOptModalOpen(true); }} className="text-[10px] border border-dashed border-gray...` |
| 244 | **Button** | `&lt;button type="button" onClick={() =&gt; { setEditingProduct(null); setProdForm({ category_id: category.id, name: "", description: "", price: "", image_ur...` |
| 253 | **Input** | `&lt;input className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" value={newCateg...` |
| 254 | **Button** | `&lt;button type="button" onClick={handleCreateCategory} className="w-full bg-orange-600 text-white py-3 rounded-lg font-bold hover:bg-orange-700 transiti...` |
| 260 | **Input** | `&lt;input className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" placeholder="No...` |
| 262 | **Input** | `&lt;input type="number" step="0.01" className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-o...` |
| 265 | **Input** | `&lt;input type="text" className="w-full bg-gray-900 border border-gray-700 rounded-lg pl-9 pr-3 py-3 text-white outline-none focus:ring-2 focus:ring-oran...` |
| 268 | **Textarea** | `&lt;textarea className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500 h-24 resize-n...` |
| 278 | **Button** | `&lt;button key={st.id} type="button" onClick={() =&gt; setProdForm({...prodForm, station: st.id})} className={'flex flex-col items-center justify-center p-2...` |
| 288 | **Input** | `&lt;input type="checkbox" className="w-5 h-5 accent-orange-600" checked={prodForm.track_stock} onChange={e =&gt; setProdForm({...prodForm, track_stock: e.ta...` |
| 293 | **Input** | `&lt;input type="number" className="w-full bg-gray-800 border border-gray-600 rounded-lg p-2 text-white mt-1" value={prodForm.stock_quantity} onChange={e ...` |
| 297 | **Button** | `&lt;button type="button" onClick={handleSaveProduct} className="w-full bg-orange-600 text-white py-3 rounded-lg font-bold flex items-center justify-cente...` |
| 303 | **Input** | `&lt;input className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" placeholder="No...` |
| 305 | **Input** | `&lt;div&gt;&lt;label className="text-[10px] font-bold text-gray-500 uppercase"&gt;Mínimo&lt;/label&gt;&lt;input type="number" className="w-full bg-gray-900 border border-g...` |
| 306 | **Input** | `&lt;div&gt;&lt;label className="text-[10px] font-bold text-gray-500 uppercase"&gt;Máximo&lt;/label&gt;&lt;input type="number" className="w-full bg-gray-900 border border-g...` |
| 308 | **Button** | `&lt;button type="button" onClick={handleAddGroup} className="w-full bg-orange-600 py-3 rounded-lg font-bold text-white hover:bg-orange-700"&gt;Criar Grupo&lt;/...` |
| 314 | **Input** | `&lt;input className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" placeholder="No...` |
| 315 | **Input** | `&lt;input type="number" step="0.01" className="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-o...` |
| 316 | **Button** | `&lt;button type="button" onClick={handleAddOption} className="w-full bg-orange-600 py-3 rounded-lg font-bold text-white hover:bg-orange-700"&gt;Adicionar Op...` |

## 📄 `app\admin\[slug]\profile\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 79 | **Form** | `&lt;form onSubmit={handlePasswordChange} className="space-y-5"&gt;` |

## 📄 `app\admin\[slug]\settings\FinanceSection.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 57 | **Button** | `&lt;button onClick={handleDisconnect} className="text-red-400 hover:text-red-300 p-2"&gt;` |

## 📄 `app\admin\[slug]\settings\FiscalSection.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 137 | **Form** | `&lt;form onSubmit={handleSubmit(onSubmit)} className="space-y-6"&gt;` |
| 139 | **Input** | `&lt;input type="hidden" {...register("name")} /&gt;` |
| 140 | **Input** | `&lt;input type="hidden" {...register("primary_color")} /&gt;` |
| 141 | **Input** | `&lt;input type="hidden" {...register("loyalty_percentage")} /&gt;` |
| 142 | **Input** | `&lt;input type="hidden" {...register("fixed_delivery_fee")} /&gt;` |
| 156 | **Button** | `&lt;button type="button" onClick={handleSearchCNPJ} className="bg-gray-700 hover:bg-gray-600 text-white px-3 rounded-lg"&gt;` |
| 177 | **Anchor** | `&lt;a href="https://focusnfe.com.br" target="_blank" className="text-[10px] text-blue-400 flex items-center gap-1"&gt;Painel &lt;ExternalLink size={10} /&gt;&lt;/a&gt;` |
| 188 | **Button** | `&lt;button type="button" onClick={handleTestConnection} className="absolute right-1 top-1 bottom-1 bg-gray-800 text-xs font-bold text-gray-300 px-3 round...` |

## 📄 `app\admin\[slug]\settings\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 255 | **Button** | `&lt;button onClick={handleSubmit(onSubmit)} disabled={isSubmitting} className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-bold te...` |

## 📄 `app\admin\[slug]\tables\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 206 | **Button** | `&lt;button onClick={() =&gt; fetchTables()} className="bg-gray-700 hover:bg-gray-600 text-white p-2 rounded-xl transition-colors" title="Atualizar"&gt;` |
| 209 | **Button** | `&lt;button onClick={() =&gt; setIsCreateModalOpen(true)} className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-xl flex items-center gap-...` |
| 212 | **Button** | `&lt;button onClick={() =&gt; window.print()} className="bg-white text-gray-900 px-4 py-2 rounded-xl flex items-center gap-2 font-bold transition-colors hove...` |
| 223 | **Button** | `&lt;button onClick={() =&gt; setIsCreateModalOpen(true)} className="mt-4 text-orange-500 font-bold hover:underline"&gt;Criar a primeira mesa&lt;/button&gt;` |
| 273 | **Input** | `&lt;input type="number" className="flex-1 bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" p...` |
| 274 | **Button** | `&lt;button onClick={handleCreate} className="bg-orange-600 text-white px-6 rounded-lg font-bold hover:bg-orange-700"&gt;Criar&lt;/button&gt;` |
| 280 | **Input** | `&lt;input type="number" className="w-24 bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" pla...` |
| 282 | **Input** | `&lt;input type="number" className="w-24 bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" pla...` |
| 283 | **Button** | `&lt;button onClick={handleBulkCreate} className="flex-1 bg-gray-700 text-white px-4 py-3 rounded-lg font-bold hover:bg-gray-600"&gt;Gerar&lt;/button&gt;` |
| 304 | **Button** | `&lt;button onClick={handleOpenTable} className="bg-green-600 text-white px-4 rounded-lg font-bold hover:bg-green-700"&gt;Abrir&lt;/button&gt;` |
| 320 | **Button** | `&lt;button onClick={() =&gt; handleCloseTable('cash')} className="bg-gray-800 hover:bg-green-600 text-gray-300 hover:text-white p-3 rounded-lg font-bold tra...` |
| 323 | **Button** | `&lt;button onClick={() =&gt; handleCloseTable('card')} className="bg-gray-800 hover:bg-blue-600 text-gray-300 hover:text-white p-3 rounded-lg font-bold tran...` |
| 331 | **Button** | `&lt;button onClick={() =&gt; handleDelete(selectedTable.id)} className="text-red-400 hover:text-red-300 text-xs font-bold flex items-center gap-1 hover:bg-r...` |

## 📄 `app\admin\[slug]\team\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 209 | **Form** | `&lt;form onSubmit={handleSubmit(onSubmit)} className="space-y-4"&gt;` |
| 243 | **Input** | `&lt;input type="radio" value="cashier" {...register("role")} className="accent-orange-600" /&gt;` |
| 250 | **Input** | `&lt;input type="radio" value="kitchen" {...register("role")} className="accent-orange-600" /&gt;` |
| 257 | **Input** | `&lt;input type="radio" value="driver" {...register("role")} className="accent-orange-600" /&gt;` |
| 264 | **Input** | `&lt;input type="radio" value="manager" {...register("role")} className="accent-orange-600" /&gt;` |
| 273 | **Button** | `&lt;button type="submit" className="w-full bg-orange-600 text-white py-3 rounded-xl font-bold hover:bg-orange-700 transition-colors shadow-lg"&gt;` |

## 📄 `app\admin\[slug]\waiter\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 78 | **Button** | `&lt;button onClick={fetchTables} className="p-2 bg-gray-800 rounded-lg hover:bg-gray-700"&gt;&lt;RefreshCw size={18}/&gt;&lt;/button&gt;` |
| 80 | **Button** | `&lt;button onClick={() =&gt; setFilter('all')} className={'px-3 py-1 rounded text-xs font-bold ${filter === 'all' ? 'bg-gray-600 text-white' : 'text-gray-40...` |
| 81 | **Button** | `&lt;button onClick={() =&gt; setFilter('free')} className={'px-3 py-1 rounded text-xs font-bold ${filter === 'free' ? 'bg-green-600 text-white' : 'text-gray...` |
| 82 | **Button** | `&lt;button onClick={() =&gt; setFilter('occupied')} className={'px-3 py-1 rounded text-xs font-bold ${filter === 'occupied' ? 'bg-red-600 text-white' : 'tex...` |
| 100 | **Button** | `&lt;button onClick={() =&gt; handleQuickOrder('takeout')} className="bg-orange-50 border border-orange-200 p-4 rounded-2xl flex flex-col items-center gap-2 ...` |
| 107 | **Button** | `&lt;button onClick={() =&gt; handleQuickOrder('delivery')} className="bg-blue-50 border border-blue-200 p-4 rounded-2xl flex flex-col items-center gap-2 act...` |

## 📄 `app\admin\[slug]\waiter\pos\quick\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 108 | **Button** | `&lt;button onClick={() =&gt; router.back()} className="p-2 hover:bg-white/20 rounded-full"&gt;&lt;ChevronLeft /&gt;&lt;/button&gt;` |
| 161 | **Input** | `&lt;input type="text" placeholder="Buscar produto..." className="w-full bg-gray-100 border-none rounded-lg pl-10 pr-4 py-3 text-sm outline-none" value={s...` |
| 192 | **Button** | `&lt;button key={cat.id} onClick={() =&gt; setActiveCategory(cat.id)} className={'whitespace-nowrap px-4 py-3 rounded-lg text-sm font-bold ${activeCategory =...` |
| 222 | **Button** | `&lt;button onClick={() =&gt; setIsCartOpen(true)} className="flex-1 bg-gray-200 text-gray-800 py-3.5 rounded-xl font-bold flex items-center justify-center g...` |
| 240 | **Button** | `&lt;button onClick={() =&gt; setIsCartOpen(false)}&gt;&lt;X /&gt;&lt;/button&gt;` |
| 246 | **Button** | `&lt;div className="flex items-center gap-3"&gt;&lt;span className="font-bold text-lg"&gt;x{item.quantity}&lt;/span&gt;&lt;button onClick={() =&gt; removeFromCart(idx)} classN...` |
| 250 | **Button** | `&lt;div className="p-4 border-t"&gt;&lt;button onClick={() =&gt; setIsCartOpen(false)} className="w-full bg-gray-900 text-white py-3 rounded-xl font-bold"&gt;Voltar&lt;...` |

## 📄 `app\admin\[slug]\waiter\pos\[tableId]\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 196 | **Button** | `&lt;button onClick={() =&gt; router.back()} className="p-2 hover:bg-gray-800 rounded-full"&gt;&lt;ChevronLeft /&gt;&lt;/button&gt;` |
| 201 | **Button** | `&lt;button onClick={() =&gt; setIsTransferOpen(true)} className="bg-orange-600 p-2 rounded-full hover:bg-orange-500 text-white" title="Transferir Mesa"&gt;&lt;Arr...` |
| 202 | **Button** | `&lt;button onClick={() =&gt; setIsSplitOpen(true)} className="bg-blue-600 p-2 rounded-full hover:bg-blue-500 text-white" title="Dividir Conta"&gt;&lt;Calculator s...` |
| 203 | **Button** | `&lt;button onClick={() =&gt; { setPartialAmount(null); setIsPaymentOpen(true); }} className="bg-green-600 p-2 rounded-full hover:bg-green-500 text-white sha...` |
| 204 | **Button** | `&lt;button onClick={() =&gt; setIsAuditOpen(true)} className="bg-gray-700 p-2 rounded-full hover:bg-gray-600 text-blue-400" title="Ver Comanda"&gt;&lt;Eye size={2...` |
| 205 | **Button** | `&lt;button onClick={handlePrintBill} className="bg-gray-700 p-2 rounded-full hover:bg-gray-600" title="Imprimir Parcial"&gt;&lt;Printer size={20} /&gt;&lt;/button&gt;` |
| 215 | **Input** | `&lt;input type="text" placeholder="Nome do Cliente" className="flex-1 bg-white border border-orange-300 rounded px-3 py-2 text-sm outline-none" value={cu...` |
| 219 | **Input** | `&lt;input type="tel" placeholder="Telefone (Busca Saldo)" className="flex-1 bg-white border border-orange-300 rounded px-3 py-2 text-sm outline-none" val...` |
| 227 | **Button** | `&lt;button onClick={handleOpenTable} className="bg-orange-600 text-white px-4 py-2 rounded font-bold text-sm w-full"&gt;Abrir Mesa&lt;/button&gt;` |
| 231 | **Input** | `&lt;div className="p-2 bg-white border-b border-gray-200 print:hidden"&gt;&lt;div className="relative"&gt;&lt;Search className="absolute left-3 top-1/2 -translate-y-...` |
| 232 | **Button** | `{topProducts.length &gt; 0 && &lt;div className="bg-gray-50 border-b border-gray-200 p-2 overflow-x-auto no-scrollbar shrink-0 print:hidden"&gt;&lt;p className="t...` |
| 233 | **Button** | `&lt;div className="bg-white border-b border-gray-200 overflow-x-auto no-scrollbar shrink-0 print:hidden"&gt;&lt;div className="flex p-2 gap-2"&gt;&lt;button onClick=...` |
| 234 | **Button** | `&lt;div className="flex-1 overflow-y-auto p-2 grid grid-cols-2 gap-2 content-start print:hidden"&gt;{filteredProducts.map(product =&gt; (&lt;button key={product.i...` |
| 235 | **Button** | `&lt;div className="bg-white border-t border-gray-200 p-4 safe-area-bottom shadow-[0_-4px_10px_rgba(0,0,0,0.1)] print:hidden"&gt;&lt;div className="flex justify...` |
| 236 | **Button** | `{isCartOpen && (&lt;div className="fixed inset-0 z-50 bg-black/50 flex justify-end print:hidden"&gt;&lt;div className="w-full max-w-md bg-white h-full flex fle...` |

## 📄 `app\trust\layout.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 15 | **Link** | `&lt;Link href="/" className="flex items-center gap-2 group"&gt;` |
| 23 | **Link** | `&lt;Link href="/trust" className="hover:text-orange-600 transition-colors"&gt;Visão Geral&lt;/Link&gt;` |
| 24 | **Link** | `&lt;Link href="/trust/status" className="hover:text-orange-600 transition-colors"&gt;Status do Sistema&lt;/Link&gt;` |
| 25 | **Link** | `&lt;Link href="/trust/security" className="hover:text-orange-600 transition-colors"&gt;Segurança & Compliance&lt;/Link&gt;` |
| 28 | **Link** | `&lt;Link href="/" className="text-sm font-medium text-gray-500 hover:text-gray-900 flex items-center gap-1"&gt;` |

## 📄 `app\trust\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 23 | **Link** | `&lt;Link href="/trust/status" className="group bg-white p-8 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-all hover:border-oran...` |
| 37 | **Link** | `&lt;Link href="/trust/security" className="group bg-white p-8 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-all hover:border-bl...` |

## 📄 `app\trust\security\page.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 67 | **Anchor** | `&lt;a href="/privacy" className="text-orange-600 font-bold text-sm hover:underline"&gt;Ler Política de Privacidade&lt;/a&gt;` |

## 📄 `app\[slug]\menu\MenuClient.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 475 | **Button** | `&lt;button type="button" onClick={() =&gt; setIsComandaOpen(true)} className="text-xs font-bold bg-gray-100 px-3 py-1.5 rounded-full flex items-center gap-1...` |
| 624 | **Button** | `&lt;button type="button" onClick={() =&gt; setIsCartOpen(true)} className="text-white px-6 py-3 rounded-xl font-bold shadow-lg flex items-center gap-2 activ...` |
| 670 | **Button** | `&lt;button type="button" onClick={() =&gt; setIsCartOpen(false)} className="text-gray-400"&gt;&lt;X size={24}/&gt;&lt;/button&gt;` |
| 675 | **Clickable Div/Span** | `&lt;div className="cursor-pointer flex-1" onClick={() =&gt; handleEditCartItem(idx)}&gt;` |
| 685 | **Button** | `&lt;button type="button" onClick={() =&gt; removeFromCart(idx)} className="text-red-500 text-xs mt-1 hover:underline"&gt;Remover&lt;/button&gt;` |
| 695 | **Input** | `&lt;input type="text" className="w-full border border-gray-200 p-3 rounded-lg bg-white outline-none focus:ring-2 focus:ring-orange-500 text-gray-900" pla...` |
| 703 | **Input** | `&lt;input type="tel" className="w-full border border-gray-200 p-3 rounded-lg bg-white outline-none focus:ring-2 focus:ring-orange-500 text-gray-900" plac...` |
| 707 | **Textarea** | `&lt;textarea className="w-full border border-gray-200 p-3 rounded-lg bg-white outline-none focus:ring-2 focus:ring-orange-500 text-gray-900" placeholder=...` |
| 715 | **Input** | `&lt;input type="tel" className="w-full border border-gray-200 p-3 rounded-lg bg-white outline-none focus:ring-2 focus:ring-orange-500 text-gray-900" plac...` |
| 771 | **Button** | `&lt;button type="button" onClick={() =&gt; setPaymentMethod("online")} className={'flex flex-col items-center gap-1 p-3 rounded-lg border transition-all ${p...` |
| 775 | **Button** | `&lt;button type="button" onClick={() =&gt; setPaymentMethod("card")} className={'flex flex-col items-center gap-1 p-3 rounded-lg border transition-all ${pay...` |
| 779 | **Button** | `&lt;button type="button" onClick={() =&gt; setPaymentMethod("card")} className={'flex flex-col items-center gap-1 p-3 rounded-lg border transition-all ${pay...` |
| 783 | **Button** | `&lt;button type="button" onClick={() =&gt; setPaymentMethod("pix")} className={'flex flex-col items-center gap-1 p-3 rounded-lg border transition-all ${paym...` |
| 786 | **Button** | `&lt;button type="button" onClick={() =&gt; setPaymentMethod("cash")} className={'flex flex-col items-center gap-1 p-3 rounded-lg border transition-all ${pay...` |
| 811 | **Button** | `&lt;button type="button" onClick={() =&gt; setIsCartOpen(false)} className="flex-1 border border-gray-300 py-3 rounded-lg font-medium text-gray-700"&gt;Voltar&lt;...` |

## 📄 `components\admin\RecipeModal.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 110 | **Button** | `&lt;button onClick={() =&gt; handleRemoveItem(idx)} className="text-red-400 hover:text-red-600 p-1"&gt;` |
| 151 | **Button** | `&lt;button onClick={handleSave} className="w-full bg-orange-600 text-white py-3 rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-oran...` |

## 📄 `components\admin\StockModal.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 84 | **Input** | `&lt;input type="checkbox" className="sr-only peer" checked={product.is_available} onChange={() =&gt; toggleAvailability(product)} /&gt;` |

## 📄 `components\admin\KDS\ItemAggregator.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 80 | **Button** | `&lt;button onClick={onClose} className="p-2 hover:bg-gray-800 rounded-full text-gray-400 hover:text-white transition-colors"&gt;` |

## 📄 `components\landing\DemoModal.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 52 | **Button** | `&lt;button onClick={onClose} className="absolute top-6 right-6 text-gray-400 hover:text-gray-600 transition-colors"&gt;` |

## 📄 `components\landing\Footer.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 59 | **Link** | `&lt;li&gt;&lt;Link href="/#recursos" className="hover:text-orange-500 transition-colors"&gt;Cardápio Digital&lt;/Link&gt;&lt;/li&gt;` |
| 60 | **Link** | `&lt;li&gt;&lt;Link href="/#recursos" className="hover:text-orange-500 transition-colors"&gt;KDS (Cozinha)&lt;/Link&gt;&lt;/li&gt;` |
| 61 | **Link** | `&lt;li&gt;&lt;Link href="/#recursos" className="hover:text-orange-500 transition-colors"&gt;Fidelidade & Cashback&lt;/Link&gt;&lt;/li&gt;` |
| 62 | **Link** | `&lt;li&gt;&lt;Link href="/#solucoes" className="hover:text-orange-500 transition-colors"&gt;Integrações Hub&lt;/Link&gt;&lt;/li&gt;` |
| 63 | **Link** | `&lt;li&gt;&lt;Link href="/admin/register" className="text-orange-500 hover:text-orange-400"&gt;Criar Conta Grátis&lt;/Link&gt;&lt;/li&gt;` |
| 70 | **Link** | `&lt;li&gt;&lt;Link href="/trust" className="hover:text-orange-500 transition-colors"&gt;Sobre Nós&lt;/Link&gt;&lt;/li&gt;` |
| 71 | **Link** | `&lt;li&gt;&lt;Link href="/trust" className="hover:text-orange-500 transition-colors"&gt;Carreiras&lt;/Link&gt;&lt;/li&gt;` |
| 72 | **Link** | `&lt;li&gt;&lt;Link href="/trust" className="hover:text-orange-500 transition-colors"&gt;Blog Técnico&lt;/Link&gt;&lt;/li&gt;` |
| 73 | **Link** | `&lt;li&gt;&lt;Link href="/trust" className="hover:text-orange-500 transition-colors"&gt;Contato&lt;/Link&gt;&lt;/li&gt;` |
| 75 | **Link** | `&lt;Link href="/trust/status" className="flex items-center gap-2 hover:text-orange-500 transition-colors"&gt;` |
| 87 | **Form** | `&lt;form onSubmit={handleNewsletterSubmit} className="flex gap-2"&gt;` |
| 126 | **Link** | `&lt;Link href="/trust/security" className="hover:text-white transition-colors"&gt;Termos de Uso&lt;/Link&gt;` |
| 127 | **Link** | `&lt;Link href="/trust/security" className="hover:text-white transition-colors"&gt;Privacidade&lt;/Link&gt;` |
| 128 | **Link** | `&lt;Link href="/trust/security" className="hover:text-white transition-colors"&gt;Segurança&lt;/Link&gt;` |

## 📄 `components\landing\LeadCapture.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 118 | **Form** | `&lt;form onSubmit={handleSubmit} className="space-y-4"&gt;` |

## 📄 `components\landing\LeadMagnet.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 96 | **Form** | `&lt;form onSubmit={handleDownload} className="flex flex-col sm:flex-row gap-4"&gt;` |

## 📄 `components\landing\Navbar.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 40 | **Link** | `&lt;Link href="/"&gt;` |
| 45 | **Anchor** | `&lt;a href="#solucoes" className="hover:text-orange-600 transition-colors"&gt;{t.navbar.solutions}&lt;/a&gt;` |
| 46 | **Anchor** | `&lt;a href="#recursos" className="hover:text-orange-600 transition-colors"&gt;{t.navbar.features}&lt;/a&gt;` |
| 47 | **Anchor** | `&lt;a href="#precos" className="hover:text-orange-600 transition-colors"&gt;{t.navbar.pricing}&lt;/a&gt;` |
| 67 | **Button** | `&lt;button onClick={() =&gt; toggleLanguage('pt')} className="block w-full text-left px-4 py-3 text-xs font-bold hover:bg-slate-50 dark:hover:bg-slate-700 d...` |
| 68 | **Button** | `&lt;button onClick={() =&gt; toggleLanguage('en')} className="block w-full text-left px-4 py-3 text-xs font-bold hover:bg-slate-50 dark:hover:bg-slate-700 d...` |
| 69 | **Button** | `&lt;button onClick={() =&gt; toggleLanguage('es')} className="block w-full text-left px-4 py-3 text-xs font-bold hover:bg-slate-50 dark:hover:bg-slate-700 d...` |

## 📄 `components\landing\Pricing.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 22 | **Clickable Div/Span** | `&lt;div className="flex items-center justify-center gap-4 cursor-pointer" onClick={() =&gt; setIsAnnual(!isAnnual)}&gt;` |
| 48 | **Link** | `&lt;Link href="/admin/register?plan=free" className="block w-full py-3 rounded-xl border border-gray-600 text-center font-bold hover:bg-gray-700 transiti...` |
| 68 | **Link** | `&lt;Link href="/admin/register?plan=pro" className="block w-full py-3 rounded-xl bg-white text-orange-600 text-center font-bold hover:bg-gray-100 transit...` |
| 86 | **Button** | `&lt;button onClick={() =&gt; alert("Abrindo Calendly...")} className="w-full py-3 rounded-xl border border-gray-600 text-center font-bold hover:bg-gray-700 ...` |

## 📄 `components\landing\QualifyModal.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 32 | **Button** | `&lt;button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"&gt;&lt;X size={24}/&gt;&lt;/button&gt;` |
| 45 | **Button** | `&lt;button key={item} onClick={() =&gt; handleSegment(item)} className="flex items-center justify-between p-4 border border-gray-200 rounded-xl hover:border...` |
| 57 | **Button** | `&lt;button onClick={() =&gt; handleFinish("low")} className="p-4 border border-gray-200 rounded-xl hover:border-green-500 hover:bg-green-50 transition-all t...` |
| 61 | **Button** | `&lt;button onClick={() =&gt; handleFinish("high")} className="p-4 border border-gray-200 rounded-xl hover:border-purple-500 hover:bg-purple-50 transition-al...` |

## 📄 `components\menu\ComandaView.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 17 | **Button** | `&lt;button onClick={onClose} className="bg-gray-100 p-2 rounded-full hover:bg-gray-200 transition-colors"&gt;&lt;X size={20}/&gt;&lt;/button&gt;` |
| 64 | **Button** | `&lt;button onClick={onClose} className="flex-1 py-3.5 rounded-xl font-bold text-white shadow-lg active:scale-95 transition-transform" style={{ background...` |

## 📄 `components\menu\FeedbackModal.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 47 | **Button** | `&lt;button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"&gt;&lt;X size={24}/&gt;&lt;/button&gt;` |

## 📄 `components\menu\MenuClient.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 473 | **Button** | `&lt;button onClick={() =&gt; setIsComandaOpen(true)} className="text-xs font-bold bg-gray-100 px-3 py-1.5 rounded-full flex items-center gap-1 hover:bg-gray...` |
| 612 | **Button** | `&lt;button onClick={() =&gt; setIsCartOpen(true)} className="text-white px-6 py-3 rounded-xl font-bold shadow-lg flex items-center gap-2 active:scale-95 tra...` |
| 657 | **Button** | `&lt;button onClick={() =&gt; setIsCartOpen(false)} className="text-gray-400"&gt;&lt;X size={24}/&gt;&lt;/button&gt;` |
| 663 | **Clickable Div/Span** | `&lt;div className="cursor-pointer flex-1" onClick={() =&gt; handleEditCartItem(idx)}&gt;` |
| 673 | **Button** | `&lt;button onClick={() =&gt; removeFromCart(idx)} className="text-red-500 text-xs mt-1 hover:underline"&gt;Remover&lt;/button&gt;` |
| 683 | **Input** | `&lt;input type="text" className="w-full border border-gray-200 p-3 rounded-lg bg-white outline-none focus:ring-2 focus:ring-orange-500 text-gray-900" pla...` |
| 691 | **Input** | `&lt;input type="tel" className="w-full border border-gray-200 p-3 rounded-lg bg-white outline-none focus:ring-2 focus:ring-orange-500 text-gray-900" plac...` |
| 695 | **Textarea** | `&lt;textarea className="w-full border border-gray-200 p-3 rounded-lg bg-white outline-none focus:ring-2 focus:ring-orange-500 text-gray-900" placeholder=...` |
| 703 | **Input** | `&lt;input type="tel" className="w-full border border-gray-200 p-3 rounded-lg bg-white outline-none focus:ring-2 focus:ring-orange-500 text-gray-900" plac...` |
| 758 | **Button** | `&lt;button onClick={() =&gt; setPaymentMethod("online")} className={'flex flex-col items-center gap-1 p-3 rounded-lg border transition-all ${paymentMethod =...` |
| 762 | **Button** | `&lt;button onClick={() =&gt; setPaymentMethod("card")} className={'flex flex-col items-center gap-1 p-3 rounded-lg border transition-all ${paymentMethod ===...` |
| 766 | **Button** | `&lt;button onClick={() =&gt; setPaymentMethod("card")} className={'flex flex-col items-center gap-1 p-3 rounded-lg border transition-all ${paymentMethod ===...` |
| 770 | **Button** | `&lt;button onClick={() =&gt; setPaymentMethod("pix")} className={'flex flex-col items-center gap-1 p-3 rounded-lg border transition-all ${paymentMethod === ...` |
| 773 | **Button** | `&lt;button onClick={() =&gt; setPaymentMethod("cash")} className={'flex flex-col items-center gap-1 p-3 rounded-lg border transition-all ${paymentMethod ===...` |
| 798 | **Button** | `&lt;button onClick={() =&gt; setIsCartOpen(false)} className="flex-1 border border-gray-300 py-3 rounded-lg font-medium text-gray-700"&gt;Voltar&lt;/button&gt;` |

## 📄 `components\menu\OrderStatusView.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 132 | **Input** | `&lt;input readOnly value={order.mp_qr_code} className="flex-1 bg-gray-100 border border-gray-200 rounded-lg px-3 py-2 text-xs text-gray-600 truncate" /&gt;` |
| 133 | **Button** | `&lt;button onClick={copyToClipboard} className="bg-gray-900 text-white p-2 rounded-lg hover:bg-gray-800"&gt;&lt;Copy size={16} /&gt;&lt;/button&gt;` |

## 📄 `components\menu\ServiceModal.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 43 | **Button** | `&lt;button onClick={onClose} className="text-gray-400 hover:text-gray-600"&gt;&lt;X size={24}/&gt;&lt;/button&gt;` |

## 📄 `components\menu\SplitBillModal.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 69 | **Button** | `&lt;button onClick={onClose} className="bg-gray-200 p-2 rounded-full hover:bg-gray-300 transition-colors"&gt;&lt;X size={20}/&gt;&lt;/button&gt;` |

## 📄 `components\menu\UpsellModal.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 24 | **Button** | `&lt;button onClick={() =&gt; onAdd(rec)} className="bg-white border border-gray-200 hover:bg-orange-50 hover:border-orange-200 text-gray-700 hover:text-oran...` |
| 30 | **Button** | `&lt;button onClick={onFinish} className="w-full text-white py-3.5 rounded-xl font-bold shadow-md flex items-center justify-center gap-2 active:scale-95 t...` |

## 📄 `components\menu\WalletWidget.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 53 | **Input** | `&lt;input type="checkbox" className="sr-only peer" checked={useBalance} onChange={(e) =&gt; onUseBalance(e.target.checked)} /&gt;` |

## 📄 `components\ui\CookieBanner.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 33 | **Button** | `&lt;button onClick={() =&gt; setIsVisible(false)} className="text-gray-500 hover:text-white transition-colors"&gt;` |

## 📄 `components\ui\Modal.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 30 | **Button** | `&lt;button onClick={onClose} className="text-gray-400 hover:text-white transition-colors"&gt;` |

## 📄 `components\waiter\BillAuditModal.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 117 | **Button** | `&lt;button onClick={onClose} className="text-orange-500 font-bold underline"&gt;Tentar novamente&lt;/button&gt;` |

## 📄 `components\waiter\ChangeCalculator.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 60 | **Button** | `&lt;button onClick={handleBackspace} className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-red-500 p-2"&gt;` |

## 📄 `components\waiter\PaymentModal.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 138 | **Button** | `&lt;button onClick={() =&gt; setIsEditingTip(!isEditingTip)} className="bg-gray-800 p-1 rounded hover:bg-gray-700 text-orange-500"&gt;` |
| 148 | **Button** | `&lt;button onClick={() =&gt; { setTipMode('percent'); setTipValue(10); }} className={'flex-1 py-1 text-xs rounded ${tipMode === 'percent' && tipValue === 10...` |
| 149 | **Button** | `&lt;button onClick={() =&gt; { setTipMode('percent'); setTipValue(12); }} className={'flex-1 py-1 text-xs rounded ${tipMode === 'percent' && tipValue === 12...` |
| 150 | **Button** | `&lt;button onClick={() =&gt; { setTipMode('percent'); setTipValue(0); }} className={'flex-1 py-1 text-xs rounded ${tipValue === 0 ? 'bg-red-600 text-white' ...` |

## 📄 `components\waiter\Receipt.tsx`
| Linha | Tipo | Snippet (Código) |
| :---: | :--- | :--- |
| 19 | **Button** | `&lt;button onClick={onClose \|\| (() =&gt; window.location.reload())} className="text-gray-400 hover:text-white"&gt;&lt;X size={20}/&gt;&lt;/button&gt;` |
