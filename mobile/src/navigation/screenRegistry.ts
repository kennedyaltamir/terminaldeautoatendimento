
/**
 * SCREEN REGISTRY — GOVERNANÇA VISUAL (L5)
 * Fonte única da verdade para todas as telas do aplicativo.
 * Se uma tela não está aqui, ela não existe oficialmente para a auditoria.
 */
export const SCREEN_REGISTRY = [
  "LoginScreen",
  "KitchenDashboard",
  "DriverDashboard",
  "WaiterDashboard",
  "OrdersScreen",
  "WaiterTablesScreen",
  "OrderEntryScreen",
  "OrderReviewScreen",
  "PaymentScreen",
  "PrinterDebugScreen",
  "WaiterCallsScreen"
] as const;

export type ScreenName = typeof SCREEN_REGISTRY[number];

