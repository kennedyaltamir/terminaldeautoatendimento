
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 09:15:00
import os
import time

PACKAGE = "com.mesaflow.mobile"
# Activity padrão para Expo Managed Workflow
ACTIVITY = "com.mesaflow.mobile.MainActivity"

def sweep():
    print("🔍 Iniciando UI Sweep v2.0 (MesaFlow Mobile)...")
    # Mapeamento de Telas para Deep Links
    screens = {
        "Login": "mesaflow://Login",
        "WaiterHome": "mesaflow://WaiterHome",
        "Kitchen": "mesaflow://KitchenDashboard",
        "Driver": "mesaflow://DriverDashboard"
    }
    
    for name, url in screens.items():
        print(f"📺 Forçando render da tela: {name}")
        # Tenta via Deep Link
        res = os.popen(f"adb shell am start -a android.intent.action.VIEW -d '{url}' {PACKAGE}").read()
        
        if "Error" in res:
            print(f"⚠️ Deep Link falhou para {name}. Tentando via Activity Manager...")
            os.system(f"adb shell am start -n {PACKAGE}/{ACTIVITY}")
            time.sleep(2)
        
        time.sleep(3)
        output_path = f"docs/mobile/reports/sweep_{name}.png"
        os.system(f"adb shell screencap -p /sdcard/sweep.png")
        os.system(f"adb pull /sdcard/sweep.png {output_path}")
        print(f"📸 Screenshot salva: {output_path}")
    
    print("✅ Sweep concluído.")

if __name__ == "__main__":
    sweep()

