import { test, expect } from '@playwright/test';

/**
 * 🕵️ MESAFLOW VISUAL INSPECTOR (BLACK BOX RECORDER)
 * Domain: Forensic Diagnostics
 * Objective: Capture live runtime events during manual interaction.
 * Duration: 300 seconds (5 minutes)
 */

const TARGET_URL = '/admin/hamburgueria-ze/driver';

// 🛡️ FIX: Configuração movida para o escopo global do arquivo
test.use({ 
  headless: false, 
  viewport: { width: 414, height: 896 },
  launchOptions: { slowMo: 0 }
});

test.describe('Visual Inspection: Driver Cockpit', () => {

  test.beforeEach(async ({ context }) => {
    await context.grantPermissions(['geolocation']);
    await context.setGeolocation({ latitude: -23.5505, longitude: -46.6333 });
    
    await context.addInitScript(() => {
      window.localStorage.setItem('mesaflow_access_token', 'mock-driver-token-forensic');
      window.localStorage.setItem('mesaflow_user_role', 'driver');
      window.localStorage.setItem('mesaflow_tour_completed', 'true');
      console.log("💉 [INJECTOR] Tokens de autenticação inseridos.");
    });
  });

  test('🔴 LIVE RECORDER: 5 Minutes of Sovereign Observation', async ({ page }) => {
    // Timeout estendido para permitir a inspeção manual
    test.setTimeout(310000); 

    console.log('\n' + '='.repeat(60));
    console.log('🎥 INICIANDO GRAVAÇÃO FORENSE (5 MINUTOS)');
    console.log('👉 INTERAJA COM A TELA AGORA. O TERMINAL REGISTRARÁ TUDO.');
    console.log('='.repeat(60) + '\n');

    // 1. DRENAGEM DE CONSOLE
    page.on('console', msg => {
      const type = msg.type().toUpperCase();
      const text = msg.text();
      if (text.includes('[Fast Refresh]')) return;
      
      const color = type === 'ERROR' ? '\x1b[31m' : type === 'WARNING' ? '\x1b[33m' : '\x1b[36m';
      console.log(`${color}[BROWSER_${type}] ${text}\x1b[0m`);
    });

    // 2. DRENAGEM DE REDE
    page.on('request', req => {
      if (req.url().includes('/api/')) {
        console.log(`📡 [REQ] ${req.method()} ${req.url().split('/api/')[1]}`);
      }
    });

    page.on('requestfailed', req => {
      console.log(`❌ [REQ_FAIL] ${req.url()} - ${req.failure()?.errorText}`);
    });

    page.on('response', async res => {
      if (res.url().includes('/api/')) {
        const status = res.status();
        const color = status >= 400 ? '\x1b[31m' : '\x1b[32m';
        console.log(`${color}📥 [RES] ${status} ${res.url().split('/api/')[1]}\x1b[0m`);
        
        if (status >= 400) {
          try {
            const body = await res.json();
            console.log(`   ⚠️ Payload de Erro:`, JSON.stringify(body, null, 2));
          } catch (e) {
            console.log(`   ⚠️ Corpo não é JSON.`);
          }
        }
      }
    });

    // 3. NAVEGAÇÃO
    await page.goto(TARGET_URL);

    // 4. JANELA DE OBSERVAÇÃO
    await page.waitForTimeout(300000); 

    console.log('\n' + '='.repeat(60));
    console.log('🛑 FIM DA JANELA DE OBSERVAÇÃO');
    console.log('='.repeat(60) + '\n');
  });
});

