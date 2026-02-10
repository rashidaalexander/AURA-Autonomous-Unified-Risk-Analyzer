from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from .parsers import detect_and_extract_packages
from .osv_client import query_osv_bulk
from .scoring import compute_risk_score, summarize_plain_english

app = FastAPI(title="AURA — Autonomous Unified Risk Analyzer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "aura"}

@app.post("/scan")
async def scan(file: UploadFile = File(...)):
    raw = await file.read()
    filename = (file.filename or "upload").lower()

    parsed = detect_and_extract_packages(filename, raw)
    if not parsed["ok"]:
        return parsed

    eco = parsed["ecosystem"]
    pkgs = parsed["packages"]

    osv_results = query_osv_bulk(pkgs, ecosystem=eco)

    score = compute_risk_score(osv_results)
    summary = summarize_plain_english(osv_results, score)

    return {
        "ok": True,
        "filename": file.filename,
        "ecosystem": eco,
        "packages_scanned": len(pkgs),
        "risk_score": score,
        "summary": summary,
        "results": osv_results,
    }
