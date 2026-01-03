@echo off
echo 🧹 Iniciando limpeza do projeto MesaFlow...

:: Arquivos na Raiz
del assert 2>nul
del gerartxt.py 2>nul
del gerar_sons.py 2>nul
del linksvideosuteirs.txt 2>nul
del ngrok.exe 2>nul
del python 2>nul
del raise 2>nul
del resposta.txt 2>nul
del table_id 2>nul
del todososarquivos.txt 2>nul
del Total 2>nul
del ver_arvore.py 2>nul

:: Pastas Duplicadas/Erradas
rmdir /s /q "frontend\src\admin[slug]" 2>nul
rmdir /s /q "frontend\src\app[slug]" 2>nul
rmdir /s /q "pp" 2>nul
rmdir /s /q "output_sounds" 2>nul

:: Testes Obsoletos
del "tests\test_auth.py" 2>nul
del "tests\test_options.py" 2>nul
del "tests\test_stock.py" 2>nul

echo ✅ Limpeza concluida!
pause