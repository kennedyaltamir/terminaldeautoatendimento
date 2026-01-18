import os

# Configuração de pastas para ignorar (reduz ruído)
IGNORE_DIRS = {
    '.git', 'node_modules', 'venv', '.venv', '__pycache__', 
    '.next', 'dist', 'build', '.pytest_cache', 'coverage',
    'android', 'ios' # Pastas de build mobile pesadas
}

OUTPUT_FILE = "estrutura_atual.txt"

def analyze_structure():
    output = []
    root = '.'
    
    # 1. Analisar a Raiz
    output.append("=== 1. ESTRUTURA DA RAIZ ===")
    try:
        root_items = sorted(os.listdir(root))
    except Exception as e:
        print(f"Erro ao ler raiz: {e}")
        return

    subdirectories = []

    for item in root_items:
        if item in IGNORE_DIRS:
            continue
            
        if os.path.isdir(item):
            output.append(f"📁 {item}/")
            subdirectories.append(item)
        else:
            output.append(f"📄 {item}")

    # 2. Analisar Nível 1 (Conteúdo imediato de cada pasta da raiz)
    output.append("\n=== 2. CONTEÚDO DAS SUBPASTAS (NÍVEL 1) ===")
    
    for folder in subdirectories:
        output.append(f"\n📂 DENTRO DE: {folder}/")
        try:
            sub_items = sorted(os.listdir(folder))
            if not sub_items:
                output.append("   (Vazio)")
                continue

            for sub_item in sub_items:
                if sub_item in IGNORE_DIRS:
                    continue
                
                full_path = os.path.join(folder, sub_item)
                if os.path.isdir(full_path):
                    output.append(f"   📁 {sub_item}/")
                else:
                    output.append(f"   📄 {sub_item}")
        except Exception as e:
            output.append(f"   ❌ Erro ao ler pasta: {e}")

    # Salvar e Imprimir
    final_text = "\n".join(output)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_text)
    
    print(final_text)
    print(f"\n✅ Análise salva em: {OUTPUT_FILE}")
    print("👉 Copie o conteúdo deste arquivo e me envie para prosseguirmos com a limpeza.")

if __name__ == "__main__":
    analyze_structure()
