// DOMAIN: SECURITY
// LAST_MODIFIED: 2026-01-18 09:30:00
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// =============================================================================
// 🛡️ MESAFLOW SECURITY MIDDLEWARE (Context-Aware v2)
// =============================================================================
// Responsabilidades:
// 1. Sandbox de Kiosk (Totem Trap via Cookie)
// 2. Proteção de Rotas Administrativas
// 3. Normalização de Headers e Bypass de Assets
// =============================================================================

// Configurações de Segurança
const ENFORCE_ADMIN_COOKIE = false; // Feature Flag: Ativar para exigir cookie de sessão no servidor
const PUBLIC_FILE_EXTENSIONS = [".svg", ".png", ".jpg", ".jpeg", ".ico", ".css", ".js", ".woff", ".woff2", ".ttf"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // 1. Bypass de Arquivos Estáticos e API Interna do Next.js
  // Otimização: Retorna cedo para não processar lógica em assets
  if (
    pathname.startsWith("/_next") ||
    pathname.startsWith("/static") ||
    PUBLIC_FILE_EXTENSIONS.some((ext) => pathname.endsWith(ext))
  ) {
    return NextResponse.next();
  }

  // 2. Definição de Contextos (Regex para precisão)
  // Detecta: /slug/kiosk, /kiosk, /slug/totem
  // Evita falsos positivos como: /admin/kiosk-settings
  const isKioskRoute = /^\/([^/]+\/)?(kiosk|totem)/.test(pathname);
  const isAdminRoute = pathname.startsWith("/admin");
  const isLoginRoute = pathname.startsWith("/admin/login") || pathname.startsWith("/admin/register") || pathname.startsWith("/admin/forgot-password");
  
  // Verifica marcador de sessão Kiosk (Cookie HttpOnly)
  const hasKioskContext = request.cookies.get("mf_kiosk_mode")?.value === "1";

  // 3. KIOSK ENTRY (Marcação de Sessão)
  // Se o usuário entrar na rota de Kiosk, marcamos a sessão com um cookie seguro.
  if (isKioskRoute) {
    const response = NextResponse.next();
    // Define o cookie de contexto. Path '/' garante que ele seja enviado em todas as rotas subsequentes.
    response.cookies.set("mf_kiosk_mode", "1", { 
        path: "/", 
        httpOnly: true, // JS não pode ler (segurança contra XSS)
        sameSite: "lax" 
    });
    return response;
  }

  // 4. KIOSK TRAP (Sandbox Enforcement)
  // Se a sessão está marcada como Kiosk, PROIBIR acesso ao Admin.
  // Isso impede que alguém digite /admin na barra de endereço do totem.
  if (isAdminRoute && hasKioskContext) {
    // Tenta redirecionar para a origem (Referer) se for segura, ou para a home pública
    const referer = request.headers.get("referer");
    const targetUrl = referer && referer.includes("/kiosk") ? referer : new URL("/", request.url);
    
    return NextResponse.redirect(targetUrl);
  }

  // 5. ADMIN GUARD (Proteção Básica)
  // Redireciona para login se tentar acessar admin sem sessão (se a flag estiver ativa)
  if (isAdminRoute && !isLoginRoute && ENFORCE_ADMIN_COOKIE) {
    const hasSessionCookie = request.cookies.has("mesaflow_session");
    if (!hasSessionCookie) {
        return NextResponse.redirect(new URL("/admin/login", request.url));
    }
  }

  // 6. Tratamento de Subdomínios (Multi-tenant - Placeholder)
  // Espaço reservado para lógica de rewrite de domínios customizados no futuro.

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    "/((?!api|_next/static|_next/image|favicon.ico).*)",
  ],
};

