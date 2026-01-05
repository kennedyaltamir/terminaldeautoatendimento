import Skeleton from "@/components/ui/Skeleton";

export default function MenuSkeleton() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 pb-20 font-sans transition-colors duration-300">
      {/* Header Sticky */}
      <div className="sticky top-0 z-30 bg-white/95 dark:bg-gray-900/95 backdrop-blur-sm shadow-sm border-b border-gray-100 dark:border-gray-800">
        <div className="p-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            {/* Logo */}
            <Skeleton className="w-10 h-10 rounded-lg" />
            {/* Nome do Restaurante */}
            <Skeleton className="w-32 h-6 rounded-md" />
          </div>
          <div className="flex gap-3">
            {/* Botões de Ação (Sino/Comanda) */}
            <Skeleton className="w-8 h-8 rounded-full" />
            <Skeleton className="w-8 h-8 rounded-full" />
          </div>
        </div>

        {/* Barra de Busca */}
        <div className="px-4 pt-2 pb-2">
          <Skeleton className="w-full h-12 rounded-xl" />
        </div>

        {/* Tags (Opcional) */}
        <div className="flex overflow-x-hidden px-4 pb-2 gap-2">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="w-16 h-6 rounded-full shrink-0" />
          ))}
        </div>

        {/* Navegação de Categorias */}
        <div className="flex overflow-x-hidden py-3 px-4 gap-3 border-t border-gray-100 dark:border-gray-800">
          {[1, 2, 3, 4, 5].map((i) => (
            <Skeleton key={i} className="w-24 h-8 rounded-full shrink-0" />
          ))}
        </div>
      </div>

      {/* Banner (Opcional) */}
      <div className="w-full h-40 md:h-64 relative">
        <Skeleton className="w-full h-full" />
      </div>

      {/* Lista de Produtos */}
      <main className="p-4 space-y-8">
        {[1, 2].map((section) => (
          <section key={section} className="space-y-4">
            {/* Título da Categoria */}
            <div className="flex items-center gap-2 mb-4">
              <Skeleton className="w-1 h-6 rounded-full" />
              <Skeleton className="w-40 h-6 rounded-md" />
            </div>

            {/* Cards de Produto */}
            <div className="space-y-4">
              {[1, 2, 3].map((card) => (
                <div 
                  key={card} 
                  className="bg-white dark:bg-gray-900 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800 flex justify-between items-center h-32"
                >
                  <div className="flex-1 pr-4 space-y-2">
                    {/* Nome do Produto */}
                    <Skeleton className="w-3/4 h-5 rounded-md" />
                    {/* Descrição (2 linhas) */}
                    <Skeleton className="w-full h-3 rounded-md" />
                    <Skeleton className="w-1/2 h-3 rounded-md" />
                    
                    {/* Preço */}
                    <div className="pt-2">
                      <Skeleton className="w-20 h-5 rounded-md" />
                    </div>
                  </div>
                  
                  {/* Imagem do Produto */}
                  <div className="flex flex-col items-center gap-2">
                    <Skeleton className="w-20 h-20 rounded-lg" />
                    <Skeleton className="w-8 h-8 rounded-full" />
                  </div>
                </div>
              ))}
            </div>
          </section>
        ))}
      </main>

      {/* Footer Fixo (Carrinho) */}
      <div className="fixed bottom-0 left-0 w-full bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800 p-4 z-20">
        <div className="flex justify-between items-center max-w-md mx-auto gap-4">
          <div className="flex flex-col gap-1">
            <Skeleton className="w-16 h-3 rounded-md" />
            <Skeleton className="w-24 h-6 rounded-md" />
          </div>
          <Skeleton className="w-40 h-12 rounded-xl" />
        </div>
      </div>
    </div>
  );
}
