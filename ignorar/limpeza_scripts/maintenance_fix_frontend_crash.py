import os
import re

def fix_layout_imports():
    print("🚑 Iniciando Reparo de Emergência no Frontend...")
    
    file_path = "frontend/src/app/admin/[slug]/layout.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado: {file_path}")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Diagnóstico: Verifica se ChefHat é usado mas não importado
        is_used = "icon: ChefHat" in content
        is_imported = "ChefHat," in content or ", ChefHat" in content or "{ ChefHat }" in content

        if is_used and not is_imported:
            print("🔍 Erro detectado: 'ChefHat' usado mas não importado.")
            
            # Regex para encontrar a linha de import do lucide-react
            # Procura por: import { ... } from "lucide-react";
            pattern = r'(import\s*{[^}]*)(\}\s*from\s*"lucide-react")'
            
            if re.search(pattern, content):
                # Injeta ChefHat na lista de imports
                new_content = re.sub(pattern, r'\1, ChefHat \2', content)
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print("✅ Correção aplicada: 'ChefHat' adicionado aos imports.")
            else:
                print("❌ Não foi possível localizar a linha de import do lucide-react.")
        else:
            print("✅ O arquivo parece estar correto quanto ao ChefHat.")

    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {e}")

def check_env_google():
    print("\n🔍 Verificando Variáveis de Ambiente (Google Auth)...")
    env_path = ".env"
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            env_content = f.read()
            if "NEXT_PUBLIC_GOOGLE_CLIENT_ID" not in env_content:
                print("⚠️  AVISO: 'NEXT_PUBLIC_GOOGLE_CLIENT_ID' não encontrado no .env.")
                print("   O login social falhará. Adicione uma chave válida ou mock.")
            else:
                print("✅ Variável do Google detectada.")

if __name__ == "__main__":
    fix_layout_imports()
    check_env_google()
    print("\n🚀 Reparo concluído. O Next.js deve recompilar automaticamente (Fast Refresh).")
