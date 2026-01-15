import { COLORS } from '../src/ui/tokens/colors';

function assertKey(path: string, value: any) {
  if (value === undefined) {
    throw new Error(`❌ TOKEN AUSENTE: ${path}`);
  }
}

console.log('🎨 Verificando tokens de cor...');

assertKey('COLORS.background', COLORS.background);
assertKey('COLORS.text.primary', COLORS.text.primary);
assertKey('COLORS.text.secondary', COLORS.text.secondary);
assertKey('COLORS.status.danger', COLORS.status.danger);
assertKey('COLORS.status.success', COLORS.status.success);
assertKey('COLORS.status.warning', COLORS.status.warning);
assertKey('COLORS.status.info', COLORS.status.info);

console.log('✅ Tokens de cor OK');
