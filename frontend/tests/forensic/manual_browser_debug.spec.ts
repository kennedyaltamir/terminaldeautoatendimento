/**
 * 🕵️ MESAFLOW MANUAL DEBUG AGENT (v1.5 - Forensic Handover)
 */
import { test, expect } from '@playwright/test';

test('Rito de Entrada e Navegação Manual', async ({ page }) => {
  console.log('🔐 Limpando ambiente e gerando novo Token...');
  
  await page.goto('http://127.0.0.1:3000');
  await page.evaluate(() => {
    localStorage.clear();
    sessionStorage.clear();
  });

  await page.goto('http://127.0.0.1:3000/admin/login');
  await page.fill('input[name="email"]', 'admin@mesaflow.com');
  await page.fill('input[name="password"]', '123456');
  await page.click('button[type="submit"]');
  
  await page.waitForURL('**/dashboard');
  await page.goto('http://127.0.0.1:3000/admin/hamburgueria-ze/driver');

  await page.evaluate(() => {
    localStorage.setItem('mesaflow_tour_completed', 'true');
  });

  console.log('\n' + '⭐'.repeat(30));
  console.log('SISTEMA PRONTO PARA TESTE HUMANO');
  console.log('1. Tente aceitar a missão (Hold button)');
  console.log('2. O robô ficará parado esperando por você.');
  console.log('⭐'.repeat(30) + '\n');

  // 🛡️ O rito de "Pause" impede o fechamento pelo timeout do teste
  await page.pause(); 
});

