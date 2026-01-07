import { JwtService } from '../auth/jwt';
import { jwtDecode } from 'jwt-decode';

jest.mock('jwt-decode');

describe('JwtService Semantic Validation', () => {
  const validToken = 'valid.token.payload';

  it('deve rejeitar token sem company_id', () => {
    (jwtDecode as jest.Mock).mockReturnValue({
      sub: 'test@test.com',
      role: 'kitchen',
      // company_id ausente
    });

    const isValid = JwtService.validateClaims(validToken);
    expect(isValid).toBe(false);
  });

  it('deve rejeitar token sem role', () => {
    (jwtDecode as jest.Mock).mockReturnValue({
      sub: 'test@test.com',
      company_id: '123',
      // role ausente
    });

    const isValid = JwtService.validateClaims(validToken);
    expect(isValid).toBe(false);
  });

  it('deve aceitar token com todas as claims obrigatórias', () => {
    (jwtDecode as jest.Mock).mockReturnValue({
      sub: 'test@test.com',
      role: 'kitchen',
      company_id: '123'
    });

    const isValid = JwtService.validateClaims(validToken);
    expect(isValid).toBe(true);
  });
});
