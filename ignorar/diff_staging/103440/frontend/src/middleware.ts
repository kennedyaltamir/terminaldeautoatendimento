// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 13:45:00
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export async function middleware(req: NextRequest) {
  const url = req.nextUrl;
  const path = url.pathname;

  // 1. Obter o Hostname
  let hostname = req.headers.get("host") || "";
  hostname = hostname.split(":")[0];

  // 2. Definir Domínio Principal
  const mainDomain = process.env.NEXT_PUBLIC_ROOT_DOMAIN || "localhost";

  // 3. SEGURANÇA: Ignorar rotas administrativas e de API da reescrita de tenant
  if (path.startsWith("/admin") || path.startsWith("/api") || path.startsWith("/_next")) {
    return NextResponse.next();
  }

  // 4. Verificar se é um Domínio Customizado (ou localhost em dev)
  const isCustomDomain = hostname !== mainDomain && hostname !== `www.${mainDomain}`;

  if (isCustomDomain) {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";
      const res = await fetch(`${apiUrl}/resolve-domain?host=${hostname}`);
      
      if (res.ok) {
        const data = await res.json();
        const slug = data.slug;

        // 5. Reescrever para o escopo do Menu do Cliente
        if (path === "/") {
           return NextResponse.rewrite(new URL(`/${slug}/menu`, req.url));
        }
        
        // Evita recursão se já estiver no path do slug
        if (!path.startsWith(`/${slug}`)) {
          return NextResponse.rewrite(new URL(`/${slug}/menu${path}`, req.url));
        }
      }
    } catch (e) {
      console.error("Erro ao resolver domínio no middleware:", e);
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/((?!api/|_next/|_static/|[\\w-]+\\.\\w+).*)",
  ],
};
