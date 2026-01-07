import { useAuthStore } from '../auth.store';
import { SecureAuthStorage } from '../../services/auth/storage';
import { AuthClient } from '../../services/auth/client';
import { JwtService } from '../../services/auth/jwt';

// Mock das dependências nativas e de rede
jest.mock('../../services/auth/storage');
jest.mock('../../services/auth/client');
jest.mock('../../services/notifications.service');
jest.mock('../../services/auth/jwt');

describe('AuthStore Integration', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    useAuthStore.setState({ status: 'idle', accessToken: null, user: null });
  });

  it('deve transitar para unauthenticated se não houver tokens no storage', async () => {
    (SecureAuthStorage.getAccessToken as jest.Mock).mockResolvedValue(null);
    
    await useAuthStore.getState().hydrate();
    
    expect(useAuthStore.getState().status).toBe('unauthenticated');
  });

  it('deve realizar login com sucesso e salvar tokens se o payload for válido', async () => {
    const mockTokens = { access_token: 'valid_at', refresh_token: 'valid_rt' };
    const mockClaims = { sub: 'test@test.com', role: 'kitchen', company_id: '123' };

    (AuthClient.login as jest.Mock).mockResolvedValue(mockTokens);
    (JwtService.validateClaims as jest.Mock).mockReturnValue(true);
    (JwtService.getClaims as jest.Mock).mockReturnValue(mockClaims);

    await useAuthStore.getState().login({ email: 'test@test.com', password: '123' });

    expect(useAuthStore.getState().status).toBe('authenticated');
    expect(useAuthStore.getState().accessToken).toBe('valid_at');
    expect(useAuthStore.getState().user?.email).toBe('test@test.com');
    expect(SecureAuthStorage.saveTokens).toHaveBeenCalledWith({
      accessToken: 'valid_at',
      refreshToken: 'valid_rt'
    });
  });

  it('deve falhar se o servidor retornar um token sem claims obrigatórias', async () => {
    const mockTokens = { access_token: 'invalid_at', refresh_token: 'rt' };
    (AuthClient.login as jest.Mock).mockResolvedValue(mockTokens);
    (JwtService.validateClaims as jest.Mock).mockReturnValue(false);

    await expect(useAuthStore.getState().login({ email: 'test@test.com', password: '123' }))
      .rejects.toThrow();

    expect(useAuthStore.getState().status).toBe('unauthenticated');
  });

  it('deve limpar o estado e o storage no logout', async () => {
    useAuthStore.setState({ status: 'authenticated', accessToken: 'at' });
    
    await useAuthStore.getState().logout();

    expect(useAuthStore.getState().status).toBe('unauthenticated');
    expect(useAuthStore.getState().accessToken).toBe(null);
    expect(SecureAuthStorage.clear).toHaveBeenCalled();
  });
});
