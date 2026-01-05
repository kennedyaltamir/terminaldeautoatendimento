import { z } from "zod";

const hexColorRegex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/;

export const settingsSchema = z.object({
  name: z.string().min(3, "Nome muito curto"),
  logo_url: z.string().optional().nullable().or(z.literal("")),
  banner_url: z.string().optional().nullable().or(z.literal("")),

  primary_color: z.string().regex(hexColorRegex, "Cor inválida (Use Hex)"),
  background_color: z.string().regex(hexColorRegex, "Cor inválida").optional().nullable().or(z.literal("")),
  text_color: z.string().regex(hexColorRegex, "Cor inválida").optional().nullable().or(z.literal("")),
  accent_color: z.string().regex(hexColorRegex, "Cor inválida").optional().nullable().or(z.literal("")),

  opens_at: z.string().optional().nullable().or(z.literal("")),
  closes_at: z.string().optional().nullable().or(z.literal("")),

  instagram_url: z.string().optional().nullable().or(z.literal("")),
  whatsapp_number: z.string().regex(/^\d*$/, "Apenas números").optional().nullable().or(z.literal("")),

  whatsapp_api_url: z.string().url("URL inválida").optional().nullable().or(z.literal("")),
  whatsapp_instance: z.string().optional().nullable().or(z.literal("")),
  whatsapp_token: z.string().optional().nullable().or(z.literal("")),

  wifi_ssid: z.string().optional().nullable().or(z.literal("")),
  wifi_password: z.string().optional().nullable().or(z.literal("")),

  pix_key: z.string().optional().nullable().or(z.literal("")),
  mp_access_token: z.string().optional().nullable().or(z.literal("")),

  // --- CAMPOS FISCAIS ---
  cnpj: z.string().regex(/^\d{14}$/, "CNPJ deve ter 14 dígitos").optional().nullable().or(z.literal("")),
  inscricao_estadual: z.string().optional().nullable().or(z.literal("")),
  fiscal_token: z.string().optional().nullable().or(z.literal("")),
  csc_token: z.string().optional().nullable().or(z.literal("")),
  csc_id: z.string().optional().nullable().or(z.literal("")),

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
