# DOMAIN: DEVOPS_SCRIPTS
import sys
import os

def verify():
    print("🔍 Verificando TASK-UX-01: Voice Ordering Interface (KDS)...")

    # 1. Verificar Hook
    hook_path = "frontend/src/hooks/useVoiceControl.ts"
    if not os.path.exists(hook_path):
        print(f"❌ Hook não encontrado: {hook_path}")
        sys.exit(1)

    with open(hook_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "SpeechRecognition" not in content:
            print("❌ Hook não utiliza SpeechRecognition API.")
            sys.exit(1)
        if "processCommand" not in content:
            print("❌ Lógica de processamento de comando ausente.")
            sys.exit(1)

    # 2. Verificar Integração na Página
    page_path = "frontend/src/app/admin/[slug]/kitchen/page.tsx"
    if not os.path.exists(page_path):
        print(f"❌ Página KDS não encontrada: {page_path}")
        sys.exit(1)

    with open(page_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "useVoiceControl" not in content:
            print("❌ Hook de voz não importado na página KDS.")
            sys.exit(1)
        if "voiceCommands" not in content:
            print("❌ Comandos de voz não definidos na página.")
            sys.exit(1)
        if "Mic" not in content:
            print("❌ Ícone de microfone não encontrado na UI.")
            sys.exit(1)

    print("\n🏆 TASK-UX-01: VALIDAÇÃO ESTRUTURAL CONCLUÍDA.")
    print("   Nota: O teste funcional requer um navegador com microfone real.")
    sys.exit(0)

if __name__ == "__main__":
    verify()
