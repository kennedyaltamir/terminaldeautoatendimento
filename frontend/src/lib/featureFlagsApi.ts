import { getToken } from "./auth";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

/**
 * Cliente isolado para gestão de Feature Flags.
 * Mantém o escopo fechado e evita modificações no api.ts legado.
 */
async function authenticatedFetch(endpoint: string, options: RequestInit = {}) {
  const token = getToken();
  const headers: any = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, { ...options, headers });

  if (!response.ok) {
    const error = new Error("Erro na requisição de Feature Flags");
    (error as any).status = response.status;
    throw error;
  }

  return response;
}

export async function getFeatureFlags() {
  const res = await authenticatedFetch("/admin/features");
  return res.json();
}

export async function updateFeatureFlag(key: string, isEnabled: boolean) {
  const res = await authenticatedFetch("/admin/features", {
    method: "POST",
    body: JSON.stringify({ key, is_enabled: isEnabled }),
  });
  return res.json();
}
