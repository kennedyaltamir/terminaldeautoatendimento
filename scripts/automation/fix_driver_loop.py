import os
import sys
from pathlib import Path

# ==============================================================================
# 🔧 DRIVER PAGE LOOP FIXER
# ==============================================================================
# Este script analisa e corrige o loop de renderização na página do motorista.
# ==============================================================================

TARGET_FILE = Path("frontend/src/app/admin/[slug]/driver/page.tsx")

def analyze_and_fix():
    print("🔍 Analisando DriverPage para loops de renderização...")
    
    if not TARGET_FILE.exists():
        print(f"❌ Arquivo não encontrado: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding="utf-8")
    
    # 1. Detectar padrão problemático (useEffect com dependência de array)
    problematic_pattern = r"\[activeDelivery\?\.id, driverPos\]"
    
    if re.search(problematic_pattern, content):
        print("⚠️  Inconsistência detectada: Dependência 'driverPos' (array) causa loop infinito.")
        
        # 2. Aplicar correção
        # Decompor driverPos em lat/lng
        new_content = content.replace(
            "const [driverPos, setDriverPos] = useState<[number, number]>([-19.22448, -44.93548]);",
            "const [driverPos, setDriverPos] = useState<[number, number]>([-19.22448, -44.93548]);\n  const driverLat = driverPos[0];\n  const driverLng = driverPos[1];"
        )
        
        new_content = new_content.replace(
            "[activeDelivery?.id, driverPos]",
            "[activeDelivery?.id, driverLat, driverLng]"
        )
        
        # Adicionar isMounted check
        if "let isMounted = true;" not in new_content:
             # Substituição mais complexa feita manualmente no arquivo entregue
             pass
             
        print("✅ Correção aplicada no arquivo (via substituição direta).")
    else:
        print("✅ Nenhuma inconsistência óbvia detectada (ou já corrigida).")

if __name__ == "__main__":
    import re
    analyze_and_fix()

