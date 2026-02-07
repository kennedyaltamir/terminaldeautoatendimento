/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 3.9.0 (Auth Contract Fixed)
 * DNA_ID: MF-API-LIB-V3-9-GOLD
 * Objective: Client de comunicação resiliente com correção de contrato OAuth2 (Form Data).
 */
import { getToken, getRefreshToken, setTokens, removeTokens } from "./auth";
import { 
  Order, MenuResponse, TableDashboard, TableSession, Product,
  Employee, Ingredient, RecipeItem, Promotion, CouponValidationResponse,
  AuditLog, Company, ServiceRequest, WebhookResponse, Metrics, Category
} from "@/types";

// --- 🛡️ INFRASTRUCTURE RESOLVER ---
const getBaseUrl = (): string => {
  if (process.env.NEXT_PUBLIC_API_URL) return process.env.NEXT_PUBLIC_API_URL;
  if (typeof window !== 'undefined') {
    const host = window.location.hostname;
    // Fallback inteligente para desenvolvimento local via Sentinel
    if (host === 'localhost' || host === '127.0.0.1') return "http://localhost:8001/api"; 
    return `http://${host}:8001/api`;
  }
  return "http://127.0.0.1:8001/api";
};

const API_BASE_URL = getBaseUrl();

/**
 * Classe de erro customizada para facilitar o catch semântico na UI.
 */
export class ApiError extends Error {
  status: number;
  code?: string;
  constructor(message: string, status: number, code?: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
  }
}

// --- 🛠️ CORE REQUEST ENGINE ---
/**
 * Executor central de requisições com interceptação de segurança.
 */
async function fetchClient<T = any>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  
  // Default headers (JSON), mas permite override (ex: para multipart ou form-data)
  const defaultHeaders: Record<string, string> = {
    "Content-Type": "application/json",
  };

  // Se o body for FormData ou URLSearchParams, o browser/fetch define o Content-Type automaticamente
  // ou devemos defini-lo explicitamente se passado nas options.
  if (options.body instanceof FormData || options.body instanceof URLSearchParams) {
      delete defaultHeaders["Content-Type"];
  }

  const headers: Record<string, string> = {
    ...defaultHeaders,
    ...(options.headers as Record<string, string>),
  };

  if (token) headers["Authorization"] = `Bearer ${token}`;

  const executeFetch = async () => {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 15000); // 15s timeout
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, { 
        ...options, 
        headers,
        signal: controller.signal 
      });
      clearTimeout(timeoutId);
      return response;
    } catch (error: any) {
      clearTimeout(timeoutId);
      if (error.name === 'AbortError') throw new ApiError("A requisição excedeu o tempo limite", 408);
      if (error.message === "Failed to fetch") throw new ApiError("Servidor Indisponível (Erro de Conexão)", 503);
      throw error;
    }
  };

  let response = await executeFetch();

  // 🔄 AUTO-REFRESH PROTOCOL: Tratamento de Token Expirado (401)
  if (response.status === 401) {
    const refreshToken = getRefreshToken();
    if (refreshToken) {
      try {
        const refreshRes = await fetch(`${API_BASE_URL}/auth/refresh`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ refresh_token: refreshToken })
        });

        if (refreshRes.ok) {
          const data = await refreshRes.json();
          setTokens(data.access_token, data.refresh_token);
          headers["Authorization"] = `Bearer ${data.access_token}`;
          response = await executeFetch(); // Tenta a requisição original novamente
        } else {
          removeTokens();
          throw new ApiError("Sessão Expirada", 401);
        }
      } catch (e) {
        removeTokens();
        throw new ApiError("Falha na renovação de sessão", 401);
      }
    }
  }

  // 🛡️ EXCEPTION HANDLING: Tratamento de Erros HTTP
  if (!response.ok) {
    let errorData: any = {};
    try {
        errorData = await response.json();
    } catch (e) {
        // Fallback para quando o servidor retorna erro 500 em texto puro
        errorData = { detail: response.statusText || "Erro interno do servidor" };
    }
    
    // Tratamento específico para Circuit Breaker (Disjuntor Aberto)
    if (response.status === 503) {
        const msg = errorData.detail || "O sistema está temporariamente em modo de proteção. Tente em 30s.";
        throw new ApiError(msg, 503, "CIRCUIT_BREAKER");
    }

    throw new ApiError(errorData.detail || "Erro desconhecido na API", response.status);
  }

  // Retorno Seguro: Evita erro de parse em respostas vazias (204 No Content)
  return response.status === 204 ? ({} as T) : response.json();
}

// =============================================================================
// 🔐 DOMAIN: AUTHENTICATION & IDENTITY
// =============================================================================

export const login = async (credentials: { email: string; password: string }) => {
  // 🛡️ CONTRATO OAUTH2: Transformando JSON em Form-Data URL Encoded exigido pelo FastAPI
  const formData = new URLSearchParams();
  formData.append("username", credentials.email);
  formData.append("password", credentials.password);

  const res = await fetch(`${API_BASE_URL}/auth/token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept": "application/json"
    },
    body: formData.toString(),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: "Credenciais inválidas" }));
    throw new ApiError(errorData.detail || "Falha na autenticação", res.status);
  }

  return res.json();
};

export const register = (data: any) => fetchClient("/auth/register", { method: "POST", body: JSON.stringify(data) });
export const updatePassword = (data: any) => fetchClient(`/admin/company/me/password`, { method: "PATCH", body: JSON.stringify(data) });
export const getCompanySettings = (): Promise<Company> => fetchClient(`/admin/company/me`);
export const updateCompanySettings = (data: any) => fetchClient(`/admin/company/me`, { method: "PATCH", body: JSON.stringify(data) });
export const validateKioskPassword = (slug: string, password: string) => fetchClient(`/admin/company/kiosk/validate`, { method: "POST", body: JSON.stringify({ password }) });

// =============================================================================
// 🚚 DOMAIN: LOGISTICS & DRIVER MOBILE
// =============================================================================

export const startDriverShift = (data: any) => fetchClient("/mobile/logistics/shift/start", { method: "POST", body: JSON.stringify(data) });
export const endDriverShift = (data: any) => fetchClient("/mobile/logistics/shift/end", { method: "POST", body: JSON.stringify(data) });
export const acceptJourney = (orderId: string) => fetchClient(`/mobile/logistics/journey/${orderId}/accept`, { method: "POST" });
export const updateJourneyStatus = (journeyId: string, status: string, podCode?: string) => fetchClient(`/mobile/logistics/journey/${journeyId}/status`, { method: "PATCH", body: JSON.stringify({ status, pod_code: podCode }) });
export const updateActiveVehicle = (data: any) => fetchClient("/mobile/logistics/vehicle/active", { method: "PATCH", body: JSON.stringify(data) });
export const ingestTelemetry = (data: any) => fetchClient("/mobile/logistics/telemetry", { method: "POST", body: JSON.stringify(data) });

// =============================================================================
// 🏢 DOMAIN: ADMINISTRATIVE OPERATIONS (KDS, BI, AUDIT)
// =============================================================================

export const getKitchenOrders = (slug: string): Promise<Order[]> => fetchClient(`/admin/${slug}/orders`);
export const getRecentCompletedOrders = (slug: string): Promise<Order[]> => fetchClient(`/admin/${slug}/orders?status=ready&limit=20`);
export const getOrderHistory = (slug: string, page: number = 1, limit: number = 10) => fetchClient(`/admin/history?slug=${slug}&page=${page}&limit=${limit}`);
export const getDashboardMetrics = (start?: string, end?: string): Promise<Metrics> => fetchClient(`/admin/metrics?start_date=${start}&end_date=${end}`);
export const getFranchiseDashboard = () => fetchClient(`/admin/franchise/dashboard`);
export const getSalesForecast = (days: number = 7) => fetchClient(`/admin/ai/forecast?days=${days}`);
export const getAuditLogs = (limit: number = 50): Promise<AuditLog[]> => fetchClient(`/admin/audit?limit=${limit}`);
export const updateOrderStatus = (slug: string, orderId: string, status: string) => fetchClient(`/admin/orders/${orderId}`, { method: "PATCH", body: JSON.stringify({ status }) });

// =============================================================================
// 🪑 DOMAIN: TABLES & WAITER MANAGEMENT
// =============================================================================

export const getTablesDashboard = (): Promise<TableDashboard[]> => fetchClient(`/admin/tables/dashboard`);
export const createTable = (data: any) => fetchClient(`/admin/tables`, { method: "POST", body: JSON.stringify(data) });
export const updateTablePositions = (positions: any[]) => fetchClient(`/admin/tables/positions`, { method: "PATCH", body: JSON.stringify(positions) });
export const deleteTable = (id: number) => fetchClient(`/admin/tables/${id}`, { method: "DELETE" });
export const createBulkTables = (data: any) => fetchClient(`/admin/tables/bulk`, { method: "POST", body: JSON.stringify(data) });
export const openTable = (id: number, customerName: string) => fetchClient(`/admin/tables/${id}/open`, { method: "POST", body: JSON.stringify({ customer_name: customerName }) });
export const closeTable = (id: number, method: string, tip: number = 0) => fetchClient(`/admin/tables/${id}/close`, { method: "POST", body: JSON.stringify({ payment_method: method, custom_service_fee: tip }) });
export const payTableSession = (id: number, amount: number, method: string) => fetchClient(`/admin/tables/${id}/pay`, { method: "POST", body: JSON.stringify({ amount, payment_method: method }) });
export const transferTable = (data: any) => fetchClient(`/admin/tables/transfer`, { method: "POST", body: JSON.stringify(data) });
export const getTableActiveSession = (tableId: number): Promise<TableSession> => fetchClient(`/admin/tables/${tableId}/active-session`);

// =============================================================================
// 🍔 DOMAIN: PUBLIC CUSTOMER FACING
// =============================================================================

export const getMenu = (slug: string): Promise<MenuResponse> => fetchClient(`/public/${slug}/menu`);
export const getPublicOrder = (orderId: string): Promise<Order> => fetchClient(`/public/orders/${orderId}`);
export const createOrder = (slug: string, data: any): Promise<Order> => fetchClient(`/public/${slug}/orders`, { method: "POST", body: JSON.stringify(data) });
export const checkTableStatus = (slug: string, tableId: number, qrToken?: string, sessionToken?: string | null) => fetchClient(`/public/${slug}/check-table`, { method: "POST", body: JSON.stringify({ table_id: tableId, qr_token: qrToken, session_token: sessionToken }) });
export const joinTable = (slug: string, data: any) => fetchClient(`/public/${slug}/join-table`, { method: "POST", body: JSON.stringify(data) });
export const getPublicMonitorOrders = (slug: string) => fetchClient(`/public/${slug}/monitor`);
export const getSessionDetails = (sessionId: string | number): Promise<TableSession> => fetchClient(`/public/session/${sessionId}`);
export const getTableSession = (sessionId: string | number): Promise<TableSession> => fetchClient(`/public/session/${sessionId}`);
export const sendOrderFeedback = (slug: string, orderId: string, score: number, comment: string) => fetchClient(`/public/${slug}/orders/${orderId}/feedback`, { method: "POST", body: JSON.stringify({ score, comment }) });
export const requestService = (slug: string, data: any) => fetchClient(`/public/${slug}/service-request`, { method: "POST", body: JSON.stringify(data) });
export const getWallet = (slug: string, phone: string) => fetchClient(`/public/${slug}/wallet/${phone}`);
export const validateCoupon = (slug: string, code: string, total: number): Promise<CouponValidationResponse> => fetchClient(`/public/${slug}/coupon/validate`, { method: "POST", body: JSON.stringify({ code, total_amount: total }) });

// =============================================================================
// 📦 DOMAIN: INVENTORY & PRODUCT MGMT
// =============================================================================

export const getIngredients = (): Promise<Ingredient[]> => fetchClient(`/admin/inventory/ingredients`);
export const createIngredient = (data: any) => fetchClient(`/admin/inventory/ingredients`, { method: "POST", body: JSON.stringify(data) });
export const updateIngredient = (id: number, data: any) => fetchClient(`/admin/inventory/ingredients/${id}`, { method: "PATCH", body: JSON.stringify(data) });
export const deleteIngredient = (id: number) => fetchClient(`/admin/inventory/ingredients/${id}`, { method: "DELETE" });

export const getQuickProducts = (): Promise<Product[]> => fetchClient(`/admin/menu/products`);
export const createProduct = (data: any): Promise<Product> => fetchClient(`/admin/menu/products`, { method: "POST", body: JSON.stringify(data) });
export const updateProduct = (id: number, data: any): Promise<Product> => fetchClient(`/admin/menu/products/${id}`, { method: "PATCH", body: JSON.stringify(data) });
export const deleteProduct = (id: number) => fetchClient(`/admin/menu/products/${id}`, { method: "DELETE" });
export const updateProductRecipe = (data: any) => fetchClient(`/admin/menu/recipes`, { method: "PATCH", body: JSON.stringify(data) });

export const createCategory = (data: any): Promise<Category> => fetchClient(`/admin/menu/categories`, { method: "POST", body: JSON.stringify(data) });
export const updateCategory = (id: number, data: any): Promise<Category> => fetchClient(`/admin/menu/categories/${id}`, { method: "PATCH", body: JSON.stringify(data) });
export const deleteCategory = (id: number): Promise<void> => fetchClient(`/admin/menu/categories/${id}`, { method: "DELETE" });

// =============================================================================
// 📣 DOMAIN: MARKETING & INTEGRATIONS
// =============================================================================
export const generateRecommendations = () => fetchClient(`/admin/marketing/recommendations/generate`, { method: "POST" });
export const getPromotions = (): Promise<Promotion[]> => fetchClient(`/admin/marketing/promotions`);
export const createPromotion = (data: any): Promise<Promotion> => fetchClient(`/admin/marketing/promotions`, { method: "POST", body: JSON.stringify(data) });
export const updatePromotion = (id: string, data: any): Promise<Promotion> => fetchClient(`/admin/marketing/promotions/${id}`, { method: "PATCH", body: JSON.stringify(data) });
export const deletePromotion = (id: string): Promise<void> => fetchClient(`/admin/marketing/promotions/${id}`, { method: "DELETE" });
export const getWebhooks = (): Promise<WebhookResponse[]> => fetchClient(`/admin/integrations/webhooks`);
export const createWebhook = (data: any): Promise<WebhookResponse> => fetchClient(`/admin/integrations/webhooks`, { method: "POST", body: JSON.stringify(data) });
export const deleteWebhook = (id: number): Promise<void> => fetchClient(`/admin/integrations/webhooks/${id}`, { method: "DELETE" });
export const getFeatureFlags = () => fetchClient("/admin/features");
export const updateFeatureFlag = (key: string, isEnabled: boolean) => fetchClient("/admin/features", { method: "POST", body: JSON.stringify({ key, is_enabled: isEnabled }) });
export const getWhatsappStatus = () => fetchClient(`/admin/integrations/whatsapp/status`);
export const emitFiscalDocument = (orderId: string) => fetchClient(`/admin/fiscal/orders/${orderId}/emit`, { method: "POST" });
export const getPaymentAuthUrl = (provider: string) => fetchClient(`/admin/payment/auth-url/${provider}`);
export const connectPaymentProvider = (provider: string, code: string) => fetchClient(`/admin/payment/callback/${provider}?code=${code}`, { method: "POST" });
export const disconnectPaymentProvider = () => fetchClient(`/admin/payment/disconnect`, { method: "DELETE" });
export const getDrivers = () => fetchClient(`/admin/logistics/drivers`);
export const dispatchOrder = (orderId: string, driverId?: number) => fetchClient(`/admin/delivery/orders/${orderId}/dispatch`, { method: "PATCH", body: JSON.stringify({ driver_id: driverId }) });
export const getDriversWithBalance = () => fetchClient(`/admin/logistics/drivers/balance`);
export const settleDriverDebt = (driverId: number, amount: number, description: string) => fetchClient(`/admin/logistics/drivers/${driverId}/settle`, { method: "POST", body: JSON.stringify({ amount, description }) });
export const getLedgerHistory = () => fetchClient(`/admin/audit/financial/ledger`);
export const getReconciliationReport = () => fetchClient(`/admin/audit/financial/reconciliation`);
export const verifyLedgerIntegrity = () => fetchClient(`/admin/audit/financial/verify-integrity`);
export const fixOrphanTransaction = (externalId: string) => fetchClient(`/admin/audit/financial/fix-orphan`, { method: "POST", body: JSON.stringify({ external_id: externalId }) });