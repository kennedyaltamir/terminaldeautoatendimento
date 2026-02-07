import { test, expect, BrowserContext, Page } from '@playwright/test';
import fs from 'fs';
import path from 'path';

const BASE_URL = 'http://localhost:3000';
const TARGET_SLUG = 'hamburgueria-ze';
const DRIVER_URL = `${BASE_URL}/admin/${TARGET_SLUG}/driver`;
const EVIDENCE_DIR = path.resolve(__dirname, '../../../audit_evidence/driver_v2');

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

test.describe('Driver Cockpit Production Audit V2 (Sovereign)', () => {
  let report: AuditReport = {
    timestamp: new Date().toISOString(),
    status: 'PASSED',
    checks: []
  };

  test.use({
    viewport: { width: 390, height: 844 },
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    hasTouch: true,
    geolocation: { latitude: -23.5505, longitude: -46.6333 },
    permissions: ['geolocation']
  });

  // FIX: Tipagem explícita para context
  test.beforeEach(async ({ context }: { context: BrowserContext }) => {
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
      window.localStorage.removeItem(`mf_driver_state_${TARGET_SLUG}`);
    });
  });

  test.afterAll(async () => {
    const reportFile = path.join(EVIDENCE_DIR, `audit_report_${Date.now()}.json`);
    fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
  });

  // FIX: Tipagem explícita para page
  test('Validar Ciclo Operacional Completo e Conformidade de UI', async ({ page }: { page: Page }) => {
    const logCheck = (element: string, status: 'OK' | 'MISSING' | 'ERROR', details?: string) => {
      report.checks.push({ element, status, details });
      if (status !== 'OK') report.status = 'FAILED';
      console.log(`[${status}] ${element} ${details ? `- ${details}` : ''}`);
    };

    try {
      await page.goto(DRIVER_URL, { waitUntil: 'networkidle' });

      const startBtn = page.getByTestId('start-shift-button');
      if (await startBtn.isVisible()) {
        logCheck('State: OFFLINE', 'OK');
        await startBtn.click();
        await page.waitForTimeout(1000);
      }

      const header = page.locator('header');
      await expect(header).toBeVisible();
      logCheck('Header Vitals', 'OK');

      const nav = page.locator('nav');
      await expect(nav).toBeVisible();
      logCheck('Bottom Navigation', 'OK');

      const idleView = page.locator('text=Buscando Missões');
      await expect(idleView).toBeVisible();
      logCheck('Idle Radar', 'OK');

    } catch (error: any) {
      logCheck('Critical Runtime', 'ERROR', error.message);
      await page.screenshot({ path: path.join(EVIDENCE_DIR, 'critical_failure.png') });
      throw error;
    }
  });
});
