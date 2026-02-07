@echo off
echo [MESAFLOW] Iniciando Auditoria em Lote...
mkdir resultados\batch_audit 2>nul
echo Executando: python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_landingpage.xml
python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_landingpage.xml
echo Executando: python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_adminlogin.xml
python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_adminlogin.xml
echo Executando: python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_adminregister.xml
python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_adminregister.xml
echo Executando: python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_admindashboard.xml
python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_admindashboard.xml
echo Executando: python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_adminmenu.xml
python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_adminmenu.xml
echo Executando: python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_adminorders.xml
python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_adminorders.xml
echo Executando: python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_admintables.xml
python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_admintables.xml
echo Executando: python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_admininventory.xml
python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_admininventory.xml
echo Executando: python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_adminsettings.xml
python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_adminsettings.xml
echo Executando: python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_clientmenu.xml
python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_clientmenu.xml
echo Executando: python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_clientkiosk.xml
python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_clientkiosk.xml
echo Executando: python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_clientmonitor.xml
python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_clientmonitor.xml
echo Executando: python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_trustcenter.xml
python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_trustcenter.xml
echo Executando: python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_offlinepage.xml
python scripts/core/forensic_executor_v4_1.py governance\protocols\auto_generated\audit_offlinepage.xml
echo [MESAFLOW] Auditoria concluida. Verifique a pasta 'resultados/batch_audit'.
pause
