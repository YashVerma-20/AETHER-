# AETHER --- Local Development Environment Setup Guide

**Project:** Adaptive Multi Agent Intelligence: A Performance-Aware Framework for Dynamic Agent Collaboration and Evaluation  
**Acronym:** AETHER (Adaptive Evaluation and Teaming through Historical Evidence and Reasoning)  
**Document ID:** AETHER-ENV-001  
**Version:** 1.0 (Phase 2 Baseline)  
**Status:** Verified Local Environment Specification

---

## 1. System Requirements and Verification Baseline

### 1.1 Hardware Baseline
- **Processor:** Intel Core i5-13550H (12 cores, 16 threads, up to 4.7 GHz Turbo).
- **Physical Memory:** 16.0 GB LPDDR5 RAM (Total visible: 16,494,456 KB).
- **Storage:** 1 TB PCIe SSD (System Drive C: 51 GB free; Workspace Drive D: 288 GB free).
- **GPU:** Integrated Intel Iris Xe Graphics (No dedicated GPU / VRAM).
- **Inference Mode:** 100% CPU-bound local inference using AVX2/threaded GGUF kernels via Ollama.

### 1.2 Financial Constraint
- **Project Budget:** ₹0 additional expenditure.
- **API Policy:** Zero commercial LLM API dependencies (no OpenAI, Anthropic, or paid cloud inference).

---

## 2. Python Environment Setup

### 2.1 Virtual Environment Verification
The project uses an isolated virtual environment located strictly at `D:\AETHER\.venv`.

Verify the virtual environment and upgraded package manager:
```powershell
# Check Python executable path and version
& "D:\AETHER\.venv\Scripts\python.exe" -c "import sys; print(sys.executable); print(sys.version)"

# Check pip version
& "D:\AETHER\.venv\Scripts\pip.exe" --version
```

**Verified Outputs:**
- Python Path: `D:\AETHER\.venv\Scripts\python.exe`
- Python Version: `3.13.1` (64-bit AMD64)
- Pip Version: `pip 26.2.2`

### 2.2 Activation & Deactivation
- **Activation (PowerShell):**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **Deactivation:**
  ```powershell
  deactivate
  ```

---

## 3. Ollama Installation & Local Runtime Configuration

### 3.1 Installation Verification
Ollama is installed locally under user program files and runs as a background service listening on `http://127.0.0.1:11434`.

```powershell
# Verify Ollama CLI version
ollama --version

# Verify Ollama background service process
Get-Process ollama*
```

**Verified Output:**
- Ollama CLI Version: `0.40.13`
- Host Endpoint: `http://127.0.0.1:11434`
- Service Status: Active background process.

### 3.2 Service Health Check
Test API connectivity using PowerShell:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -Method Get
```

---

## 4. Model Management & Operational Rules

### 4.1 Approved Model Policy
- **Primary Family:** Alibaba Cloud **Qwen** is the official preferred LLM family for AETHER.
- **Model Selected:** `qwen2.5:7b` (7.6B parameters, Q4_K_M 4-bit quantization, 4.7 GB disk footprint).
- **Reason for 7B Selection over 14B:** On 16 GB total RAM with integrated graphics, 14B models require ~11–12 GB runtime RAM, causing dangerous memory pressure and slow inference (~2–3 tok/s). The 7B model occupies 5.1 GB in memory, runs at ~7.5–8.2 tok/s on CPU, and preserves >5 GB of free RAM for OS, backend, and PostgreSQL stability.

### 4.2 Pulling and Inspecting Models
To download the approved model:
```powershell
ollama pull qwen2.5:7b
```

Inspect model architecture and context window:
```powershell
ollama show qwen2.5:7b
```

Check loaded models in memory:
```powershell
ollama ps
```

### 4.3 Runtime Safety Controls
1. **Single Model Residency:** Never run or load more than one model simultaneously.
2. **Context Window Cap:** Cap context length to `num_ctx: 4096` in inference payloads to prevent memory expansion.
3. **Sequential Execution:** Agents must execute sequentially; concurrent LLM generation threads are strictly forbidden.

---

## 5. Verification Inference Script

A Python test script demonstrating local zero-cost inference via standard library `urllib` (no external dependencies):

```python
import urllib.request
import json
import time

url = "http://127.0.0.1:11434/api/generate"
payload = {
    "model": "qwen2.5:7b",
    "prompt": "Explain multi-agent collaboration in two sentences.",
    "stream": False,
    "options": {
        "temperature": 0.2,
        "num_ctx": 4096
    }
}

req = urllib.request.Request(
    url, 
    data=json.dumps(payload).encode("utf-8"), 
    headers={"Content-Type": "application/json"}
)

t0 = time.perf_counter()
with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode("utf-8"))
t1 = time.perf_counter()

print("Status:", "OK")
print("Response:", res.get("response"))
print("Latency:", round(t1 - t0, 3), "s")
print("Tokens:", res.get("eval_count"))
print("Speed:", round(res.get("eval_count") / (res.get("eval_duration") / 1e9), 2), "tok/s")
```
