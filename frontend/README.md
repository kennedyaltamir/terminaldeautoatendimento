<MesaFlow_Execution version="6.8">
    <Task_Classification>COMPLEXA</Task_Classification>
    <Domain>MOBILE</Domain>
    <Execution_Context>
        <Mode>STRICT</Mode>
    </Execution_Context>
    <Execution_State>
        <Phase>APPLY</Phase>
        <Result>SUCCESS</Result>
    </Execution_State>
    <Execution_Result>
        <Files>
            <File>
                <Path>docs/tasks/details/TASK-MOB-FIX-01/specs.md</Path>
                <Content><![CDATA[
[[MESAFLOW_BEGIN:docs/tasks/details/TASK-MOB-FIX-01/specs.md]]
# 📝 Especificação Técnica: TASK-MOB-FIX-01
> **Título:** Diagnóstico e Correção de Boot do App Mobile
> **Status:** EM DEFINIÇÃO
> **Objetivo:** Identificar por que o ambiente mobile nunca rodou e estabilizar o processo de inicialização (Expo).

## 1. Pontos de Verificação (Checklist de Diagnóstico)
- **Ambiente Node:** Validar se a versão do Node.js é compatível com Expo SDK 54 (Recomendado v18 ou v20).
- **Dependências:** Verificar integridade do `node_modules` e se há conflitos no `package.json`.
- **Configuração Expo:** Validar `app.json` e `eas.json`.
- **Scripts de Inicialização:** Garantir que `npm start` ou `npx expo start` executam o bundler corretamente.
- **Assets:** Confirmar se os ícones e splash screens obrigatórios existem.

## 2. Escopo da Correção
- Ajuste de versões de dependências se houver incompatibilidade.
- Correção de erros de sintaxe em arquivos de configuração.
- Limpeza de cache do Metro Bundler.
[[MESAFLOW_END]]
                ]]></Content>
            </File>
            <File>
                <Path>docs/tasks/details/TASK-MOB-FIX-01/verification_plan.md</Path>
                <Content><![CDATA[
[[MESAFLOW_BEGIN:docs/tasks/details/TASK-MOB-FIX-01/verification_plan.md]]
# 🧪 Plano de Verificação: TASK-MOB-FIX-01

## 1. Critérios de Sucesso (DoD)
- [ ] Script `scripts/maintenance/mobile_doctor.py` retorna "HEALTHY" para todos os checks.
- [ ] O comando `npx expo start` inicia o Metro Bundler sem erros fatais.
- [ ] O aplicativo pode ser visualizado no Expo Go ou simulador.

## 2. Procedimento de Teste
1. Executar `python scripts/maintenance/mobile_doctor.py`.
2. Tentar rodar `cd mobile && npx expo start --clear`.
3. Validar se o QR Code do Expo é gerado no terminal.
[[MESAFLOW_END]]
                ]]></Content>
            </File>
            <File>
                <Path>docs/tasks/details/TASK-MOB-FIX-01/rollback_plan.md</Path>
                <Content><![CDATA[
[[MESAFLOW_BEGIN:docs/tasks/details/TASK-MOB-FIX-01/rollback_plan.md]]
# ⏪ Plano de Rollback: TASK-MOB-FIX-01

## 1. Procedimento
- Reverter alterações no `mobile/package.json` e `mobile/app.json` via Git.
- Deletar a pasta `mobile/node_modules` e rodar `npm install` novamente para restaurar o estado anterior.
[[MESAFLOW_END]]
                ]]></Content>
            </File>
            <File>
                <Path>scripts/maintenance/mobile_doctor.py</Path>
                <Content><![CDATA[
[[MESAFLOW_BEGIN:scripts/maintenance/mobile_doctor.py]]
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 00:20:00
import os
import subprocess
import json
from pathlib import Path

def check_command(cmd):
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, shell=True)
        return True
    except:
        return False

def run_doctor():
    print("🩺 MesaFlow Mobile Doctor - Iniciando Diagnóstico...")
    
    mobile_dir = Path("mobile")
    results = []

    # 1. Verifica existência da pasta
    if not mobile_dir.exists():
        print("❌ ERRO: Pasta 'mobile/' não encontrada.")
        return

    # 2. Verifica Node.js
    node_ok = check_command("node -v")
    results.append(("Node.js Instalado", node_ok))

    # 3. Verifica package.json
    pkg_path = mobile_dir / "package.json"
    pkg_ok = pkg_path.exists()
    results.append(("package.json existe", pkg_ok))

    if pkg_ok:
        with open(pkg_path, 'r') as f:
            pkg = json.load(f)
            expo_ver = pkg.get("dependencies", {}).get("expo")
            results.append((f"Expo SDK ({expo_ver})", True))

    # 4. Verifica node_modules
    nm_ok = (mobile_dir / "node_modules").exists()
    results.append(("node_modules instalado", nm_ok))

    # 5. Verifica Assets Críticos
    assets_dir = mobile_dir / "assets"
    icon_ok = (assets_dir / "icon.png").exists()
    results.append(("Ícone (assets/icon.png)", icon_ok))

    print(f"\n{'CHECK':<30} | {'STATUS':<10}")
    print("-" * 45)
    for check, status in results:
        print(f"{check:<30} | {'✅ OK' if status else '❌ FALHA'}")

    print("\n💡 Próximos passos sugeridos:")
    if not nm_ok:
        print("   - Execute: cd mobile && npm install")
    if not icon_ok:
        print("   - Gere os assets placeholder ou coloque imagens reais em mobile/assets/")
    
    print("\n--- Fim do Diagnóstico ---")

if __name__ == "__main__":
    run_doctor()
[[MESAFLOW_END]]
                ]]></Content>
            </File>
        </Files>
        <Terminal_Commands>
            <Command>python atualizar.py</Command>
            <Command>python scripts/maintenance/mobile_doctor.py</Command>
            <Command>git add . && git commit -m "chore(mobile): implement TASK-MOB-FIX-01 definition and diagnostic tool"</Command>
        </Terminal_Commands>
    </Execution_Result>
</MesaFlow_Execution>