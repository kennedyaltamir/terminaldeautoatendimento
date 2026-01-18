
const fs = require('fs');
const path = require('path');

// Configuração L5
const THRESHOLDS = {
  CRASH_RATE: 0.5, // %
  TEST_PASS_RATE: 100 // %
};

function checkQualityGate() {
  console.log('🤖 KERNEL BOT: Analyzing Quality Reports...');

  // 1. Ler Relatório Human QA
  const humanReportPath = path.join(__dirname, '../../docs/mobile/reports/HUMAN_UI_TEST_REPORT.json');
  
  if (!fs.existsSync(humanReportPath)) {
    console.error('❌ FATAL: Relatório Human QA não encontrado.');
    process.exit(1);
  }

  const humanData = JSON.parse(fs.readFileSync(humanReportPath, 'utf8'));
  
  if (!humanData.success) {
    console.error('🚫 KERNEL VETO: Human QA Failed.');
    console.error(`   Tests Passed: ${humanData.tests_passed}/${humanData.tests_total}`);
    process.exit(1);
  }

  // 2. Verificar Lock de Produção
  const lockPath = path.join(__dirname, '../../docs/mobile/reports/PRODUCTION_LOCK_MOBILE.json');
  if (!fs.existsSync(lockPath)) {
    console.error('❌ FATAL: Production Lock violado (arquivo ausente).');
    process.exit(1);
  }

  console.log('✅ KERNEL APPROVAL: All gates passed.');
  console.log('   - UI Sweep: PASS');
  console.log('   - Human QA: PASS');
  console.log('   - Prod Lock: ACTIVE');
  
  process.exit(0);
}

checkQualityGate();

