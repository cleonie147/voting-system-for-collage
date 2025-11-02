Write-Host "Starting College Voting System Desktop App..." -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host ""
}

# Install/update dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
& ".\.venv\Scripts\pip.exe" install -r requirements.txt --quiet
Write-Host ""

# Launch the desktop app
Write-Host "Launching application..." -ForegroundColor Green
& ".\.venv\Scripts\python.exe" app_desktop.py
