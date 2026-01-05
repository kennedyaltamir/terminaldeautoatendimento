import os
import sys
import re
import argparse
import datetime
import fnmatch
import json
import time
import asyncio
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Set, Tuple

# Dependências Profissionais
try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.panel import Panel
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False

try:
    import pyperclip
    HAS_CLIPBOARD = True
except ImportError:
    HAS_CLIPBOARD = False

try:
    from playwright.async_api import async_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

# ============================================================
# CONFIGURAÇÃO (V7.1 - Flat Handover Edition)
# ============================================================

HANDOVER_DIR = "HANDOVER_MESAFLOW"
MAX_FILE_SIZE = 500 * 1024  # 500KB
TOKEN_LIMIT = 450000 

BASE_URL = "http://localhost:3000"
SLUG = "hamburgueria-ze"
ADMIN_EMAIL = "admin@mesaflow.com"
ADMIN_PASS = "123456"

PRIORITY_FILES = [
    "app/models.py", "app/schemas.py", "app/database.py", 
    "app/main.py", "frontend/src/types/index.ts", "docs/ROADMAP.md"
]

IGNORAR_EXTENSOES = {
    ".pyc", ".pyo", ".pyd", ".db", ".sqlite", ".sqlite3", 
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", 
    ".woff", ".woff2", ".ttf", ".eot", ".mp3", ".wav", 
    ".mp4", ".pdf", ".zip", ".tar", ".gz", ".rar", ".7z", 
    ".exe", ".dll", ".so", ".log", ".bak", ".tag", ".lock"
}

IGNORAR_PASTAS = {
    ".git", "node_modules", ".next", "__pycache__", "venv", ".venv", 
    "Copy", ".temp_diff", "dist", "build", ".vscode", "screenshots",
    "output_sounds", "assets", "public/uploads", HANDOVER_DIR
}

SECRET_PATTERNS = {
    "Stripe_Key": r"sk_(?:live|test)_[0-9a-zA-Z]{24,}",
    "MercadoPago_Token": r"APP_USR-[0-9]{16}-[0-9]{6}-[a-z0-9]{32}-[0-9]{9,}",
    "JWT_Secret": r"SECRET_KEY\s*=\s*['\"][a-zA-Z0-9_\-]{32,}['\"]",
}

# ============================================================
# MOTOR DE INTELIGÊNCIA
# ============================================================

class ProjectIntelligence:
    def __init__(self):
        self.import_map = {}
        self.component_props = {}
        self.all_files = set()
        self.referenced_files = set()
        self.latency_report = {}

    def analyze(self, path: str, content: str):
        self.all_files.add(path)
        imports = re.findall(r"(?:import|from)\s+['\"]?([@\w./-]+)", content)
        if imports:
            self.import_map[path] = imports
            for imp in imports:
                clean_name = imp.split('/')[-1].split('.')[0]
                self.referenced_files.add(clean_name)

        if path.endswith(('.tsx', '.jsx')):
            props = re.findall(r"interface\s+(\w+Props)\s*{([^}]*)}", content)
            if props:
                self.component_props[path] = props

    def get_dead_code(self) -> List[str]:
        dead = []
        for f in self.all_files:
            name = Path(f).stem
            if name not in self.referenced_files and "page" not in name and "layout" not in name and "main" not in name and "init" not in name:
                if f.endswith(('.py', '.ts', '.tsx')):
                    dead.append(f)
        return dead

# ============================================================
# MOTOR VISUAL PARALELO (FLAT OUTPUT)
# ============================================================

async def capture_screen(browser, storage_state, url, name, category, intel, semaphore):
    async with semaphore:
        start = time.time()
        # Injeta o estado de login (cookies/localStorage) em cada contexto
        context = await browser.new_context(
            storage_state=storage_state,
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()
        try:
            await page.goto(url, wait_until="networkidle", timeout=20000)
            
            # Se for a página de configurações, tenta clicar nas abas se o nome for específico
            if "settings" in url and "_" in name:
                tab_label = name.split("_")[-1]
                try:
                    await page.get_by_role("button").filter(has_text=tab_label).first.click()
                    await page.wait_for_load_state("networkidle")
                    await asyncio.sleep(1)
                except: pass

            intel.latency_report[name] = f"{time.time() - start:.2f}s"
            filename = f"IMG_{category}_{name}.webp"
            full_path = Path(HANDOVER_DIR) / filename
            await page.screenshot(path=str(full_path), type="webp", quality=50, full_page=True)
            print(f"   ✅ Capturado: {category}/{name}")
            return True
        except Exception as e:
            print(f"   ❌ Erro ao capturar {name}: {str(e)[:50]}")
            return False
        finally:
            await context.close()

async def run_visual_audit(intel):
    if not HAS_PLAYWRIGHT: return
    print("\n[bold cyan]⚡ Iniciando Auditoria Visual (Flat Mode)...[/bold cyan]")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Realizar Login e Capturar Estado
        print("   🔑 Autenticando para capturas protegidas...")
        login_context = await browser.new_context()
        login_page = await login_context.new_page()
        await login_page.goto(f"{BASE_URL}/admin/login")
        await login_page.fill('input[name="email"]', ADMIN_EMAIL)
        await login_page.fill('input[name="password"]', ADMIN_PASS)
        await login_page.click('button[type="submit"]')
        await login_page.wait_for_url("**/dashboard", timeout=15000)
        await login_page.evaluate("localStorage.setItem('mesaflow_tour_completed', 'true')")
        
        # Salva cookies e localStorage
        storage = await login_context.storage_state()
        await login_context.close()

        # 2. Disparar Capturas Paralelas
        semaphore = asyncio.Semaphore(3)
        tasks = [
            capture_screen(browser, storage, BASE_URL, "Home", "Public", intel, semaphore),
            capture_screen(browser, storage, f"{BASE_URL}/admin/{SLUG}/dashboard", "Dashboard", "Admin", intel, semaphore),
            capture_screen(browser, storage, f"{BASE_URL}/admin/{SLUG}/menu", "Cardapio", "Admin", intel, semaphore),
            capture_screen(browser, storage, f"{BASE_URL}/admin/{SLUG}/inventory", "Estoque", "Admin", intel, semaphore),
            capture_screen(browser, storage, f"{BASE_URL}/admin/{SLUG}/settings", "Config_Geral", "Settings", intel, semaphore),
            capture_screen(browser, storage, f"{BASE_URL}/admin/{SLUG}/settings", "Config_Fiscal", "Settings", intel, semaphore),
            capture_screen(browser, storage, f"{BASE_URL}/admin/{SLUG}/kitchen", "KDS", "Operations", intel, semaphore),
            capture_screen(browser, storage, f"{BASE_URL}/{SLUG}/menu", "Menu_Mobile", "Mobile", intel, semaphore),
        ]
        
        await asyncio.gather(*tasks)
        await browser.close()

# ============================================================
# CORE DE PROCESSAMENTO
# ============================================================

def redact(content: str) -> str:
    for name, pattern in SECRET_PATTERNS.items():
        content = re.sub(pattern, f"[REDACTED_{name.upper()}]", content)
    return content

def generate_tree(startpath: str) -> str:
    tree = ["📂 Estrutura do Projeto:\n.\n"]
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in IGNORAR_PASTAS]
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * level
        if root != startpath: tree.append(f"{indent}├── {os.path.basename(root)}/\n")
        subindent = '│   ' * (level + 1)
        for f in files:
            if os.path.splitext(f)[1].lower() not in IGNORAR_EXTENSOES:
                tree.append(f"{subindent}├── {f}\n")
    return "".join(tree)

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-img", action="store_true")
    args = parser.parse_args()

    # Preparar pasta de Handover
    if os.path.exists(HANDOVER_DIR):
        shutil.rmtree(HANDOVER_DIR)
    os.makedirs(HANDOVER_DIR)

    intel = ProjectIntelligence()
    if not args.no_img:
        await run_visual_audit(intel)

    output_buffer = [
        f"# MESAFLOW FLAT HANDOVER v7.1\n",
        f"# Generated: {datetime.datetime.now()}\n",
        generate_tree("."),
        "\n" + "="*50 + "\nCONTEÚDO DOS ARQUIVOS\n" + "="*50 + "\n"
    ]

    all_paths = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in IGNORAR_PASTAS]
        for f in files:
            path = os.path.join(root, f).replace("\\", "/")
            if os.path.splitext(f)[1].lower() in IGNORAR_EXTENSOES: continue
            if any(fnmatch.fnmatch(path, p) for p in ["*.log", "resposta.txt"]): continue
            all_paths.append(path)

    all_paths.sort(key=lambda x: (x not in PRIORITY_FILES, x))

    file_count = 0
    current_tokens = 0
    chunk_id = 0

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TaskProgressColumn()) as progress:
        task = progress.add_task("[cyan]Gerando Pacote Flat...", total=len(all_paths))
        
        for filepath in all_paths:
            try:
                if os.path.getsize(filepath) > MAX_FILE_SIZE: continue
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                intel.analyze(filepath, content)
                content = redact(content)
                content = re.sub(r'\n\s*\n', '\n\n', content)
                
                formatted = f"\n# FILE: {filepath}\n```{os.path.splitext(filepath)[1][1:] or 'txt'}\n{content}\n```\n"
                output_buffer.append(formatted)
                
                current_tokens += len(formatted) // 4
                file_count += 1
                progress.update(task, advance=1)

                if current_tokens > TOKEN_LIMIT:
                    chunk_id += 1
                    fname = f"CODE_part_{chunk_id}.txt"
                    with open(Path(HANDOVER_DIR) / fname, "w", encoding="utf-8") as f:
                        f.write("".join(output_buffer))
                    output_buffer = [f"# CONTINUAÇÃO PARTE {chunk_id+1}\n"]
                    current_tokens = 0
            except: pass

    # Salvar arquivo principal ou último chunk
    final_name = "CODE_todososarquivos.txt" if chunk_id == 0 else f"CODE_part_{chunk_id + 1}.txt"
    with open(Path(HANDOVER_DIR) / final_name, "w", encoding="utf-8") as f:
        f.write("".join(output_buffer))

    if HAS_RICH:
        table = Table(title="📦 Pacote de Handover Flat Pronto")
        table.add_column("Métrica", style="green")
        table.add_column("Resultado", style="bold white")
        table.add_row("Pasta de Saída", HANDOVER_DIR)
        table.add_row("Arquivos de Texto", str(chunk_id + 1))
        table.add_row("Imagens (Screenshots)", str(len(list(Path(HANDOVER_DIR).glob('*.webp')))))
        table.add_row("Código Morto Detectado", str(len(intel.get_dead_code())))
        console.print(table)
        console.print(f"\n[bold yellow]👉 Instrução: Abra a pasta '{HANDOVER_DIR}', selecione TUDO e arraste para a IA.[/bold yellow]")

if __name__ == "__main__":
    asyncio.run(main())
