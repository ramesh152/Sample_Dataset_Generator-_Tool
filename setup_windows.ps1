$ErrorActionPreference = "Stop"

Write-Host "[1/5] Checking Python availability..."
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python is not installed or not available on PATH."
}

Write-Host "[2/5] Creating virtual environment (.myenv) if needed..."
if (-not (Test-Path ".myenv\Scripts\python.exe")) {
    python -m venv .myenv
}

$venvPython = ".\.myenv\Scripts\python.exe"

Write-Host "[3/5] Upgrading pip/setuptools/wheel in virtual environment..."
& $venvPython -m pip install --upgrade pip setuptools wheel

Write-Host "[4/5] Installing project dependencies..."
& $venvPython -m pip install -r generator_requirements.txt

Write-Host "[5/5] Verifying critical imports..."
& $venvPython -c "import cv2, numpy, pandas, PIL, streamlit; print('Environment check passed.')"

Write-Host ""
Write-Host "Setup complete."
Write-Host "Run the app with:"
Write-Host ".\.myenv\Scripts\streamlit run auto_dataset_streamlit.py"
