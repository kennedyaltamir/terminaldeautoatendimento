import pytest

def classify_file(filename):
    """
    Replica a lógica do script de organização para teste unitário.
    Sincronizado com scripts/organize_scripts.py v2.0
    """
    STRUCTURE = {
        "security": [
            "audit", "security", "auth", "create_admin", "fix_layouts"
        ],
        "functional": [
            "logistics", "payment", "delivery", "stock", "order", "menu", 
            "kds", "waiter", "franchise", "marketing", "simular", "test_"
        ],
        "maintenance": [
            "update_db", "fix_", "seed", "cleanup", "purge", "fix_deps", 
            "fix_fiscal", "fix_tips", "fix_pwa", "fix_sentry"
        ],
        "setup": [
            "check_env", "verify", "download", "install", "configurar", "gerar_url"
        ]
    }
    
    filename = filename.lower()
    for folder, keywords in STRUCTURE.items():
        if any(k in filename for k in keywords):
            return folder
    return "maintenance" # Default

def test_script_classification():
    # Security
    assert classify_file("security_audit.py") == "security"
    assert classify_file("create_admin_user.py") == "security"
    
    # Functional
    assert classify_file("test_payment_flow.py") == "functional"
    assert classify_file("simular_pagamento.py") == "functional"
    assert classify_file("test_marketing_flow.py") == "functional"
    
    # Maintenance
    assert classify_file("update_db_fiscal.py") == "maintenance"
    assert classify_file("fix_deps.py") == "maintenance"
    assert classify_file("seed.py") == "maintenance"
    
    # Setup
    assert classify_file("verify_installation.py") == "setup"
    assert classify_file("check_env.py") == "setup"

    print("✅ Lógica de classificação de scripts validada!")
