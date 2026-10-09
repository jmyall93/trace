$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
py -3 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\pyinstaller.exe --noconfirm --clean --onefile --windowed --name "TRACE-Edge-Manager" app.py
if ($LASTEXITCODE -ne 0) { throw "Application build failed" }
Write-Host "Manager executable built. Installer packaging is performed by the Windows release workflow."
