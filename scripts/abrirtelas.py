import webbrowser
import json
from pathlib import Path

# Caminho para o inventário gerado
INVENTORY_FILE = Path("docs/audit/ui_inventory.json")

with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

WEB_BASE_URL = "http://localhost:3000"

for screen in data["web"]:
    url = WEB_BASE_URL + screen["rota"]
    print(f"Abrindo {screen['tela']} -> {url}")
    webbrowser.open(url)
