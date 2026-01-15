import re
from pathlib import Path

FILES = [
    "frontend/src/app/admin/[slug]/dashboard/history/page.tsx",
    "frontend/src/app/admin/[slug]/history/page.tsx",
    "frontend/src/app/[slug]/menu/MenuClient.tsx"
]

def inspect():
    print("🔍 Inspecting UI Issues...")
    for file_path in FILES:
        path = Path(file_path)
        if not path.exists():
            print(f"❌ File not found: {file_path}")
            continue
            
        print(f"\n📄 Analyzing: {file_path}")
        content = path.read_text(encoding="utf-8")
        
        # Find buttons
        for match in re.finditer(r'<button(.*?)>', content, re.DOTALL):
            attrs = match.group(1)
            has_click = "onClick" in attrs
            has_submit = 'type="submit"' in attrs or "type='submit'" in attrs
            has_form_action = "formAction" in attrs
            
            if not (has_click or has_submit or has_form_action):
                # Calculate line number
                start_pos = match.start()
                line_num = content[:start_pos].count('\n') + 1
                print(f"   ⚠️  Line {line_num}: Button missing action")
                # Clean up newlines for display
                clean_context = match.group(0).replace('\n', ' ').replace('\r', '')
                print(f"      Context: {clean_context[:100]}...")

if __name__ == "__main__":
    inspect()
