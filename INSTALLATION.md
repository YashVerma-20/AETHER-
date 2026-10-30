# Installing Stage A into the AETHER repository

1.  Make a backup or create a Git checkpoint before merging these files.
2.  Extract this archive into the root of the actual AETHER repository.
3.  If files with the same names already exist, compare and merge; do
    not blindly overwrite them.
4.  Inspect the existing repository and Git status before any
    implementation.
5.  Review `AGENTS.md` and `.agents/rules/`.
6.  Confirm the Stage A documents with the project owner.
7.  Only then begin Phase 1.

This archive is a reference pack, not an application implementation. It
does not include or replace backend/frontend source code.

## Python Environment Setup

### 1. Requirements & Compatibility
- **Python Version**: Python 3.11+ is recommended (verified active: Python 3.13.1 64-bit).
- **Environment Isolation**: Always use the dedicated virtual environment located at `.venv/`.

### 2. Creating the Virtual Environment
From the repository root (`D:\AETHER`):
```powershell
python -m venv .venv
```

### 3. Activating the Environment
In PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```
*Note: If PowerShell execution policy blocks script execution, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` or call the python/pip binaries directly via `.\.venv\Scripts\python.exe` and `.\.venv\Scripts\pip.exe`.*

Verify active Python and pip:
```powershell
python -c "import sys; print(sys.executable)"
pip --version
```

### 4. Deactivating the Environment
In PowerShell:
```powershell
deactivate
```

### 5. Installing Future Dependencies
Dependencies will be selected and pinned during subsequent phases. Once requirements files are finalized:
```powershell
python -m pip install -r requirements.txt
```

