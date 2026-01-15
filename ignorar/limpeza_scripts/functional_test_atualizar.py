import os, shutil, sys

# Adiciona o diretório raiz ao PATH para encontrar o atualizar.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_automation():
    print("🧪 Testando script atualizar.py (Protocolo v2.1)...")
    
    # 1. Criar arquivo original para teste
    with open("dummy.txt", "w", encoding="utf-8") as f: 
        f.write("Versao Antiga\n")
    
    # 2. Criar resposta.txt simulado com o novo protocolo
    with open("resposta.txt", "w", encoding="utf-8") as f:
        f.write("Olá! Aqui está o teste do novo protocolo.\n\n")
        f.write("[[MESAFLOW_BEGIN:dummy.txt]]\n")
        f.write("```text\nVersao Nova\n```\n")
        f.write("[[MESAFLOW_END]]\n")

    print("ℹ️  O script atualizar.py será executado.")
    print("ℹ️  O VS Code abrirá o Diff. Feche a aba do Diff e digite 's' no terminal.")
    
    try:
        import atualizar
        atualizar.process_updates()
    except Exception as e:
        print(f"❌ Erro ao executar o script: {e}")
        return

    # 3. Validar resultados
    print("\n--- Verificando Resultados ---")
    
    if os.path.exists("Copy/dummy.txt"):
        print("✅ Backup criado em Copy/dummy.txt")
    
    if os.path.exists("dummy.txt"):
        with open("dummy.txt", "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content == "Versao Nova":
                print("✅ Arquivo dummy.txt atualizado com sucesso!")
            else:
                print(f"❌ Falha: O conteúdo é '{content}' em vez de 'Versao Nova'")
    
    if os.path.exists("atualizar.log"):
        print("✅ Log de ação registrado em atualizar.log")

if __name__ == "__main__":
    test_automation()