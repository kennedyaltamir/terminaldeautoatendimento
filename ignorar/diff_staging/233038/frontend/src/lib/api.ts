# DOMAIN: FRONTEND
# LAST_MODIFIED: 2026-01-15 02:40:00
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
  try {
    const res = await fetch(`${API_BASE_URL}/${slug}/menu`, { cache: "no-store" });
    if (!res.ok) throw new Error("Falha ao carregar cardápio");
    return res.json();
  } catch (error) {
    console.error("Erro ao buscar menu:", error);
    throw new Error("Não foi possível carregar o cardápio. O sistema pode estar offline.");
  }
}

export async function getPublicMonitorOrders(slug: string) {
  const res = await fetch(`${API_BASE_URL}/${slug}/monitor`, { cache: "no-store" });
  if (!res.ok) throw new Error("Falha ao carregar monitor");
  return res.json();
}

export async function getWallet(slug: string, phone: string) {
  try {
    const res = await fetch(`${API_BASE_URL}/${slug}/wallet/${phone}`);
    if (!res.ok) return { balance: 0, loyalty_percentage: 0 };
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
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Erro ao entrar na mesa");
  }
  return res.json();
}

export async function getTableSession(slug: string, sessionToken: string) {
  const res = await fetch(`${API_BASE_URL}/${slug}/session/${sessionToken}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Erro ao carregar comanda");
  return res.json();
}

export async function createOrder(slug: string, data: any) {
  const res = await fetch(`${API_BASE_URL}/${slug}/orders`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || "Erro ao enviar pedido");
  }
  return res.json();
}

export async function processOnlinePayment(data: any) {
  const res = await fetch(`${API_BASE_URL}/payments/process`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || "Falha no pagamento");
  }
  return res.json();
}

export async function getOrder(orderId: string) {
  const res = await fetch(`${API_BASE_URL}/orders/${orderId}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Falha ao consultar pedido");
  return res.json();
}

export async function requestService(slug: string, data: { table_id: number, qr_token: string, service_type: string, notes?: string }) {
  const res = await fetch(`${API_BASE_URL}/${slug}/service`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Erro ao chamar garçom");
  return res.json();
}

// --- ADMIN API ---
export async function login(username: string, password: string) {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);
  try {
    const res = await fetch(`${API_BASE_URL}/auth/token`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
    });
    if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Login falhou.");
    }
    const data = await res.json();
    setTokens(data.access_token, data.refresh_token);
    return data;
  } catch (error: any) {
    throw new Error(error.message || "Erro de conexão ao tentar login.");
  }
}

export async function register(data: any) {
  const res = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || "Falha no cadastro");
  }
  const responseData = await res.json();
  setTokens(responseData.access_token, responseData.refresh_token);
  return responseData;
}

export async function getDashboardMetrics(startDate?: string, endDate?: string) {
  let query = "";
  const params = new URLSearchParams();
  if (startDate) params.append("start_date", startDate);
  if (endDate) params.append("end_date", endDate);
  if (params.toString()) query = `?${params.toString()}`;
  const res = await fetchClient(`/admin/metrics${query}`);
  return res.json();
}

export async function getKitchenOrders(slug: string) {
  const res = await fetchClient(`/admin/${slug}/orders`);
  return res.json();
}

export async function getRecentCompletedOrders(slug: string) {
  const res = await fetchClient(`/admin/${slug}/orders/recent-completed`);
  return res.json();
}

export async function getQuickProducts(slug: string) {
  const res = await fetchClient(`/admin/${slug}/products/quick-list`);
  return res.json();
}

export async function getOrderHistory(slug: string, page = 1, limit = 10) {
  const res = await fetchClient(`/admin/${slug}/history?page=${page}&limit=${limit}`);
  return res.json();
}

export async function updateOrderStatus(slug: string, orderId: string, newStatus: string) {
  const res = await fetchClient(`/admin/orders/${orderId}`, {
    method: "PATCH",
    body: JSON.stringify({ status: newStatus }),
  });
  return res.json();
}

export async function updateOrderPayment(orderId: string, newStatus: string) {
  const res = await fetchClient(`/admin/orders/${orderId}/payment`, {
    method: "PATCH",
    body: JSON.stringify({ payment_status: newStatus }),
  });
  return res.json();
}

export async function deleteProduct(productId: number) {
  const res = await fetchClient(`/admin/menu/products/${productId}`, { method: "DELETE" });
  return res.ok;
}

export async function deleteCategory(categoryId: number) {
  const res = await fetchClient(`/admin/menu/categories/${categoryId}`, { method: "DELETE" });
  return res.ok;
}

export async function createCategory(name: string) {
  const res = await fetchClient(`/admin/menu/categories`, {
    method: "POST",
    body: JSON.stringify({ name, order_index: 0 })
  });
  return res.json();
}

export async function createProduct(data: any) {
  const res = await fetchClient(`/admin/menu/products`, {
    method: "POST",
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function updateProduct(productId: number, data: any) {
  const res = await fetchClient(`/admin/menu/products/${productId}`, {
    method: "PATCH",
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function createOptionGroup(productId: number, data: any) {
  const res = await fetchClient(`/admin/menu/products/${productId}/groups`, {
    method: "POST",
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function deleteOptionGroup(groupId: number) {
  const res = await fetchClient(`/admin/menu/groups/${groupId}`, { method: "DELETE" });
  return res.ok;
}

export async function createOption(groupId: number, data: any) {
  const res = await fetchClient(`/admin/menu/groups/${groupId}/options`, {
    method: "POST",
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function deleteOption(optionId: number) {
  const res = await fetchClient(`/admin/menu/options/${optionId}`, { method: "DELETE" });
  return res.ok;
}

export async function getCompanySettings() {
  const res = await fetchClient(`/admin/company/me`);
  return res.json();
}

export async function updateCompanySettings(data: Partial<Company>) {
  const res = await fetchClient(`/admin/company/me`, {
    method: "PATCH",
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function updatePassword(data: any) {
  const res = await fetchClient(`/admin/company/me/password`, {
    method: "PATCH",
    body: JSON.stringify(data)
  });
  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || "Falha ao atualizar senha");
  }
  return res.json();
}

export async function getTables() {
  const res = await fetchClient(`/admin/tables`);
  return res.json();
}

export async function createTable(tableNumber: number) {
  const res = await fetchClient(`/admin/tables`, {
    method: "POST",
    body: JSON.stringify({ table_number: tableNumber })
  });
  return res.json();
}

export async function createTablesBulk(start: number, end: number) {
  const res = await fetchClient(`/admin/tables/bulk`, {
    method: "POST",
    body: JSON.stringify({ start, end })
  });
  return res.json();
}

export async function deleteTable(tableId: number) {
  const res = await fetchClient(`/admin/tables/${tableId}`, { method: "DELETE" });
  return res.ok;
}

export async function getTablesDashboard(slug: string) {
  const res = await fetchClient(`/admin/tables/dashboard`);
  return res.json();
}

export async function openTable(tableId: number, customerName: string) {
  const res = await fetchClient(`/admin/tables/${tableId}/open`, {
    method: "POST",
    body: JSON.stringify({ customer_name: customerName })
  });
  return res.json();
}

export async function closeTable(tableId: number, paymentMethod: string, customServiceFee?: number) {
  const res = await fetchClient(`/admin/tables/${tableId}/close`, {
    method: "POST",
    body: JSON.stringify({ 
      payment_method: paymentMethod,
      custom_service_fee: customServiceFee 
    })
  });
  return res.json();
}

export async function payTableSession(tableId: number, amount: number, method: string) {
  const res = await fetchClient(`/admin/tables/${tableId}/pay`, {
    method: "POST",
    body: JSON.stringify({ amount, payment_method: method })
  });
  return res.json();
}

export async function updateTablePositions(positions: { id: number, x: number, y: number }[]) {
  const res = await fetchClient(`/admin/tables/positions`, {
    method: "PATCH",
    body: JSON.stringify(positions)
  });
  return res.json();
}

export async function getIngredients() {
  const res = await fetchClient(`/admin/inventory/ingredients`);
  return res.json();
}

export async function createIngredient(data: Partial<Ingredient>) {
  const res = await fetchClient(`/admin/inventory/ingredients`, {
    method: "POST",
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function updateIngredient(id: number, data: Partial<Ingredient>) {
  const res = await fetchClient(`/admin/inventory/ingredients/${id}`, {
    method: "PATCH",
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function deleteIngredient(id: number) {
  const res = await fetchClient(`/admin/inventory/ingredients/${id}`, { method: "DELETE" });
  return res.ok;
}

export async function updateProductRecipe(productId: number, ingredients: RecipeItem[]) {
  const res = await fetchClient(`/admin/inventory/recipes`, {
    method: "POST",
    body: JSON.stringify({ product_id: productId, ingredients })
  });
  return res.json();
}

export async function updateSessionName(sessionId: number, name: string) {
  const res = await fetchClient(`/admin/tables/sessions/${sessionId}`, {
    method: "PATCH",
    body: JSON.stringify({ customer_name: name })
  });
  return res.json();
}

export async function getSessionDetails(sessionId: number) {
  const res = await fetchClient(`/admin/tables/sessions/${sessionId}/details`);
  return res.json();
}

export async function transferTable(data: { from_table_id: number, to_table_id: number, merge: boolean }) {
  const res = await fetchClient(`/admin/tables/transfer`, {
    method: "POST",
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function getDrivers() {
  const res = await fetchClient(`/admin/employees?role=driver`);
  return res.json();
}

export async function dispatchOrder(orderId: string, driverId?: number) {
  const res = await fetchClient(`/admin/delivery/orders/${orderId}/dispatch`, {
    method: "PATCH",
    body: JSON.stringify({ driver_id: driverId })
  });
  return res.json();
}

export async function getFranchiseDashboard() {
  const res = await fetchClient(`/admin/franchise/dashboard`);
  return res.json();
}

export async function getPaymentAuthUrl(provider: string) {
  const res = await fetchClient(`/admin/payment/auth-url/${provider}`);
  return res.json();
}

export async function connectPaymentProvider(provider: string, code: string) {
  const res = await fetchClient(`/admin/payment/callback/${provider}?code=${code}`, {
    method: "POST"
  });
  return res.json();
}

export async function disconnectPaymentProvider() {
  const res = await fetchClient(`/admin/payment/disconnect`, {
    method: "DELETE"
  });
  return res.json();
}

export async function emitFiscalDocument(orderId: string) {
  const res = await fetchClient(`/admin/fiscal/orders/${orderId}/emit`, {
    method: "POST"
  });
  return res.json();
}

export async function generateRecommendations() {
  const res = await fetchClient(`/admin/marketing/recommendations/generate`, {
    method: "POST"
  });
  return res.json();
}

export async function getAuditLogs(limit = 50) {
  const res = await fetchClient(`/admin/audit?limit=${limit}`);
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

export async function getPromotions() {
  const res = await fetchClient(`/admin/marketing/promotions`);
  return res.json();
}

export async function createPromotion(data: any) {
  const res = await fetchClient(`/admin/marketing/promotions`, {
    method: "POST",
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function updatePromotion(id: string, data: any) {
  const res = await fetchClient(`/admin/marketing/promotions/${id}`, {
    method: "PATCH",
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function deletePromotion(id: string) {
  const res = await fetchClient(`/admin/marketing/promotions/${id}`, { method: "DELETE" });
  return res.ok;
}

export async function validateCoupon(slug: string, code: string, totalAmount: number): Promise<CouponValidationResponse> {
  const res = await fetch(`${API_BASE_URL}/${slug}/cart/validate-coupon`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code, total_amount: totalAmount })
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Cupom inválido");
  }
  return res.json();
}

export async function getWebhooks() {
  const res = await fetchClient(`/admin/integrations/webhooks`);
  return res.json();
}

export async function createWebhook(data: any) {
  const res = await fetchClient(`/admin/integrations/webhooks`, {
    method: "POST",
    body: JSON.stringify(data)
  });
  return res.json();
}

export async function deleteWebhook(id: number) {
  const res = await fetchClient(`/admin/integrations/webhooks/${id}`, {
    method: "DELETE"
  });
  return res.ok;
}

export async function getWhatsappStatus() {
  const res = await fetchClient(`/admin/marketing/whatsapp/status`);
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

export async function getSalesForecast(days: number = 7) {
  const res = await fetchClient(`/admin/ai/forecast?days=${days}`);
  return res.json();
}

export async function importIfoodMenu(url: string) {
  const res = await fetchClient(`/admin/menu/import/ifood`, {
    method: "POST",
    body: JSON.stringify({ url })
  });
  return res.json();
}

// --- FINANCIAL AUDIT (NEW EXPORTS) ---
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

export async function getServiceRequestsAdmin(slug: string) {
  const res = await fetchClient(`/admin/${slug}/service-requests`);
  return res.json();
}
