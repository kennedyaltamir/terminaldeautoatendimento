import os

def fix_layouts():
    # Caminho do layout que pode estar causando conflito
    conflict_layout = os.path.join("frontend", "src", "app", "admin", "layout.tsx")
    
    if os.path.exists(conflict_layout):
        print(f"⚠️  Encontrado layout conflitante em: {conflict_layout}")
        print("   Este layout envolve a tela de login e pode causar loop infinito.")
        
        # Renomear para backup
        backup_name = conflict_layout + ".bak"
        if os.path.exists(backup_name):
            os.remove(backup_name)
            
        os.rename(conflict_layout, backup_name)
        print(f"✅ Layout renomeado para {backup_name}. O login deve funcionar agora.")
    else:
        print("✅ Nenhum layout conflitante encontrado na raiz de /admin.")

if __name__ == "__main__":
    fix_layouts()