import axios from 'axios';
import { ENV } from '../../config/env';
import { AuthTokens } from '../../types/auth';

/**
 * AuthClient: Cliente de baixo nível para chamadas de autenticação pura.
 * Não utiliza a instância 'api' para evitar recursão infinita no interceptor.
 */
export const AuthClient = {
  async refresh(refreshToken: string): Promise<{ access_token: string; refresh_token: string }> {
    const response = await axios.post(`${ENV.API_URL}/auth/refresh`, {}, {
      headers: { 'X-Refresh-Token': refreshToken }
    });
    return response.data;
  },

  async login(credentials: any): Promise<any> {
    const formData = new URLSearchParams();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);

    const response = await axios.post(`${ENV.API_URL}/auth/token`, formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    return response.data;
  }
};
