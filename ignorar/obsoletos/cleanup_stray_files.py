import os

def cleanup():
    files_to_remove = ["path"]
    for f in files_to_remove:
        if os.path.exists(f):
            os.remove(f)
            print(f"✅ Arquivo resíduo '{f}' removido.")

if __name__ == "__main__":
    cleanup()
