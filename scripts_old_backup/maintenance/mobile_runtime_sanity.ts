
/**
 * MOBILE RUNTIME SANITY CHECK
 * Valida inicialização + registro de telas
 */

import { SCREEN_REGISTRY } from "../../mobile/src/navigation/screenRegistry";

console.log("🧪 MOBILE RUNTIME SANITY CHECK");

if (!Array.isArray(SCREEN_REGISTRY) || SCREEN_REGISTRY.length === 0) {
  console.error("❌ Nenhuma tela registrada no SCREEN_REGISTRY.");
  process.exit(1);
}

console.log(`✅ ${SCREEN_REGISTRY.length} telas registradas:`);

SCREEN_REGISTRY.forEach(screen => {
  console.log(`   - ${screen}`);
});

console.log("✅ SANITY CHECK FINALIZADO — Registro de telas OK.");
process.exit(0);

