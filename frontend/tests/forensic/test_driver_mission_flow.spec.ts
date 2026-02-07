/**
 * 🕵️ MESAFLOW FORENSIC AGENT - LOGISTICS DOMAIN
 * DNA_ID: MF-QA-DRIVER-POMPEU-2026
 * Protocol: Sovereign Mission Cycle
 */

import { test, expect, Page } from '@playwright/test';

// Configurações de Perímetro Operacional
const TARGET_URL = '/admin/hamburgueria-ze/driver';
const POMPEU_MATRIZ = { latitude: -19.2244, longitude: -44.9354 };

class LogisticsForensicAgent {
  constructor(private page: Page) {}

  /** 🧬 Registra evento no log estruturado do CI */
  async log(phase: string, msg: string) {
    console.log(`[${new Date().toISOString()}] [PHASE=${phase}] 🔍 ${msg}`);
  }

  /** 🛡️ Garante que o ambiente está limpo e autenticado */
  async prepareEnvironment() {
    await this.page.addInitScript(() => {
      window.localStorage.clear();
      window.localStorage.setItem('mesaflow_tour_completed', 'true');
      window.localStorage.setItem('mesaflow_user_role', 'driver');
      window.localStorage.setItem('mesaflow_access_token', 'mock-forensic-token');
      // Injeta flag de bypass para o Sentinel e Middleware
      (window as any).__MESAFLOW_AUDIT_MODE__ = true;
    });
  }

  /** 👆 Simula o rito físico de pressionar e segurar (Hold Button) */
  async holdToAccept(selector: string, durationMs: number = 1500) {
    const btn = this.page.locator(selector);
    await btn.scrollIntoViewIfNeeded();
    const box = await btn.boundingBox();
    if (!box) throw new Error(`Element ${selector} not found or not visible for interaction.`);

    await this.page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
    await this.page.mouse.down();
    await this.page.waitForTimeout(durationMs);
    await this.page.mouse.up();
  }
}

test.describe('Logistics: Pompéu Mission Cycle', () => {
  
  test.beforeEach(async ({ context, page }) => {
    const agent = new LogisticsForensicAgent(page);
    
    // 🌍 Configuração de Satélite e Permissões
    await context.grantPermissions(['geolocation']);
    await context.setGeolocation(POMPEU_MATRIZ);
    
    // 🛡️ Bypass de Middleware via Header
    await page.route('**/*', async (route) => {
      const headers = {
        ...route.request().headers(),
        'x-e2e-test': 'true', // Autorização soberana para o Kernel
        'Authorization': 'Bearer mock-forensic-token'
      };
      await route.continue({ headers });
    });

    await agent.prepareEnvironment();
    
    // Drenagem de erros de console para o relatório
    page.on('console', msg => {
      if (msg.type() === 'error') console.error(`[BROWSER_ERROR] ${msg.text()}`);
    });
  });

  test('Ciclo de Vida da Missão: Aceite, Navegação e Cockpit Tático', async ({ page }) => {
    const agent = new LogisticsForensicAgent(page);

    await test.step('1. Boot Operacional (OFFLINE -> IDLE)', async () => {
      await agent.log('BOOT', 'Acessando Cockpit do Motorista...');
      await page.goto(TARGET_URL, { waitUntil: 'networkidle' });

      const startBtn = page.getByRole('button', { name: /Iniciar Trabalho/i });
      if (await startBtn.isVisible()) {
        await agent.log('BOOT', 'Iniciando turno físico...');
        await startBtn.click();
      }

      // Valida transição para estado de busca (Radar)
      await expect(page.getByTestId('driver-status-searching')).toBeVisible({ timeout: 10000 });
      await agent.log('BOOT', 'Motorista em modo IDLE (Radar Ativo).');
    });

    await test.step('2. Radar & Ingestão de Missão', async () => {
      await agent.log('SCAN', 'Aguardando missões seedadas no perímetro...');
      
      // Espera o card da missão aparecer no DOM
      const missionCard = page.locator('[data-testid*="mission-card"]').first();
      await expect(missionCard).toBeVisible({ timeout: 20000 });

      // Valida integridade dos dados injetados pelo seed
      await expect(page.locator('h2')).not.toHaveText(/Cliente não identificado/i);
      await expect(page.locator('text=Pompéu')).toBeVisible();
      
      await agent.log('SCAN', 'Missão legítima detectada em Pompéu.');
    });

    await test.step('3. Rito de Aceite (Atomic Handshake)', async () => {
      await agent.log('ACTION', 'Iniciando rito de aceite (Hold-to-Accept)...');
      
      // Executa a pressão longa no botão de aceite
      await agent.holdToAccept('[data-testid="btn-accept-mission"]');

      // Verifica mudança de estado na FSM via LocalStorage (Verdade Atômica)
      await expect.poll(async () => {
        return await page.evaluate(() => localStorage.getItem('mf_driver_state_hamburgueria-ze'));
      }, { timeout: 10000 }).toMatch(/ASSIGNED|EN_ROUTE/);
      
      await agent.log('ACTION', 'Transição de estado confirmada pelo Kernel.');
    });

    await test.step('4. Cockpit Tático & Telemetria', async () => {
      await agent.log('VERIFY', 'Validando interface de Missão Ativa...');

      // Verifica HUD Financeiro (Sovereignty Layer)
      await expect(page.getByTestId('financial-hud')).toBeVisible();

      // Verifica Mapa (GIS Layer) e presença de Rota (Polyline)
      const map = page.locator('.leaflet-container');
      await expect(map).toBeVisible();
      
      // Verifica se o Leaflet renderizou ao menos um caminho (SVG path)
      const routePath = page.locator('.leaflet-overlay-pane path');
      await expect(routePath.first()).toBeAttached({ timeout: 15000 });

      // Captura evidência forense final
      await page.screenshot({ 
        path: 'scripts/reports/evidence/pompeu_cockpit_vibranium_success.png',
        fullPage: true 
      });
      
      await agent.log('FINISH', 'Auditoria completa. Sistema íntegro para produção.');
    });
  });
});