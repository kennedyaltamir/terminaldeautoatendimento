import { z } from "zod";

// Regex para WhatsApp BR (com ou sem 9º dígito, com DDD)
// Aceita: 11999999999, 1199999999
const phoneRegex = /^\d{10,11}$/;

export const kioskCheckoutSchema = z.object({
  customerName: z.string()
    .min(3, "Nome deve ter no mínimo 3 letras")
    .transform(val => val.trim()),
    
  customerPhone: z.string()
    .regex(phoneRegex, "Digite um número válido com DDD (apenas números)")
    .transform(val => {
      // Normalização para formato internacional (55 + numero)
      const clean = val.replace(/\D/g, "");
      return clean.startsWith("55") ? clean : `55${clean}`;
    }),

  pickupNote: z.string()
    .min(1, "Identifique sua localização (Mesa, Balcão ou Senha)")
    .max(50, "Máximo 50 caracteres")
    .transform(val => val.trim()),

  paymentMethod: z.enum(["pix", "card", "cash"], {
    errorMap: () => ({ message: "Selecione uma forma de pagamento" })
  })
});

export type KioskCheckoutFormData = z.infer<typeof kioskCheckoutSchema>;
