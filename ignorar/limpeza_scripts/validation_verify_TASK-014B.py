import sys
import os
import subprocess
import json
import io

# Força UTF-8 no Windows para evitar UnicodeDecodeError
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def verify():
    print("🔍 Verificando TASK-014B: AuthGate Boundary...")
    
    # 1. Verificação de Existência de Arquivos
    required_files = [
        "mobile/src/navigation/AuthGate.tsx",
        "mobile/src/navigation/RootNavigator.tsx",
        "mobile/src/navigation/__tests__/AuthGate.test.tsx",
        "mobile/package.json"
    ]
    
    for f_path in required_files:
        if not os.path.exists(f_path):
            print(f"❌ Arquivo faltando: {f_path}")
            sys.exit(1)
        print(f"✅ Arquivo encontrado: {f_path}")

    # 2. Verificação de Conteúdo (Lógica Implementada)
    with open("mobile/src/navigation/AuthGate.tsx", "r", encoding="utf-8") as f:
        content = f.read()
        if "useAuthStore" not in content:
            print("❌ AuthGate não está conectado à Store.")
            sys.exit(1)
        if "return null" not in content:
            print("❌ AuthGate não implementa retorno nulo para estados de transição.")
            sys.exit(1)

    with open("mobile/src/navigation/RootNavigator.tsx", "r", encoding="utf-8") as f:
        content = f.read()
        if "<AuthGate />" not in content:
            print("❌ RootNavigator não está renderizando o AuthGate.")
            sys.exit(1)
        if "AppStack" in content or "AuthStack" in content:
            print("❌ VIOLAÇÃO: RootNavigator ainda importa Stacks diretamente.")
            sys.exit(1)

    # 2.1 Verificação do package.json (Script de teste)
    try:
        with open("mobile/package.json", "r", encoding="utf-8") as f:
            pkg = json.load(f)
            if "test" not in pkg.get("scripts", {}):
                print("❌ Script 'test' não encontrado no mobile/package.json")
                sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao ler mobile/package.json: {e}")
        sys.exit(1)

    # 3. Execução dos Testes Automatizados (Jest)
    print("🧪 Executando testes unitários (Jest)...")
    
    target_dir = os.path.abspath("mobile")
    os.chdir(target_dir)
    print(f"   📂 Diretório de execução: {os.getcwd()}")

    try:
        # Adiciona encoding='utf-8' e errors='replace' para evitar crash no Windows
        result = subprocess.run(
            ["npm", "run", "test", "--", "src/navigation/__tests__/AuthGate.test.tsx", "--runInBand"],
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        print("✅ Testes Unitários: PASSOU")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("❌ Testes Unitários: FALHOU")
        print("--- STDOUT ---")
        print(e.stdout)
        print("--- STDERR ---")
        print(e.stderr)
        sys.exit(1)

    print("\n🏆 TASK-014B: VALIDAÇÃO CONCLUÍDA COM SUCESSO.")
    sys.exit(0)

if __name__ == "__main__":
    verify()
