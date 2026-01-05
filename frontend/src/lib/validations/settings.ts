import { z } from "zod";

// Regex para Hex Color (#RRGGBB ou #RGB)
const hexColorRegex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/;

export const settingsSchema = z.object({
  // Geral
  name: z.string().min(3, "Nome muito curto"),
  logo_url: z.string().optional().nullable().or(z.literal("")),
  banner_url: z.string().optional().nullable().or(z.literal("")),
  
  // Cores (Tema)
  primary_color: z.string().regex(hexColorRegex, "Cor inválida (Use Hex)"),
  background_color: z.string().regex(hexColorRegex, "Cor inválida").optional().nullable().or(z.literal("")),
  text_color: z.string().regex(hexColorRegex, "Cor inválida").optional().nullable().or(z.literal("")),
  accent_color: z.string().regex(hexColorRegex, "Cor inválida").optional().nullable().or(z.literal("")),
  
  // Horários (Strings HH:MM)
  opens_at: z.string().optional().nullable().or(z.literal("")),
  closes_at: z.string().optional().nullable().or(z.literal("")),

  // Marketing
  instagram_url: z.string().optional().nullable().or(z.literal("")),
  whatsapp_number: z.string().regex(/^\d*$/, "Apenas números").optional().nullable().or(z.literal("")),
  wifi_ssid: z.string().optional().nullable().or(z.literal("")),
  wifi_password: z.string().optional().nullable().or(z.literal("")),

  // Financeiro
  pix_key: z.string().optional().nullable().or(z.literal("")),
  mp_access_token: z.string().optional().nullable().or(z.literal("")),
  
  // Porcentagens e Taxas (Conversão segura de string para number)
  loyalty_percentage: z.union([z.string(), z.number()])
    .transform((val) => {
      if (val === "" || val === null || val === undefined) return 0;
      const num = Number(val);
      return isNaN(num) ? 0 : num;
    })
    .pipe(z.number().min(0).max(100)),

  fixed_delivery_fee: z.union([z.string(), z.number()])
    .transform((val) => {
      if (val === "" || val === null || val === undefined) return 0;
      const num = Number(val);
      return isNaN(num) ? 0 : num;
    })
    .pipe(z.number().min(0)),
});

export type SettingsSchema = z.infer<typeof settingsSchema>;