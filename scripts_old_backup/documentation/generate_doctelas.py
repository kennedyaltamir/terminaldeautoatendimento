# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-16 05:30:00
import json
import os
from pathlib import Path
from datetime import datetime

# Configuração de Caminhos
ROOT_DIR = Path("doctelas")
WEB_DIR = ROOT_DIR / "web"
MOBILE_DIR = ROOT_DIR / "mobile"
INVENTORY_FILE = Path("docs/audit/ui_inventory.json")

# Base de Conhecimento Enriquecida (Descriptions & Insights)
# Mapeia o 'tela' (nome) ou 'rota' para descrições humanas.
ENRICHMENT_DB = {
    "LandingPage": {
        "purpose": "Porta de entrada comercial. Converte visitantes em leads ou contas de teste (PLG).",
        "observations": "Performance (LCP) crítica para SEO. Imagens devem usar next/image com priority."
    },
    "DashboardPage": {
        "purpose": "Visão tática da operação. Decisões baseadas em dados em tempo real.",
        "observations": "Dados pesados devem ser carregados via Promise.all. Cache de SWR/React Query recomendado."
    },
    "KitchenPage": {
        "purpose": "Orquestração de produção (KDS). Substitui impressoras de cozinha.",
        "observations": "Deve manter estado local se a rede cair. Contraste alto para leitura à distância."
    },
    "CounterPage": {
        "purpose": "Ponto de venda (PDV) para operação de caixa rápida.",
        "observations": "Foco em acessibilidade por teclado (F2, Enter, Esc)."
    },
    "LoginScreen": {
        "purpose": "Autenticação segura e persistente no dispositivo.",
        "observations": "Validação semântica do JWT obrigatória antes de navegar."
    },
    "WaiterDashboard": {
        "purpose": "Gestão de salão em movimento para garçons.",
        "observations": "Deve permitir abertura de mesa offline. Sincronia eventual."
    },
    "DriverDashboard": {
        "purpose": "Gestão de entregas para motoboys próprios.",
        "observations": "Envio de telemetria deve ser throttled (3s) para bateria."
    }
}

def load_inventory():
    if not INVENTORY_FILE.exists():
        print(f"❌ Inventário não encontrado: {INVENTORY_FILE}")
        return None
    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erro ao ler JSON: {e}")
        return None

def get_enrichment(name, route):
    # Tenta casar por nome exato ou substrings da rota
    if name in ENRICHMENT_DB:
        return ENRICHMENT_DB[name]
    
    # Heurísticas de fallback
    if "login" in route.lower():
        return {"purpose": "Autenticação de usuário.", "observations": "Verificar persistência de sessão."}
    if "register" in route.lower():
        return {"purpose": "Cadastro de novos usuários/tenants.", "observations": "Validar inputs em tempo real."}
    if "settings" in route.lower():
        return {"purpose": "Configurações do sistema.", "observations": "Alterações sensíveis devem exigir confirmação."}
    
    return {
        "purpose": "Funcionalidade específica do sistema.",
        "observations": "Nenhuma observação crítica registrada automaticamente."
    }

def generate_markdown_content(screen, platform):
    name = screen.get("tela", "Unknown")
    route = screen.get("rota", "N/A")
    layout = screen.get("layout", [])
    elements = screen.get("elementos", [])
    flows = screen.get("fluxo", [])
    states = screen.get("estados_detectados", []) or screen.get("estados_codigo", [])
    
    info = get_enrichment(name, route)
    
    # Formatação de Elementos
    elements_list = []
    if elements:
        for el in elements:
            tipo = el.get("tipo", "Elemento").upper()
            nome = el.get("nome", "N/A")
            acao = el.get("acao", "-")
            validacao = el.get("validacao", "")
            val_str = f" ({validacao})" if validacao and validacao != "none" else ""
            elements_list.append(f"- **{tipo}**: {nome} — *Ação: {acao}*{val_str}")
    else:
        elements_list.append("- *Nenhum elemento interativo detectado.*")

    # Formatação de Fluxos
    flows_list = [f"1. {f}" for f in flows] if flows else ["- Navegação padrão."]

    content = f"""# 📱 {name}
> **Plataforma:** {platform}
> **Rota:** `{route}`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
{info['purpose']}

## 2. Estrutura e Layout
**Containers:** {', '.join(layout) if layout else 'Padrão'}

## 3. Elementos Interativos
{chr(10).join(elements_list)}

## 4. Estados e Comportamentos
**Estados Detectados:** {', '.join(states) if states else 'Padrão'}

## 5. Fluxos de Navegação
{chr(10).join(flows_list)}

## 6. Observações Críticas
{info['observations']}

---
*Gerado automaticamente em {datetime.now().isoformat()}*
"""
    return content

def main():
    print("📚 Gerando Documentação Completa de Telas (Doctelas)...")
    data = load_inventory()
    if not data: return

    WEB_DIR.mkdir(parents=True, exist_ok=True)
    MOBILE_DIR.mkdir(parents=True, exist_ok=True)

    generated_files = {"web": [], "mobile": []}

    # Processar Web
    print("   🌐 Processando Web...")
    for screen in data.get("web", []):
        content = generate_markdown_content(screen, "WEB")
        filename = f"{screen.get('tela', 'unknown').replace(' ', '')}.md"
        with open(WEB_DIR / filename, "w", encoding="utf-8") as f:
            f.write(content)
        generated_files["web"].append(filename)

    # Processar Mobile
    print("   📱 Processando Mobile...")
    for screen in data.get("mobile", []):
        content = generate_markdown_content(screen, "MOBILE")
        filename = f"{screen.get('tela', 'unknown').replace(' ', '')}.md"
        with open(MOBILE_DIR / filename, "w", encoding="utf-8") as f:
            f.write(content)
        generated_files["mobile"].append(filename)

    # Atualizar README
    readme_content = f"""# 📱 Documentação de Telas - MesaFlow OS

Este diretório contém a documentação funcional detalhada de todas as telas do sistema, gerada automaticamente a partir do inventário de UI.

## 📊 Estatísticas
- **Web:** {len(generated_files['web'])} telas documentadas.
- **Mobile:** {len(generated_files['mobile'])} telas documentadas.
- **Última Atualização:** {datetime.now().isoformat()}

## 📂 Índice Web
{chr(10).join([f"- [{f}](./web/{f})" for f in sorted(generated_files['web'])])}

## 📂 Índice Mobile
{chr(10).join([f"- [{f}](./mobile/{f})" for f in sorted(generated_files['mobile'])])}

---
*MesaFlow Kernel L6*
"""
    with open(ROOT_DIR / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"✅ Sucesso! {len(generated_files['web']) + len(generated_files['mobile'])} documentos gerados em /doctelas.")

if __name__ == "__main__":
    main()

