import os
import re

def fix_layout_imports():
    print("🔧 [1/5] Corrigindo imports em layout.tsx...")
    file_path = "frontend/src/app/admin/[slug]/layout.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado: {file_path}")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Verifica se ChefHat é usado mas não importado
        if "icon: ChefHat" in content and "ChefHat," not in content and ", ChefHat" not in content and "{ ChefHat }" not in content:
            print("   🔍 'ChefHat' faltando nos imports. Corrigindo...")
            # Regex para encontrar o import do lucide-react e adicionar ChefHat
            pattern = r'(import\s*{[^}]*)(\}\s*from\s*"lucide-react")'
            if re.search(pattern, content):
                new_content = re.sub(pattern, r'\1, ChefHat \2', content)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print("   ✅ Import corrigido.")
            else:
                print("   ❌ Não foi possível localizar o import do lucide-react.")
        else:
            print("   ✅ Imports parecem corretos.")

    except Exception as e:
        print(f"   ❌ Erro ao processar arquivo: {e}")

def check_google_env():
    print("\n🔧 [2/5] Verificando variável Google Client ID...")
    env_path = ".env"
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "NEXT_PUBLIC_GOOGLE_CLIENT_ID" not in content:
                print("   ⚠️ Variável NEXT_PUBLIC_GOOGLE_CLIENT_ID não encontrada.")
                # Opcional: Adicionar mock se não existir
                # with open(env_path, "a", encoding="utf-8") as f:
                #     f.write("\nNEXT_PUBLIC_GOOGLE_CLIENT_ID=mock_id\n")
                # print("   ✅ Mock adicionado.")
            else:
                print("   ✅ Variável encontrada.")
    else:
        print("   ❌ Arquivo .env não encontrado.")

def fix_session_fetch_logic():
    print("\n🔧 [3/5] Verificando lógica de fetch de sessão (undefined)...")
    # Procurar onde a chamada para /session/ é feita no frontend
    # Provavelmente em MenuClient.tsx ou similar
    target_file = "frontend/src/app/[slug]/menu/MenuClient.tsx"
    
    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Procurar por getTableSession(slug, sessionToken) ou similar
        # E verificar se tem check de undefined
        
        # Exemplo de correção simples (regex pode ser complexo aqui, vamos fazer uma busca simples)
        if "getTableSession(slug, statusData.session_token)" in content:
             print("   🔍 Chamada de sessão encontrada. Verificando proteção...")
             # A lógica já parece ter um if (statusData.session_token), mas o log mostrou undefined.
             # Pode ser que statusData.session_token esteja vindo undefined mas entrando no if?
             # Ou a chamada é feita em outro lugar.
             pass
        
        # O erro específico foi: GET /api/hamburgueria-ze/session/undefined
        # Isso sugere que uma variável interpolada resultou em "undefined".
        # Vamos procurar por `${sessionToken}` ou similar.
        
        # Correção preventiva: Adicionar verificação explicita antes de chamadas de API que usam tokens
        # Isso é complexo de fazer via script regex sem contexto total, mas vamos tentar identificar o ponto.
        
        print("   ℹ️  Recomendação: Verificar manualmente 'frontend/src/app/[slug]/menu/MenuClient.tsx' para garantir que 'sessionToken' não seja undefined antes de chamar 'getTableSession'.")

    else:
        print(f"   ⚠️ Arquivo {target_file} não encontrado.")

def check_employee_payload_schema():
    print("\n🔧 [4/5] Verificando Schema de Employee (Erro 422)...")
    schema_path = "app/schemas.py"
    if os.path.exists(schema_path):
        with open(schema_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "class EmployeeCreate" in content:
                print("   ✅ Schema EmployeeCreate encontrado no backend.")
                # Poderíamos imprimir os campos obrigatórios para conferência
            else:
                print("   ❌ Schema EmployeeCreate não encontrado.")
    else:
        print("   ❌ Arquivo schemas.py não encontrado.")

def summary():
    print("\n📋 [5/5] Resumo")
    print("   As correções automáticas foram aplicadas onde possível.")
    print("   Para os erros de lógica (404/422), verifique os pontos indicados acima.")

if __name__ == "__main__":
    fix_layout_imports()
    check_google_env()
    fix_session_fetch_logic()
    check_employee_payload_schema()
    summary()
