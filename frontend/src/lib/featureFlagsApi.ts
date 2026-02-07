
import { getToken } from "./auth";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8001/api";

async function authenticatedFetch(endpoint: string, options: RequestInit = {}): Promise<Response> {
  const token = getToken();
  const headers: any = {
    "Content-Type": "application/json",
    ...options.headers,
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  // 🛡️ FIX: Remove barras duplicadas ou finais para evitar redirects de CORS
  const cleanPath = endpoint.replace(/\/$/, "").replace(/^\//, "");
  const url = `${API_BASE_URL}/${cleanPath}`;

  try {
    const response = await fetch(url, { ...options, headers });
    if (!response.ok) throw new Error(`HTTP_${response.status}`);
    return response;
  } catch (error: any) {
    throw error;
  }
}

export async function getFeatureFlags(): Promise<Record<string, boolean>> {
  try {
    const res = await authenticatedFetch("admin/features");
    return await res.json();
  } catch (error) {
    return {};
  }
}

export async function updateFeatureFlag(key: string, isEnabled: boolean) {
  const res = await authenticatedFetch("admin/features", {
    method: "POST",
    body: JSON.stringify({ key, is_enabled: isEnabled }),
  });
  return await res.json();
}
