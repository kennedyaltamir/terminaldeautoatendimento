import os
import sys

# [TEST_EXEMPT: Script de auditoria de integridade para a Missão 33]

def verify():
    print("🔍 Iniciando Auditoria de Pagamentos Nativos (Missão 33)...")

    checks = [
        ("mobile/package.json", "react-native-qrcode-svg"),
        ("mobile/src/store/waiter.store.ts", "paymentData: PaymentData"),
        ("mobile/src/store/waiter.store.ts", "initiatePayment:"),
        ("mobile/src/screens/waiter/PaymentScreen.tsx", "QRCode"),
        ("mobile/src/navigation/stacks/AppStack.tsx", "Payment")
    ]

    errors = 0
    for path, content in checks:
        if not os.path.exists(path):
            print(f"❌ Arquivo ausente: {path}")
            errors += 1
            continue

        with open(path, "r", encoding="utf-8") as f:
            if content not in f.read():
                print(f"❌ VIOLAÇÃO: Lógica '{content}' não encontrada em {path}")
                errors += 1
            else:
                print(f"✅ {path} validado.")

    print("\n" + "="*50)
    if errors == 0:
        print("✨ SUCESSO: A infraestrutura de pagamentos nativos está pronta.")
        sys.exit(0)
    else:
        print(f"🚨 ALERTA: {errors} inconsistência(s) encontrada(s).")
        sys.exit(1)

if __name__ == "__main__":
    verify()
