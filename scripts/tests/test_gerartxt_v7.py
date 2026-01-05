import os
import shutil
from pathlib import Path
import pytest
from gerartxt import main
import sys

@pytest.mark.asyncio
async def test_flat_handover_structure():
    """Verifica se o script gera a pasta flat com os prefixos corretos."""
    # Simula execução sem imagens para ser rápido
    sys.argv = ["gerartxt.py", "--no-img"]
    
    from gerartxt import main as run_main
    await run_main()
    
    handover_path = Path("HANDOVER_MESAFLOW")
    assert handover_path.exists()
    
    # Verifica se o arquivo principal de código existe com o prefixo
    code_files = list(handover_path.glob("CODE_*.txt"))
    assert len(code_files) > 0
    
    # Limpeza
    # shutil.rmtree(handover_path) # Comentado para inspeção manual se necessário
