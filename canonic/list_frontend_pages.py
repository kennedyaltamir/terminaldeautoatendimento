import os
from pathlib import Path

# ==============================================================================
# 🗺️ FRONTEND PAGE MAPPER
# ==============================================================================
# Varre a estrutura do Next.js App Router para listar todas as rotas acessíveis.
# ==============================================================================

def list_pages():
    base_dir = Path("frontend/src/app")
    if not base_dir.exists():
        print(f"❌ Diretório não encontrado: {base_dir}")
        return

    print(f"🔍 Mapeando páginas em: {base_dir}\n")
    
    pages = []
    for root, _, files in os.walk(base_dir):
        if "page.tsx" in files:
            # Calcula a rota relativa
            rel_path = Path(root).relative_to(base_dir)
            route = "/" + str(rel_path).replace("\\", "/")
            
            # Limpeza de rotas do Next.js
            route = route.replace("/.", "") # Raiz
            if route == "": route = "/"
            
            # Identifica se é rota dinâmica
            type_ = "Dinâmica" if "[" in route else "Estática"
            
            pages.append((route, type_))

    # Ordena por URL
    pages.sort(key=lambda x: x[0])

    print(f"{'TIPO':<10} | {'ROTA'}")
    print("-" * 60)
    for route, type_ in pages:
        print(f"{type_:<10} | {route}")
    
    print("-" * 60)
    print(f"✅ Total de páginas encontradas: {len(pages)}")

if __name__ == "__main__":
    list_pages()

