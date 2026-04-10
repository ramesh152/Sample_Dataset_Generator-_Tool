# Windows Quickstart

This project is tested with a local virtual environment at `.myenv`.

## One-command setup

```powershell
powershell -ExecutionPolicy Bypass -File .\setup_windows.ps1
```

## Manual setup (if preferred)

```powershell
python -m venv .myenv
.\.myenv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\.myenv\Scripts\python.exe -m pip install -r .\generator_requirements.txt
.\.myenv\Scripts\streamlit run .\auto_dataset_streamlit.py
```

## Why this fixes `setuptools.build_meta` errors

The failure happens when `setuptools` is missing or when old package pins force source builds on newer Python versions.
This repo now:

- Installs `setuptools` and `wheel` explicitly
- Uses dependency versions compatible with current Windows Python wheels
- Installs inside `.myenv` to avoid global interpreter conflicts
