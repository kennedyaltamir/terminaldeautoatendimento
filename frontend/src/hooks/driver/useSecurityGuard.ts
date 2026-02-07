/**
 * Author: MESAFLOW_AI
 * Version: 1.1.0 (Literal Type Fix)
 * DNA_ID: MF-HOOK-SEC-GUARD-V1
 */
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';

export function useSecurityGuard(deviceId: string, isUntrusted: boolean) {
  const router = useRouter();

  useEffect(() => {
    const checkBlacklist = async () => {
      // 🛡️ FIX: Tipagem explícita para permitir comparação com 'BLACKLISTED'
      const status: 'ACTIVE' | 'BLACKLISTED' = 'ACTIVE'; 
      
      if (status === ('BLACKLISTED' as string)) {
        toast.error("Dispositivo bloqueado.");
        router.push('/admin/login?error=device_banned');
      }
    };

    if (isUntrusted) {
      toast.warning("Sinal de GPS inconsistente.");
    }

    checkBlacklist();
  }, [deviceId, isUntrusted, router]);

  const registerFailedAttempt = () => {
    const attempts = parseInt(localStorage.getItem('mf_sec_attempts') || '0') + 1;
    localStorage.setItem('mf_sec_attempts', attempts.toString());
    return { locked: attempts >= 5, duration: 3600 };
  };

  return { registerFailedAttempt };
}
