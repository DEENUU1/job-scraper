$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location -Path $scriptDirectory

$venvPath = ".venv\Scripts\Activate"
if (Test-Path $venvPath) {
    Write-Host "Activating virtual environment..."
    & $venvPath
} else {
    Write-Host "Virtual environment not found."
    exit 1
}

$pythonScript = "server.py"
if (Test-Path $pythonScript) {
    Write-Host "Running Python script..."
    python $pythonScript
} else {
    Write-Host "Python script 'server.py' not found."
    exit 1
}
