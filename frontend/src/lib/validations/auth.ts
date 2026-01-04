import { z } from "zod";

export const loginSchema = z.object({
  email: z.string().email("Digite um e-mail válido"),
  password: z.string().min(1, "A senha é obrigatória"),
});

export const registerSchema = z.object({
  company_name: z.string().min(3, "Nome do negócio deve ter no mínimo 3 caracteres"),
  company_slug: z
    .string()
    .min(3, "O link deve ter no mínimo 3 caracteres")
    .regex(/^[a-z0-9-]+$/, "Use apenas letras minúsculas, números e hífens"),
  owner_email: z.string().email("Digite um e-mail válido"),
  owner_phone: z.string().optional(),
  owner_role: z.string().optional(),
  
  // Campo essencial para a Verticalização (Hotel, Eventos, etc)
  segment: z.enum(["gastro", "event", "hotel", "corp"]).default("gastro"),
  
  password: z
    .string()
    .min(8, "A senha deve ter no mínimo 8 caracteres")
    .regex(/[A-Za-z]/, "A senha deve conter letras")
    .regex(/[0-9]/, "A senha deve conter números"),
});

export type LoginSchema = z.infer<typeof loginSchema>;
export type RegisterSchema = z.infer<typeof registerSchema>;