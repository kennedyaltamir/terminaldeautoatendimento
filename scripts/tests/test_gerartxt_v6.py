import os
import pytest
from gerartxt import redact, ProjectIntelligence

def test_redact_secrets():
    content = "STRIPE_KEY = 'sk_live_123456789012345678901234'"
    redacted = redact(content)
    assert "REDACTED_STRIPE_KEY" in redacted
    assert "sk_live" not in redacted

def test_intelligence_props_extraction():
    intel = ProjectIntelligence()
    content = "interface ButtonProps { label: string; active: boolean; }"
    intel.analyze("Button.tsx", content)
    assert "Button.tsx" in intel.component_props
    assert "ButtonProps" in str(intel.component_props["Button.tsx"])

def test_dead_code_detection():
    intel = ProjectIntelligence()
    # Simula arquivos e referências
    # Teste de importação estilo Python (sem aspas)
    intel.analyze("main.py", "import helper")
    intel.analyze("helper.py", "def run(): pass")
    
    # Teste de importação estilo JS/TS (com aspas)
    intel.analyze("App.tsx", "import { UI } from './UI'")
    intel.analyze("UI.tsx", "export const UI = () => {}")
    
    # Arquivo que não é importado por ninguém
    intel.analyze("unused.py", "def ghost(): pass")
    
    dead = intel.get_dead_code()
    
    assert "unused.py" in dead
    assert "helper.py" not in dead
    assert "UI.tsx" not in dead
