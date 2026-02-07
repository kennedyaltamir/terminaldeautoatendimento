/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 2.1.0 (E2E Mock Injection)
 * DNA_ID: MF-AUTH-GUARD-V2-1
 * Objective: Server-side identity resolution with E2E mock support.
 */
import { cookies, headers } from "next/headers";
import { redirect } from "next/navigation";

export interface AuthSession {
  sub: string;
  email: string;
  role: string;
  name: string;
  company_id: string;
  iat?: number;
  exp?: number;
}

export async function requireAuth(requiredRole?: string): Promise<AuthSession | null> {
  const headersList = await headers();
  
  // 🛡️ E2E BYPASS: Detecção de modo de teste via Header injetado pelo Middleware
  const isE2E = headersList.get("x-mesaflow-e2e-auth") === "true" || headersList.get("x-e2e-test") === "true";

  if (isE2E) {
    // Retorna identidade sintética de Motorista para testes forenses
    return {
      sub: "999",
      email: "admin@mesaflow.com",
      role: "driver",
      name: "Auditor Forense",
      company_id: "00000000-0000-0000-0000-000000000000",
      iat: Date.now(),
      exp: Date.now() + 3600 * 24 // 24h validade
    };
  }

  const currentPath = headersList.get("x-mesaflow-path") || "";
  
  // Bypass para páginas de login/recuperação
  const isAuthPage = [
    "/admin/login", 
    "/admin/register", 
    "/admin/forgot-password",
    "/admin/reset-password",
    "/admin/support"
  ].some(path => currentPath.startsWith(path));

  if (isAuthPage) return null;

  const cookieStore = await cookies();
  const token = cookieStore.get("auth_token")?.value;

  if (!token) {
    // Se não tem token e não é página de login, redireciona
    if (!currentPath.includes("/login")) {
        redirect("/admin/login");
    }
    return null;
  }

  try {
    // Suporte a token mockado manualmente (legado)
    if (token.includes("mock-token")) {
      return { 
        sub: "admin@test.com", 
        email: "admin@test.com",
        role: "owner", 
        name: "Mock Admin",
        company_id: "test-id" 
      };
    }

    const parts = token.split('.');
    if (parts.length !== 3) throw new Error("Invalid JWT Format");
    
    const payload = JSON.parse(Buffer.from(parts[1], 'base64').toString());
    const now = Math.floor(Date.now() / 1000);
    
    if (payload.exp && payload.exp < now) throw new Error("Expired");
    
    // Validação de Role
    if (requiredRole && payload.role !== requiredRole && payload.role !== 'owner') {
      redirect("/admin/login?error=unauthorized");
    }

    return payload as AuthSession;

  } catch (e) {
    console.error("🚨 [AuthGuard] Falha crítica no token:", e);
    redirect("/admin/login?error=invalid_session");
  }
}
