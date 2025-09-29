@echo off
echo [!] Stopping download_manager.py...

:: Run PowerShell silently and suppress all errors/output
powershell -Command "try { Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'download_manager.py' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force } } catch {}" >nul 2>&1

echo [✓] download_manager.py terminated.
