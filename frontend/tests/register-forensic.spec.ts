import { test, expect, Page } from '@playwright/test';
import fs from 'fs';
import path from 'path';

const BASE_URL = 'http://localhost:3000/admin/register';
const RESULTS_DIR = path.join(process.cwd(), 'resultados');

async function ensureResultsFolder() {
  if (!fs.existsSync(RESULTS_DIR)) {
    fs.mkdirSync(RESULTS_DIR, { recursive: true });
  }
}

async function dumpDOMElements(page: Page, step: string) {
  const elements = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('*')).map(el => ({
      tag: el.tagName,
      id: el.id,
      class: el.className,
      text: el.textContent?.trim().substring(0, 30)
    }));
  });
  fs.writeFileSync(path.join(RESULTS_DIR, `${step}_elements.json`), JSON.stringify(elements, null, 2));
  console.log(`[FORENSIC] DOM_DUMP: ${step} registrado.`);
}

async function updateAuditDoc(verdict: string, details: string) {
  const content = `# MESAFLOW FORENSIC AUDIT\n\n- **Data**: ${new Date().toISOString()}\n- **Veredito**: ${verdict}\n- **Detalhes**: ${details}\n`;
  fs.writeFileSync(path.join(RESULTS_DIR, 'AUDIT_SUMMARY.md'), content);
  console.log(`[FORENSIC] DOC_UPDATE: Relatório MD atualizado.`);
}

test.describe('MesaFlow Registration Forensics v4.1', () => {

  test.beforeEach(async ({ page }) => {
    await ensureResultsFolder();
    page.on('console', msg => {
      if (msg.type() === 'error') console.log(`[BROWSER_ERROR] ${msg.text()}`);
    });
    await page.goto(BASE_URL);
    await expect(page.locator('input[name="company_name"]')).toBeVisible({ timeout: 30000 });
    await page.evaluate(() => localStorage.clear());
  });

  test('[REG-01] Ciclo Forense Completo', async ({ page }) => {
    const uniqueId = Date.now();
    const testName = `Forensic Grill ${uniqueId}`;
    const testSlug = `forensic-grill-${uniqueId}`;

    console.log(`[INIT] Iniciando Auditoria REG-01 com ID: ${uniqueId}`);
    await dumpDOMElements(page, 'START');

    const interactables = await page.locator('button, a, label, input').all();
    console.log(`[ACTION] Interagindo com ${interactables.length} elementos.`);
    
    for (const el of interactables.slice(0, 10)) {
      try { if (await el.isVisible()) await el.hover({ timeout: 500 }); } catch (e) {}
    }

    await page.locator('label').filter({ hasText: 'Restaurante' }).click();

    const slugPromise = page.waitForResponse(r => r.url().includes('check-slug'));
    await page.locator('input[name="company_name"]').fill(testName);
    await slugPromise;
    
    const slugInput = page.getByPlaceholder('link-da-loja');
    await expect(slugInput).toHaveValue(testSlug);
    await expect(page.locator('svg.text-green-500').first()).toBeVisible({ timeout: 10000 });

    await page.getByRole('button', { name: 'Próximo' }).click();
    await expect(page.locator('input[name="owner_role"]')).toBeVisible({ timeout: 15000 });

    await page.locator('input[name="owner_role"]').fill('Auditor');
    await page.locator('input[name="owner_phone"]').fill('11999999999');
    await page.locator('input[name="owner_email"]').fill(`forensic_${uniqueId}@test.com`);
    await page.locator('input[name="password"]').fill('SenhaForte123!');

    const regPromise = page.waitForResponse(r => r.url().includes('/auth/register'));
    await page.getByRole('button', { name: 'Finalizar' }).click();
    await regPromise;

    await expect(page.getByText('Conta criada com sucesso!').first()).toBeVisible();
    await page.screenshot({ path: path.join(RESULTS_DIR, 'evidence.png'), fullPage: true });
    
    await updateAuditDoc('PASSED', `Fluxo completo validado para o slug: ${testSlug}`);
    
    const finalReport = { id: "REG-01", status: "PASSED", slug: testSlug, timestamp: new Date().toISOString() };
    fs.writeFileSync(path.join(RESULTS_DIR, 'report.json'), JSON.stringify(finalReport, null, 2));
    console.log('[DONE] Ciclo forense concluído com sucesso.');
  });

});