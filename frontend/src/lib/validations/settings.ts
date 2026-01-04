import { z } from "zod";

// Regex para Hex Color (#RRGGBB ou #RGB)
const hexColorRegex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/;

export const settingsSchema = z.object({
  // Geral
  name: z.string().min(3, "Nome muito curto"),
  logo_url: z.string().url("URL inválida").or(z.literal("")).optional().nullable(),
  banner_url: z.string().url("URL inválida").or(z.literal("")).optional().nullable(),
  primary_color: z.string().regex(hexColorRegex, "Cor inválida (Use Hex)"),
  
  // Horários (Strings HH:MM)
  opens_at: z.string().optional().nullable(),
  closes_at: z.string().optional().nullable(),

  // Marketing
  instagram_url: z.string().url("URL inválida").or(z.literal("")).optional().nullable(),
  whatsapp_number: z.string().regex(/^\d*$/, "Apenas números").optional().nullable(),
  wifi_ssid: z.string().optional().nullable(),
  wifi_password: z.string().optional().nullable(),

  // Financeiro
  pix_key: z.string().optional().nullable(),
  mp_access_token: z.string().optional().nullable(),
  
  // Porcentagens e Taxas (Conversão segura de string para number)
  loyalty_percentage: z.any()
    .transform((val) => {
      const num = Number(val);
      return isNaN(num) ? 0 : num;
    })
    .pipe(z.number().min(0).max(100)),

  fixed_delivery_fee: z.any()
    .transform((val) => {
      const num = Number(val);
      return isNaN(num) ? 0 : num;
    })
    .pipe(z.number().min(0)),
});

export type SettingsSchema = z.infer<typeof settingsSchema>;