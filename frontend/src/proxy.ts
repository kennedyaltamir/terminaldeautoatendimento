/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 16.1.0 (Named Export Fix)
 * DNA_ID: MF-PROXY-V16-1-GOLD
 * Objective: Next.js 16 compliant request interception with Named Export.
 */
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// 🛡️ FIX: Exportação NOMEADA obrigatória para a convenção proxy.ts
export async function proxy(req: NextRequest) {
  const { pathname } = req.nextUrl;

  // 🛡️ PROTOCOLO DE AUDITORIA FORENSE (E2E Bypass)
  const isE2E = req.headers.get('x-e2e-test') === 'true';

  if (isE2E) {
    const requestHeaders = new Headers(req.headers);
    requestHeaders.set("x-mesaflow-e2e-auth", "true");
    requestHeaders.set("x-mesaflow-path", pathname);
    
    return NextResponse.next({
      request: { headers: requestHeaders }
    });
  }

  const token = req.cookies.get("auth_token")?.value;
  
  // Rotas públicas
  const isPublicRoute = 
    pathname === "/" ||
    pathname === "/offline" ||
    pathname.startsWith("/trust") ||
    pathname.includes("/menu") ||   
    pathname.includes("/kiosk") ||
    pathname.includes("/checkout") || 
    pathname.includes("/monitor");

  if (isPublicRoute || pathname.startsWith("/_next") || pathname.includes(".")) {
    return NextResponse.next();
  }

  // 🔐 Bloqueio Administrativo
  if (pathname.startsWith("/admin") && !pathname.includes("/login") && !token) {
    const loginUrl = new URL("/admin/login", req.url);
    loginUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
