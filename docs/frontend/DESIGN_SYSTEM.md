🎨 MesaFlow Design System

Guia de referência para manter a consistência visual da interface.

1. Fundamentos

Fonte: Inter (Sans-serif). Legibilidade máxima em telas pequenas.

Raio de Borda: rounded-xl (12px) para cards e inputs. rounded-full para botões de ação.

Sombras: Suaves e difusas (shadow-lg, shadow-orange-500/20).

2. Paleta de Cores (Tailwind)
Nome	Token	Uso
Primary	bg-orange-600	Botões de ação principal (CTA), Destaques.
Secondary	bg-gray-900	Sidebar, Cabeçalhos, Texto forte.
Success	bg-green-600	Confirmação, Pagamento, Status "Pronto".
Warning	bg-yellow-500	Status "Pendente", Alertas não bloqueantes.
Danger	bg-red-600	Erro, Cancelar, Status "Atrasado".
Surface	bg-white / bg-gray-50	Fundos de cards e páginas.
3. Componentes Core
Botões (Button)

Sempre com feedback tátil (active:scale-95) e transição de cor.

code
Tsx
download
content_copy
expand_less
<button className="bg-orange-600 hover:bg-orange-700 text-white font-bold py-3 px-6 rounded-xl transition-all shadow-lg active:scale-95 flex items-center gap-2">
  <Icon size={20} /> Label
</button>
Inputs (AuthInput)

Com ícone à esquerda e validação visual.

code
Tsx
download
content_copy
expand_less
<div className="relative">
  <Icon className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
  <input className="w-full pl-10 p-3 border rounded-xl focus:ring-2 focus:ring-orange-500 outline-none" />
</div>
Cards (Card)

Brancos, com borda sutil e sombra ao hover.

code
Tsx
download
content_copy
expand_less
<div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
  {children}
</div>
Badges de Status

Pílulas com fundo translúcido.

code
Tsx
download
content_copy
expand_less
<span className="bg-green-100 text-green-700 px-2 py-1 rounded text-xs font-bold uppercase">
  Pago
</span>
4. Animações (Framer Motion / Tailwind)

Entrada de Página: animate-in fade-in slide-in-from-bottom-4.

Modais: zoom-in rápido (200ms).

Skeletons: animate-pulse em cinza claro (bg-gray-200).
