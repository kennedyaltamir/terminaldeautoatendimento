import { useAuthStore } from '../auth.store';
import { SecureAuthStorage } from '../../services/auth/storage';
import { AuthClient } from '../../services/auth/client';
import { JwtService } from '../../services/auth/jwt';

// Mock das dependências
jest.mock('../../services/auth/storage');
jest.mock('../../services/auth/client');
jest.mock('../../services/notifications.service');
jest.mock('../../services/auth/jwt');

describe('AuthStore Integration (TASK-014A)', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    useAuthStore.setState({ status: 'idle', accessToken: null, user: null });
  });

  it('deve transitar para unauthenticated se não houver tokens no storage', async () => {
    (SecureAuthStorage.getAccessToken as jest.Mock).mockResolvedValue(null);
    await useAuthStore.getState().hydrate();
    expect(useAuthStore.getState().status).toBe('unauthenticated');
  });

  it('deve transitar para unauthenticated se o token tiver claims inválidas', async () => {
    (SecureAuthStorage.getAccessToken as jest.Mock).mockResolvedValue('invalid_claims_token');
    (SecureAuthStorage.getRefreshToken as jest.Mock).mockResolvedValue('refresh_token');
    
    // Simula falha na validação de claims
    (JwtService.validateClaims as jest.Mock).mockReturnValue(false);

    await useAuthStore.getState().hydrate();

    expect(useAuthStore.getState().status).toBe('unauthenticated');
    expect(SecureAuthStorage.clear).toHaveBeenCalled();
  });

  it('deve tentar refresh se o token estiver expirado', async () => {
    (SecureAuthStorage.getAccessToken as jest.Mock).mockResolvedValue('expired_token');
    (SecureAuthStorage.getRefreshToken as jest.Mock).mockResolvedValue('valid_refresh_token');
    
    // Claims válidas, mas expirado
    (JwtService.validateClaims as jest.Mock).mockReturnValue(true);
    (JwtService.isTokenExpired as jest.Mock).mockReturnValue(true);

    // Mock do sucesso no refresh
    const newTokens = { access_token: 'new_at', refresh_token: 'new_rt' };
    (AuthClient.refresh as jest.Mock).mockResolvedValue(newTokens);
    
    // Mock das claims do novo token
    const newClaims = { sub: 'user@test.com', role: 'kitchen', company_id: '123' };
    (JwtService.getClaims as jest.Mock).mockReturnValue(newClaims);

    await useAuthStore.getState().hydrate();

    expect(AuthClient.refresh).toHaveBeenCalledWith('valid_refresh_token');
    expect(SecureAuthStorage.saveTokens).toHaveBeenCalledWith({
      accessToken: 'new_at',
      refreshToken: 'new_rt'
    });
    expect(useAuthStore.getState().status).toBe('authenticated');
  });

  it('deve fazer logout se o refresh falhar', async () => {
    (SecureAuthStorage.getAccessToken as jest.Mock).mockResolvedValue('expired_token');
    (SecureAuthStorage.getRefreshToken as jest.Mock).mockResolvedValue('invalid_refresh_token');
    
    (JwtService.validateClaims as jest.Mock).mockReturnValue(true);
    (JwtService.isTokenExpired as jest.Mock).mockReturnValue(true);

    // Simula erro no refresh
    (AuthClient.refresh as jest.Mock).mockRejectedValue(new Error('Refresh failed'));

    await useAuthStore.getState().hydrate();

    expect(useAuthStore.getState().status).toBe('unauthenticated');
    expect(SecureAuthStorage.clear).toHaveBeenCalled();
  });

  it('deve autenticar com sucesso se o token for válido e não expirado', async () => {
    (SecureAuthStorage.getAccessToken as jest.Mock).mockResolvedValue('valid_token');
    (SecureAuthStorage.getRefreshToken as jest.Mock).mockResolvedValue('valid_refresh');
    
    (JwtService.validateClaims as jest.Mock).mockReturnValue(true);
    (JwtService.isTokenExpired as jest.Mock).mockReturnValue(false);
    
    const claims = { sub: 'user@test.com', role: 'kitchen', company_id: '123' };
    (JwtService.getClaims as jest.Mock).mockReturnValue(claims);

    await useAuthStore.getState().hydrate();

    expect(useAuthStore.getState().status).toBe('authenticated');
    expect(useAuthStore.getState().user?.email).toBe('user@test.com');
  });
});
