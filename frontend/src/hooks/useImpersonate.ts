import { useState, useCallback, useEffect } from "react";
import { toast } from "sonner";
import { setTokens, setUserRole } from "@/lib/auth";
import { auditLogger } from "@/lib/audit-logger";

interface ImpersonateResponse {
  access_token: string;
  refresh_token: string;
  user_role: string;
  company_slug: string;
}

const ERROR_MESSAGES: Record<number, string> = {
  400: "Dados inválidos. Verifique o formato do e-mail.",
  401: "Chave Mestra incorreta ou expirada.",
  403: "Acesso negado. IP não autorizado ou nível insuficiente.",
  404: "Cliente não encontrado na base de dados.",
  429: "Muitas tentativas. Aguarde 60 segundos.",
  500: "Erro interno do servidor. A equipe de infraestrutura foi notificada.",
};

export function useImpersonate() {
  const [loading, setLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [networkError, setNetworkError] = useState(false);
  const [cooldown, setCooldown] = useState(0);

  // Efeito de Cooldown
  useEffect(() => {
    if (cooldown > 0) {
      const timer = setInterval(() => setCooldown(c => c - 1), 1000);
      return () => clearInterval(timer);
    }
  }, [cooldown]);

  const impersonate = useCallback(async (secret: string, email: string) => {
    if (cooldown > 0) {
      toast.warning(`Aguarde ${cooldown}s para tentar novamente.`);
      throw new Error("Cooldown ativo");
    }

    setLoading(true);
    setNetworkError(false);
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 15000);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/impersonate`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "X-Super-Secret": secret 
        },
        body: JSON.stringify({ target_email: email }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        const msg = errData.detail || ERROR_MESSAGES[res.status] || "Acesso negado.";
        
        // Se for erro 429 ou 401/403 repetido, ativa cooldown
        if (res.status === 429 || res.status === 401) {
          setCooldown(10); // 10 segundos de penalidade
        }
        
        throw new Error(msg);
      }

      const data: ImpersonateResponse = await res.json();
      
      setTokens(data.access_token, data.refresh_token);
      setUserRole(data.user_role);
      
      auditLogger.logAttempt(email, true);
      setIsSuccess(true);
      
      return data.company_slug;

    } catch (e: any) {
      const isNetwork = e.name === 'AbortError' || e.message.includes('fetch');
      const msg = isNetwork ? "Erro de conexão. Verifique sua rede." : e.message;
      
      // Não loga se for apenas cooldown local
      if (msg !== "Cooldown ativo") {
        auditLogger.logAttempt(email, false, msg);
      }
      
      if (isNetwork) {
        setNetworkError(true);
        toast.error("Falha de Rede", { description: "Não foi possível contatar o servidor." });
      } else if (msg !== "Cooldown ativo") {
        toast.error("Acesso Negado", { description: msg });
      }
      
      setIsSuccess(false);
      throw e; 
    } finally {
      setLoading(false);
    }
  }, [cooldown]);

  return { impersonate, loading, isSuccess, setIsSuccess, networkError, cooldown };
}
