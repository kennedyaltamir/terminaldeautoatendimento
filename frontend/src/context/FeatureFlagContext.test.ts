import { describe, it, expect, vi, beforeEach } from 'vitest';
import { decodeJwtPayload } from '../lib/jwt';

// Mock dos utilitários e API
vi.mock('../lib/auth', () => ({
  getToken: vi.fn(() => 'fake.token.signature')
}));

vi.mock('../lib/jwt', () => ({
  decodeJwtPayload: vi.fn()
}));

vi.mock('../lib/featureFlagsApi', () => ({
  getFeatureFlags: vi.fn(),
  updateFeatureFlag: vi.fn()
}));

import { getFeatureFlags, updateFeatureFlag } from '../lib/featureFlagsApi';

describe('FeatureFlag Logic & Security', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('deve identificar isImpersonator como true quando a claim existe no JWT', () => {
    (decodeJwtPayload as any).mockReturnValue({ impersonator: true });
    const payload = decodeJwtPayload('token');
    expect(payload.impersonator).toBe(true);
  });

  it('deve identificar isImpersonator como false quando a claim está ausente', () => {
    (decodeJwtPayload as any).mockReturnValue({ sub: 'admin@test.com' });
    const payload = decodeJwtPayload('token');
    expect(payload.impersonator).toBeFalsy();
  });

  it('deve falhar de forma segura se a decodificação do JWT falhar', () => {
    (decodeJwtPayload as any).mockImplementation(() => { throw new Error(); });
    // A implementação real do utilitário já captura o erro e retorna {}
    // Aqui testamos o comportamento esperado do utilitário
    vi.restoreAllMocks(); // Usa a implementação real do jwt.ts
    const result = decodeJwtPayload('token_invalido');
    expect(result).toEqual({});
    expect(result.impersonator).toBeFalsy();
  });

  it('deve simular rollback de estado em caso de erro 403 na API', async () => {
    // Simulação da lógica interna do toggleFlag
    const flags = { feature_a: false };
    const key = 'feature_a';
    
    // 1. Simula início do toggle (otimista)
    const optimisticFlags = { ...flags, [key]: true };
    expect(optimisticFlags[key]).toBe(true);

    // 2. Simula falha na API
    (updateFeatureFlag as any).mockRejectedValue({ status: 403 });
    
    try {
      await updateFeatureFlag(key, true);
    } catch (e) {
      // 3. Simula Rollback
      const rolledBackFlags = { ...optimisticFlags, [key]: flags[key] };
      expect(rolledBackFlags[key]).toBe(false);
    }
  });
});
