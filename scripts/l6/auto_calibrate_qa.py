
import subprocess
import re
import sys
import xml.etree.ElementTree as ET

def get_element_bounds(text):
    """Busca as coordenadas de um elemento pelo texto no dump atual da tela."""
    subprocess.run("adb shell uiautomator dump /sdcard/ui.xml", shell=True, stdout=subprocess.DEVNULL)
    subprocess.run("adb pull /sdcard/ui.xml ui_dump.xml", shell=True, stdout=subprocess.DEVNULL)
    
    try:
        tree = ET.parse("ui_dump.xml")
        root = tree.getroot()
        
        for node in root.iter("node"):
            if text in node.attrib.get("text", "") or text in node.attrib.get("content-desc", ""):
                bounds = node.attrib.get("bounds") # "[x1,y1][x2,y2]"
                coords = re.findall(r'\d+', bounds)
                if coords:
                    x1, y1, x2, y2 = map(int, coords)
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    return center_x, center_y
        return None
    except Exception as e:
        print(f"Erro ao parsear XML: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python auto_calibrate_qa.py 'Texto do Botão'")
        sys.exit(1)
    
    target = sys.argv[1]
    coords = get_element_bounds(target)
    if coords:
        print(f"📍 Coordenadas para '{target}': {coords[0]}, {coords[1]}")
    else:
        print(f"❌ Elemento '{target}' não encontrado na tela atual.")

