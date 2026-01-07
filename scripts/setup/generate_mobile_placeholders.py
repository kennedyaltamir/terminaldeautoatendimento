import os
import base64

# [TEST_EXEMPT: Script de utilidade para geração de assets técnicos]

def generate():
    """
    Gera assets PNG válidos de 1x1 pixel usando Base64 verificado.
    Isso evita erros de CRC (Cyclic Redundancy Check) no processador Jimp do Expo.
    """
    assets_dir = "mobile/assets"
    os.makedirs(assets_dir, exist_ok=True)

    # Base64 de um PNG transparente de 1x1 pixel válido
    valid_png_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    png_data = base64.b64decode(valid_png_b64)

    files = ["icon.png", "splash.png", "adaptive-icon.png", "favicon.png"]

    print(f"🛠️  Reparando assets técnicos em {assets_dir}...")

    for file_name in files:
        file_path = os.path.join(assets_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(png_data)
        print(f"✅ Gerado com sucesso: {file_name}")

    print("\n✨ Assets corrigidos. O erro de CRC deve desaparecer.")

if __name__ == "__main__":
    generate()
