# AURA — Autonomous Unified Risk Analyzer

AURA is a deployable **defensive** security posture analyzer that scans dependency manifests via the **OSV (Open Source Vulnerabilities)** API, generates an **explainable risk score**, and returns **plain-English remediation guidance**.

**Tech:** FastAPI + minimal Web UI + Docker + GitHub Actions CI

## What it does
- Upload `requirements.txt`, `pyproject.toml`, or `package-lock.json`
- AURA queries OSV for known vulnerabilities
- It returns:
  - `risk_score` (0–100)
  - a readable `summary`
  - full JSON results

## Run (Docker)
```bash
docker compose up --build
```

- Web UI: http://localhost:8080  
- API health: http://localhost:8000/health  
- API scan: `POST /scan` (multipart file upload)

## API usage (curl)
```bash
curl -s -X POST "http://localhost:8000/scan"       -F "file=@requirements.txt" | jq
```

## Supported inputs
- `requirements.txt` (PyPI)
- `pyproject.toml` (PyPI, best-effort parse)
- `package-lock.json` (npm)

## Notes
- This is **defensive**: it reports known vulnerabilities from public advisories (OSV).
- Risk scoring is intentionally simple & explainable. You can evolve it later.

## License
MIT
