import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export async function middleware(req: NextRequest) {
  const url = req.nextUrl;
  
  // 1. Obter o Hostname (ex: pedidos.loja.com ou localhost:3000)
  let hostname = req.headers.get("host") || "";
  
  // Remover porta se existir (para localhost)
  hostname = hostname.split(":")[0];

  // 2. Definir Domínio Principal (Onde o SaaS roda)
  // Em dev: localhost. Em prod: app.mesaflow.com
  const mainDomain = process.env.NEXT_PUBLIC_ROOT_DOMAIN || "localhost";

  // 3. Verificar se é um Domínio Customizado
  // Se o hostname for diferente do domínio principal e não for um subdomínio de sistema (ex: www, app)
  const isCustomDomain = hostname !== mainDomain && hostname !== `www.${mainDomain}`;

  if (isCustomDomain) {
    // 4. Resolver o Slug (API Call)
    // Em produção, isso deve ser cacheado (Vercel KV ou Redis)
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";
      const res = await fetch(`${apiUrl}/resolve-domain?host=${hostname}`);
      
      if (res.ok) {
        const data = await res.json();
        const slug = data.slug;

        // 5. Reescrever a Rota
        // O usuário vê: pedidos.loja.com/
        // O Next renderiza: app.mesaflow.com/[slug]/menu
        
        // Mantém o path original (ex: /carrinho, /checkout)
        const path = url.pathname;
        
        // Se for a raiz, manda pro menu
        if (path === "/") {
           return NextResponse.rewrite(new URL(`/${slug}/menu`, req.url));
        }

        // Se for outra rota, mantém (ex: /admin não deve ser acessível aqui, mas o layout protege)
        return NextResponse.rewrite(new URL(`/${slug}/menu${path}`, req.url));
      }
    } catch (e) {
      console.error("Erro ao resolver domínio:", e);
    }
  }

  return NextResponse.next();
}

// Configuração para não rodar em arquivos estáticos
export const config = {
  matcher: [
    "/((?!api/|_next/|_static/|[\\w-]+\\.\\w+).*)",
  ],
};