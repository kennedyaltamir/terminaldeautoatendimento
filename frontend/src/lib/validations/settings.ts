/**
 * Author: MESAFLOW_AI
 * Version: 15.0.0 (Platinum Master - Hardware & QR Integrated)
 * DNA_ID: settings-schema-v15-master
 * Objective: Unified Zod schema for Company settings, including Stone POS and QR customization.
 * LAST_MODIFIED: 2026-01-28 15:55:00
 */
import { z } from "zod";

// --- HELPERS DE VALIDAÇÃO ---
const hexColorRegex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/;

const emptyToOptional = (schema: z.ZodString) => 
  z.preprocess((val) => (val === "" ? undefined : val), schema.optional().nullable());

// --- SCHEMA PRINCIPAL ---
export const settingsSchema = z.object({
  // 1. Identidade e Domínio
  name: z.string().min(3, "O nome deve ter pelo menos 3 caracteres"),
  custom_domain: emptyToOptional(z.string()),
  logo_url: emptyToOptional(z.string()),
  banner_url: emptyToOptional(z.string()),
  
  // 2. Identidade Visual (Branding)
  primary_color: z.string().regex(hexColorRegex, "Cor inválida (Use Hex, ex: #ea580c)"),
  background_color: emptyToOptional(z.string().regex(hexColorRegex, "Cor inválida")),
  text_color: emptyToOptional(z.string().regex(hexColorRegex, "Cor inválida")),
  accent_color: emptyToOptional(z.string().regex(hexColorRegex, "Cor inválida")),
  
  // 3. Operacional e Horários
  opens_at: emptyToOptional(z.string()),
  closes_at: emptyToOptional(z.string()),
  
  // 4. Integração de Hardware (Sovereign Stone POS)
  stone_merchant_id: emptyToOptional(z.string()),
  stone_terminal_id: emptyToOptional(z.string()), // Número de Série (S/N) da máquina
  
  // 5. Comunicação e Social
  instagram_url: emptyToOptional(z.string()),
  whatsapp_number: emptyToOptional(z.string().regex(/^\d*$/, "Apenas números")),
  whatsapp_api_url: z.preprocess(
    (val) => (val === "" ? undefined : val),
    z.string().url("URL da API inválida").optional().nullable()
  ),
  whatsapp_instance: emptyToOptional(z.string()),
  whatsapp_token: emptyToOptional(z.string()),
  
  // 6. Conectividade Local
  wifi_ssid: emptyToOptional(z.string()),
  wifi_password: emptyToOptional(z.string()),
  
  // 7. Fintech e Pagamentos
  pix_key: emptyToOptional(z.string()),
  mp_access_token: emptyToOptional(z.string()),
  service_fee_percentage: z.coerce.number().min(0).max(100).default(10),
  loyalty_percentage: z.coerce.number().min(0).max(100).default(0),
  fixed_delivery_fee: z.coerce.number().min(0).default(0),
  
  // 8. Dados Fiscais (Compliance)
  cnpj: z.preprocess(
    (val) => (typeof val === 'string' ? val.replace(/\D/g, '') : val),
    emptyToOptional(z.string().length(14, "CNPJ deve ter 14 dígitos"))
  ),
  inscricao_estadual: emptyToOptional(z.string()),
  fiscal_token: emptyToOptional(z.string()),
  csc_token: emptyToOptional(z.string()),
  csc_id: emptyToOptional(z.string()),
  
  // 9. Segurança de Terminal (Kiosk/Totem)
  kiosk_password: emptyToOptional(z.string().min(4, "Mínimo 4 dígitos")),
  
  // 10. Configuração de Impressão de QR Code (v13.0 Integration)
  qr_config: z.object({
    show_wifi: z.boolean().default(true),
    show_instagram: z.boolean().default(true),
    show_steps: z.boolean().default(true),
    show_logo: z.boolean().default(true),
    dark_mode: z.boolean().default(false),
    custom_color: z.string().optional().nullable(),
  }).optional(),
});

// --- EXPORTAÇÃO DE TIPOS ---
export type SettingsSchema = z.infer<typeof settingsSchema>;