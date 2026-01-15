# DOMAIN: FRONTEND
# LAST_MODIFIED: 2026-01-15 02:30:00
import { getToken, getRefreshToken, setTokens, removeTokens } from "./auth";
import { Company, Ingredient, RecipeItem, Promotion, CouponValidationResponse } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function fetchClient(endpoint: string, options: RequestInit = {}) {
  const token = getToken();
  const headers: any = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  let response;
  try {
    response = await fetch(`${API_BASE_URL}${endpoint}`, { ...options, headers });
  } catch (error) {
    console.error("Erro de conexão com API:", error);
    throw new ApiError("Servidor indisponível. Verifique sua conexão.", 0);
  }

  if (response.status === 401) {
    const refreshToken = getRefreshToken();
    if (!refreshToken) {
      removeTokens();
      if (typeof window !== "undefined" && !window.location.pathname.includes("/login")) {
        window.location.href = "/admin/login";
      }
      throw new ApiError("Sessão expirada", 401);
    }
    try {
      const refreshRes = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: "POST",
        headers: { "X-Refresh-Token": refreshToken },
      });
      if (refreshRes.ok) {
        const data = await refreshRes.json();
        setTokens(data.access_token, data.refresh_token);
        headers["Authorization"] = `Bearer ${data.access_token}`;
        response = await fetch(`${API_BASE_URL}${endpoint}`, { ...options, headers });
      } else {
        throw new Error("Refresh falhou");
      }
    } catch (e) {
      removeTokens();
      if (typeof window !== "undefined" && !window.location.pathname.includes("/login")) {
        window.location.href = "/admin/login";
      }
      throw new ApiError("Sessão expirada", 401);
    }
  }

  if (!response.ok) {
    let errorMessage = "Erro na requisição";
    try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorMessage;
    } catch (e) {}
    throw new ApiError(errorMessage, response.status);
  }
  return response;
}

// --- PUBLIC API ---
export async function getMenu(slug: string) {
  const res = await fetch(`${API_BASE_URL}/${slug}/menu`, { cache: "no-store" });
  return res.json();
}

export async function getPublicMonitorOrders(slug: string) {
  const res = await fetch(`${API_BASE_URL}/${slug}/monitor`, { cache: "no-store" });
  return res.json();
}

export async function getWallet(slug: string, phone: string) {
  try {
    const res = await fetch(`${API_BASE_URL}/${slug}/wallet/${phone}`);
    return res.json();
  } catch (e) {
    return { balance: 0, loyalty_percentage: 0 };
  }
}

export async function checkTableStatus(slug: string, tableId: number, qrToken: string, sessionToken?: string | null) {
  const res = await fetch(`${API_BASE_URL}/${slug}/check-table`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ table_id: tableId, qr_token: qrToken, session_token: sessionToken }),
  });
  return res.json();
}

export async function joinTable(slug: string, tableId: number, qrToken: string, customerName: string, pin?: string) {
  const res = await fetch(`${API_BASE_URL}/${slug}/join-table`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ table_id: tableId, qr_token: qrToken, customer_name: customerName, pin: pin }),
  });
  return res.json();
}

export async function createOrder(slug: string, data: any) {
  const res = await fetch(`${API_BASE_URL}/${slug}/orders`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

// --- ADMIN API ---
export async function login(username: string, password: string) {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);
  const res = await fetch(`${API_BASE_URL}/auth/token`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData,
  });
  return res.json();
}

export async function getDashboardMetrics(startDate?: string, endDate?: string) {
  const params = new URLSearchParams();
  if (startDate) params.append("start_date", startDate);
  if (endDate) params.append("end_date", endDate);
  const res = await fetchClient(`/admin/metrics?${params.toString()}`);
  return res.json();
}

export async function getKitchenOrders(slug: string) {
  const res = await fetchClient(`/admin/${slug}/orders`);
  return res.json();
}

export async function updateOrderStatus(slug: string, orderId: string, newStatus: string) {
  const res = await fetchClient(`/admin/orders/${orderId}`, {
    method: "PATCH",
    body: JSON.stringify({ status: newStatus }),
  });
  return res.json();
}

export async function getCompanySettings() {
  const res = await fetchClient(`/admin/company/me`);
  return res.json();
}

export async function getOrderHistory(slug: string, page = 1, limit = 10) {
  const res = await fetchClient(`/admin/${slug}/history?page=${page}&limit=${limit}`);
  return res.json();
}

// --- AUDIT & FINANCIAL (FIX: MISSING EXPORTS) ---
export async function getLedgerHistory(limit = 50) {
  const res = await fetchClient(`/admin/audit/financial/ledger?limit=${limit}`);
  return res.json();
}

export async function getReconciliationReport() {
  const res = await fetchClient(`/admin/audit/financial/reconciliation`);
  return res.json();
}

export async function verifyLedgerIntegrity() {
  const res = await fetchClient(`/admin/audit/financial/verify-integrity`);
  return res.json();
}

export async function fixOrphanTransaction(externalId: string) {
  const res = await fetchClient(`/admin/audit/financial/fix-orphan`, {
    method: "POST",
    body: JSON.stringify({ external_id: externalId })
  });
  return res.json();
}

export async function getAuditLogs(limit = 50) {
  const res = await fetchClient(`/admin/audit?limit=${limit}`);
  return res.json();
}

// --- OTHERS ---
export async function getServiceRequests(slug: string) {
  const res = await fetchClient(`/admin/${slug}/service-requests`);
  return res.json();
}

export async function getDrivers() {
  const res = await fetchClient(`/admin/employees?role=driver`);
  return res.json();
}

export async function getDriversWithBalance() {
  const res = await fetchClient(`/admin/logistics/drivers`);
  return res.json();
}

export async function settleDriverDebt(driverId: number, amount: number, description: string) {
  const res = await fetchClient(`/admin/logistics/drivers/${driverId}/settle`, {
    method: "POST",
    body: JSON.stringify({ amount, description })
  });
  return res.json();
}

export async function getFeatureFlags() {
  const res = await fetchClient(`/admin/features`);
  return res.json();
}

export async function updateFeatureFlag(key: string, isEnabled: boolean) {
  const res = await fetchClient(`/admin/features`, {
    method: "POST",
    body: JSON.stringify({ key, is_enabled: isEnabled })
  });
  return res.json();
}

export async function getWhatsappStatus() {
  const res = await fetchClient(`/admin/marketing/whatsapp/status`);
  return res.json();
}

export async function emitFiscalDocument(orderId: string) {
  const res = await fetchClient(`/admin/fiscal/orders/${orderId}/emit`, {
    method: "POST"
  });
  return res.json();
}
