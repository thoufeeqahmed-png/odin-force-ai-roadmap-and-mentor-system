# PowerShell Activation Helper for ODIN TA Junior
$VenvScript = Join-Path $PSScriptRoot "venv\Scripts\Activate.ps1"

if (Test-Path $VenvScript) {
    Write-Host "⚔️  Activating ODIN TA Junior Virtual Environment..." -ForegroundColor Cyan
    & $VenvScript
    Write-Host "🛡️  Venv Activated! Ready to run: python manage.py runserver" -ForegroundColor Green
} else {
    Write-Host "⚠️  Virtual environment not found at .\venv. Creating it now..." -ForegroundColor Yellow
    python -m venv (Join-Path $PSScriptRoot "venv")
    & (Join-Path $PSScriptRoot "venv\Scripts\pip.exe") install -r (Join-Path $PSScriptRoot "requirements.txt")
    & $VenvScript
    Write-Host "✨ Venv created & activated successfully!" -ForegroundColor Green
}
