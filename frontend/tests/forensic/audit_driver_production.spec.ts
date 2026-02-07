/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 4.2.1 (TypeScript Hardened)
 * DNA_ID: MF-DRIVER-AUDIT-TS-FIX
 * OBJETIVO: Auditoria de produção com tipagem estrita para evitar erros de compilação TS.
 */
import { test, expect, type Page, type BrowserContext } from '@playwright/test';
import fs from 'fs';
import path from 'path';

const BASE_URL = 'http://localhost:3000';
const TARGET_SLUG = 'hamburgueria-ze';
const DRIVER_URL = `${BASE_URL}/admin/${TARGET_SLUG}/driver`;
const EVIDENCE_DIR = path.resolve(__dirname, '../../../audit_evidence');

// Garante diretório de evidências
if (!fs.existsSync(EVIDENCE_DIR)) {
  fs.mkdirSync(EVIDENCE_DIR, { recursive: true });
}

interface AuditReport {
  timestamp: string;
  status: 'PASSED' | 'FAILED';
  checks: {
    element: string;
    status: 'OK' | 'MISSING' | 'ERROR';
    details?: string;
  }[];
}

test.describe('Driver Cockpit Production Audit', () => {
  let report: AuditReport = {
    timestamp: new Date().toISOString(),
    status: 'PASSED',
    checks: [],
  };

  // 🛡️ FIX: Tipagem explícita do context para resolver TS7031
  test.beforeEach(async ({ context }: { context: BrowserContext }) => {
    await context.grantPermissions(['geolocation']);
    await context.setGeolocation({ latitude: -23.5505, longitude: -46.6333 });

    await context.addCookies([{
      name: 'auth_token',
      value: 'mock-production-token',
      domain: 'localhost',
      path: '/'
    }]);

    await context.addInitScript(() => {
      window.localStorage.setItem('mesaflow_access_token', 'mock-production-token');
      window.localStorage.setItem('mesaflow_user_role', 'driver');
      window.localStorage.setItem('mesaflow_tour_completed', 'true');
    });
  });

  test.afterAll(async () => {
    const reportFile = path.join(EVIDENCE_DIR, `audit_report_${Date.now()}.json`);
    fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
    console.log(`📄 Relatório de auditoria salvo em: ${reportFile}`);
  });

  // 🛡️ FIX: Tipagem explícita da page para resolver TS7031
  test('Validar Integridade Operacional do Cockpit', async ({ page }: { page: Page }) => {
    const logCheck = (element: string, status: 'OK' | 'MISSING' | 'ERROR', details?: string) => {
      report.checks.push({ element, status, details });
      if (status !== 'OK') report.status = 'FAILED';
      const icon = status === 'OK' ? '✅' : status === 'MISSING' ? '⚠️' : '❌';
      console.log(`${icon} [${status}] ${element} ${details ? `- ${details}` : ''}`);
    };

    try {
      await page.goto(DRIVER_URL, { waitUntil: 'networkidle' });

      // 1. Validação de Carregamento
      await expect(page).not.toHaveURL(/.*login.*/);
      logCheck('Page Load', 'OK');

      // 2. Header Vitals
      const header = page.locator('header');
      await expect(header).toBeVisible();
      logCheck('Header Vitals', 'OK');

      // 3. Transição OFFLINE -> IDLE
      const startBtn = page.getByRole('button', { name: /Iniciar Turno|Iniciar Trabalho/i });
      if (await startBtn.isVisible()) {
        await startBtn.click();
        await page.waitForTimeout(1000);
        logCheck('Shift Start Action', 'OK');
      }

      // 4. Navegação de Abas (Resiliente a nomes)
      const mapTab = page.getByRole('button', { name: /Seus Pedidos|Rota/i });
      await expect(mapTab).toBeVisible();
      await mapTab.click();
      logCheck('Tab: Rota/Pedidos', 'OK');

      // 5. Verificação do Mapa (Leaflet)
      const mapContainer = page.locator('.leaflet-container');
      const idleState = page.getByText(/Buscando Missões|Nenhuma entrega/i);
      
      if (await mapContainer.isVisible() || await idleState.isVisible()) {
        logCheck('Operational View', 'OK', 'Map or Idle state active');
      } else {
        logCheck('Operational View', 'ERROR', 'Map container not rendered');
      }

      // 6. Segurança: Stealth Mode
      const stealthBtn = page.locator('button').filter({ has: page.locator('svg.lucide-eye, svg.lucide-eye-off') }).first();
      if (await stealthBtn.isVisible()) {
        await stealthBtn.click();
        logCheck('Stealth Mode Toggle', 'OK');
      }

    } catch (error: any) {
      logCheck('Critical Runtime', 'ERROR', error.message);
      await page.screenshot({ path: path.join(EVIDENCE_DIR, 'failure_snapshot.png') });
      throw error;
    }
  });
});