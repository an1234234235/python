param([switch]$Network)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if ($Network) {
    $env:SANPC_HOST = "0.0.0.0"
} elseif (-not $env:SANPC_HOST) {
    $env:SANPC_HOST = "127.0.0.1"
}

$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    & $venvPython "server.py"
    exit $LASTEXITCODE
}

if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 "server.py"
    exit $LASTEXITCODE
}

& python "server.py"
exit $LASTEXITCODE
