import os
import sys

def verify():
    print("🔍 Verificando TASK-UX-02 & TASK-UX-03 (UI/UX Modernization)")
    
    # 1. Verificar Globals CSS
    css_path = "frontend/src/app/globals.css"
    if not os.path.exists(css_path):
        print(f"❌ Arquivo {css_path} não encontrado.")
        sys.exit(1)
    
    with open(css_path, "r", encoding="utf-8") as f:
        content = f.read()
        if ".glass-card" not in content:
            print("❌ Classe .glass-card não encontrada no CSS.")
            sys.exit(1)
        if "backdrop-blur" not in content:
            print("❌ Propriedade backdrop-blur não encontrada no CSS.")
            sys.exit(1)
            
    # 2. Verificar Componente Logo
    logo_path = "frontend/src/components/ui/Logo.tsx"
    if not os.path.exists(logo_path):
        print(f"❌ Componente Logo não encontrado em {logo_path}.")
        sys.exit(1)
        
    # 3. Verificar Hero Slogan
    hero_path = "frontend/src/components/landing/Hero.tsx"
    with open(hero_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "Onde a tecnologia encontra a hospitalidade" not in content:
            print("❌ Novo slogan não encontrado no Hero.")
            sys.exit(1)
            
    # 4. Verificar Admin Layout (AnimatePresence)
    layout_path = "frontend/src/app/admin/[slug]/layout.tsx"
    with open(layout_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "AnimatePresence" not in content:
            print("❌ AnimatePresence não encontrado no Admin Layout.")
            sys.exit(1)

    print("✅ UI/UX Modernization Verified Successfully.")
    sys.exit(0)

if __name__ == "__main__":
    verify()
