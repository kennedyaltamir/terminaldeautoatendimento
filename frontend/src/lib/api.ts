import { getToken, getRefreshToken, setTokens, removeTokens } from "./auth";
import { Company, Ingredient, RecipeItem } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

async function fetchClient(endpoint: string, options: RequestInit = {}) {
  const token = getToken();
  const headers: any = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  let response = await fetch(`${API_BASE_URL}${endpoint}`, { ...options, headers });

  if (response.status === 401) {
    const refreshToken = getRefreshToken();
    if (!refreshToken) {
      removeTokens();
      if (typeof window !== "undefined" && !window.location.pathname.includes("/login")) {
        window.location.href = "/admin/login";
      }
      throw new Error("Sessão expirada");
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
      throw new Error("Sessão expirada");
    }
  }

  return response;
}

// ... (Funções existentes mantidas: getMenu, getWallet, etc.) ...
export async function getMenu(slug: string) {
  const res = await fetch(`${API_BASE_URL}/${slug}/menu`, { cache: "no-store" });
  if (!res.ok) throw new Error("Falha ao carregar cardápio");
  return res.json();
}

export async function getWallet(slug: string, phone: string) {
  const res = await fetch(`${API_BASE_URL}/${slug}/wallet/${phone}`);
  if (!res.ok) return { balance: 0, loyalty_percentage: 0 };
  return res.json();
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

export async function getServiceRequests(slug: string) {
  const res = await fetchClient(`/admin/${slug}/service-requests`);
  if (!res.ok) throw new Error("Falha ao carregar chamados");
  return res.json();
}

export async function resolveServiceRequest(requestId: number) {
  const res = await fetchClient(`/admin/service-requests/${requestId}/resolve`, { method: "PATCH" });
  return res.ok;
}

export async function login(username: string, password: string) {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);
  const res = await fetch(`${API_BASE_URL}/auth/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: formData,
  });
  if (!res.ok) throw new Error("Login falhou.");
  const data = await res.json();
  setTokens(data.access_token, data.refresh_token);
  return data;
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
  if (!res.ok) throw new Error("Falha ao carregar métricas");
  return res.json();
}

export async function getKitchenOrders(slug: string) {
  const res = await fetchClient(`/admin/${slug}/orders`);
  if (!res.ok) throw new Error("Falha ao carregar pedidos");
  return res.json();
}

export async function getRecentCompletedOrders(slug: string) {
  const res = await fetchClient(`/admin/${slug}/orders/recent-completed`);
  if (!res.ok) throw new Error("Falha ao carregar histórico recente");
  return res.json();
}

export async function getQuickProducts(slug: string) {
  const res = await fetchClient(`/admin/${slug}/products/quick-list`);
  if (!res.ok) throw new Error("Falha ao carregar produtos");
  return res.json();
}

export async function getOrderHistory(slug: string, page = 1, limit = 10) {
  const res = await fetchClient(`/admin/${slug}/history?page=${page}&limit=${limit}`);
  if (!res.ok) throw new Error("Falha ao carregar histórico");
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
  if (!res.ok) throw new Error("Erro ao criar mesas em lote");
  return res.json();
}

export async function deleteTable(tableId: number) {
  const res = await fetchClient(`/admin/tables/${tableId}`, { method: "DELETE" });
  return res.ok;
}

export async function getTablesDashboard(slug: string) {
  const res = await fetchClient(`/admin/tables/dashboard`);
  if (!res.ok) throw new Error("Erro ao carregar dashboard de mesas");
  return res.json();
}

export async function openTable(tableId: number, customerName: string) {
  const res = await fetchClient(`/admin/tables/${tableId}/open`, {
    method: "POST",
    body: JSON.stringify({ customer_name: customerName })
  });
  if (!res.ok) throw new Error("Erro ao abrir mesa");
  return res.json();
}

export async function closeTable(tableId: number, paymentMethod: string) {
  const res = await fetchClient(`/admin/tables/${tableId}/close`, {
    method: "POST",
    body: JSON.stringify({ payment_method: paymentMethod })
  });
  if (!res.ok) throw new Error("Erro ao fechar mesa");
  return res.json();
}

export async function updateTablePositions(positions: { id: number, x: number, y: number }[]) {
  const res = await fetchClient(`/admin/tables/positions`, {
    method: "PATCH",
    body: JSON.stringify(positions)
  });
  if (!res.ok) throw new Error("Erro ao salvar layout");
  return res.json();
}

export async function getIngredients() {
  const res = await fetchClient(`/admin/inventory/ingredients`);
  if (!res.ok) throw new Error("Erro ao carregar ingredientes");
  return res.json();
}

export async function createIngredient(data: Partial<Ingredient>) {
  const res = await fetchClient(`/admin/inventory/ingredients`, {
    method: "POST",
    body: JSON.stringify(data)
  });
  if (!res.ok) throw new Error("Erro ao criar ingrediente");
  return res.json();
}

export async function updateIngredient(id: number, data: Partial<Ingredient>) {
  const res = await fetchClient(`/admin/inventory/ingredients/${id}`, {
    method: "PATCH",
    body: JSON.stringify(data)
  });
  if (!res.ok) throw new Error("Erro ao atualizar ingrediente");
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
  if (!res.ok) throw new Error("Erro ao salvar ficha técnica");
  return res.json();
}

export async function updateSessionName(sessionId: number, name: string) {
  const res = await fetchClient(`/admin/tables/sessions/${sessionId}`, {
    method: "PATCH",
    body: JSON.stringify({ customer_name: name })
  });
  if (!res.ok) throw new Error("Erro ao renomear mesa");
  return res.json();
}

export async function getSessionDetails(sessionId: number) {
  const res = await fetchClient(`/admin/tables/sessions/${sessionId}/details`);
  if (!res.ok) throw new Error("Erro ao carregar detalhes da sessão");
  return res.json();
}

export async function transferTable(data: { from_table_id: number, to_table_id: number, merge: boolean }) {
  const res = await fetchClient(`/admin/tables/transfer`, {
    method: "POST",
    body: JSON.stringify(data)
  });
  
  if (!res.ok) {
    const err = await res.json();
    throw err;
  }
  return res.json();
}

export async function getDrivers() {
  const res = await fetchClient(`/admin/employees?role=driver`);
  if (!res.ok) throw new Error("Erro ao carregar entregadores");
  return res.json();
}

export async function dispatchOrder(orderId: string, driverId?: number) {
  const res = await fetchClient(`/admin/delivery/orders/${orderId}/dispatch`, {
    method: "PATCH",
    body: JSON.stringify({ driver_id: driverId })
  });
  if (!res.ok) throw new Error("Erro ao despachar pedido");
  return res.json();
}

export async function getFranchiseDashboard() {
  const res = await fetchClient(`/admin/franchise/dashboard`);
  if (!res.ok) throw new Error("Erro ao carregar dashboard de franquia");
  return res.json();
}

// --- NOVAS FUNÇÕES DE PAGAMENTO (OAUTH) ---

export async function getPaymentAuthUrl(provider: string) {
  const res = await fetchClient(`/admin/payment/auth-url/${provider}`);
  if (!res.ok) throw new Error("Erro ao obter URL de autenticação");
  return res.json();
}

export async function connectPaymentProvider(provider: string, code: string) {
  const res = await fetchClient(`/admin/payment/callback/${provider}?code=${code}`, {
    method: "POST"
  });
  if (!res.ok) throw new Error("Erro ao conectar provedor");
  return res.json();
}

export async function disconnectPaymentProvider() {
  const res = await fetchClient(`/admin/payment/disconnect`, {
    method: "DELETE"
  });
  if (!res.ok) throw new Error("Erro ao desconectar");
  return res.json();
}