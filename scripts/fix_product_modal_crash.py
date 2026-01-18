import os
from pathlib import Path

# ==============================================================================
# 🩹 HOTFIX: ProductModal Null Pointer Exception
# ==============================================================================
# Corrige o erro "Cannot read properties of null (reading 'price')"
# adicionando um Guard Clause no início do componente.
# ==============================================================================

TARGET_FILE = Path("frontend/src/components/menu/ProductModal.tsx")

def apply_fix():
    if not TARGET_FILE.exists():
        print(f"❌ Arquivo não encontrado: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding="utf-8")
    
    # Verifica se já foi corrigido
    if "if (!product) return null;" in content:
        print("✅ Arquivo já possui a correção.")
        return

    # Aplica a correção
    # Procura pelo início da função e injeta o guard clause
    # Assumindo que a função começa com "export default function ProductModal" ou similar
    # e recebe props.
    
    lines = content.splitlines()
    new_lines = []
    injected = False
    
    for line in lines:
        new_lines.append(line)
        # Injeta logo após a desestruturação das props ou início da função
        # Heurística: Logo após a linha que contém "isOpen" e "product" (props)
        if not injected and "isOpen" in line and "product" in line and "{" in line:
             # Verifica se é a definição da função
             pass
        
        # Melhor estratégia: Inserir antes de qualquer uso de product.price
        # Mas precisamos inserir dentro do corpo da função.
        # Vamos procurar a linha "if (!isOpen) return null;" que geralmente existe em modais
        
        if "if (!isOpen) return null;" in line and not injected:
            new_lines.append("  if (!product) return null;")
            injected = True
            print("   💉 Guard clause injetado após verificação de isOpen.")

    if not injected:
        # Fallback: Tenta injetar antes do uso problemático
        print("   ⚠️  Padrão 'if (!isOpen)' não encontrado. Tentando patch direto no uso.")
        final_lines = []
        for line in lines:
            if "const basePrice = Number(product.price);" in line:
                final_lines.append("  if (!product) return null;")
                final_lines.append(line)
                injected = True
            else:
                final_lines.append(line)
        new_lines = final_lines

    if injected:
        TARGET_FILE.write_text("\n".join(new_lines), encoding="utf-8")
        print("✅ Correção aplicada com sucesso.")
    else:
        print("❌ Não foi possível aplicar a correção automaticamente. Verifique o arquivo manualmente.")

if __name__ == "__main__":
    apply_fix()

