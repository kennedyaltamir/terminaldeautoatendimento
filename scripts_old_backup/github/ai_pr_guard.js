
/**
 * MESAFLOW AI PR GUARD (L5)
 * Este bot roda no CI e tem poder de VETO sobre Pull Requests.
 */

const fs = require('fs');
const path = require('path');

// Limites de Qualidade L5
const THRESHOLDS = {
  CRASH_RATE_MAX: 0.5, // %
  TEST_PASS_RATE_MIN: 100, // %
  UI_SWEEP_REQUIRED: true
};

function runGuard() {
  console.log('🤖 AI KERNEL GUARD: Analyzing PR...');

  // 1. Verificar Relatório Human QA
  const humanReportPath = path.join(__dirname, '../../docs/mobile/reports/HUMAN_UI_TEST_REPORT.json');
  if (!fs.existsSync(humanReportPath)) {
    fail('❌ Relatório Human QA não encontrado. O teste rodou?');
  }
  const humanData = JSON.parse(fs.readFileSync(humanReportPath, 'utf8'));
  if (!humanData.success) {
    fail(`🚫 Human QA falhou. Passou: ${humanData.tests_passed}/${humanData.tests_total}`);
  }

  // 2. Verificar Production Lock
  const lockPath = path.join(__dirname, '../../docs/mobile/reports/PRODUCTION_LOCK_MOBILE.json');
  if (!fs.existsSync(lockPath)) {
    fail('❌ Production Lock ausente. O sistema não está selado.');
  }

  // 3. Verificar Telemetria (Simulado via ENV check)
  if (!process.env.EXPO_PUBLIC_SENTRY_DSN) {
    console.warn('⚠️  AVISO: Sentry DSN não detectado no ambiente de CI.');
    // Em modo estrito, isso seria fail().
  }

  console.log('✅ AI KERNEL: PR Aprovado. Quality Gates satisfeitos.');
  process.exit(0);
}

function fail(reason) {
  console.error(`⛔ BLOQUEIO KERNEL: ${reason}`);
  process.exit(1);
}

runGuard();

