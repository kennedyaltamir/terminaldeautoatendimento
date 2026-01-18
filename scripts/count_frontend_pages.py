# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 21:00:00
import os
from pathlib import Path

def count_pages():
    app_dir = Path("frontend/src/app")
    pages = []
    for root, dirs, files in os.walk(app_dir):
        if "page.tsx" in files:
            rel_path = os.path.relpath(root, app_dir)
            route = "/" + rel_path.replace("\\", "/")
            if route == "/.": route = "/"
            pages.append(route)
    
    print(f"📊 Total de páginas detectadas no Frontend: {len(pages)}")
    for p in sorted(pages):
        print(f"   - {p}")

if __name__ == "__main__":
    count_pages()

