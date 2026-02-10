from typing import List, Dict, Any

def compute_risk_score(results: List[Dict[str, Any]]) -> int:
    # Explainable scoring (0..100)
    score = 0
    for r in results:
        vc = int(r.get("vuln_count", 0) or 0)
        score += vc * 8

        vulns = r.get("vulnerabilities", []) or []
        for v in vulns:
            sev = v.get("severity", []) or []
            if sev:
                score += 3

    return min(100, score)

def summarize_plain_english(results: List[Dict[str, Any]], score: int) -> str:
    total_vulns = sum(int(r.get("vuln_count", 0) or 0) for r in results)
    affected = [r["package"] for r in results if int(r.get("vuln_count", 0) or 0) > 0]

    if total_vulns == 0:
        return (
            f"Risk score {score}/100. No known vulnerabilities found via OSV for the detected dependencies. "
            "Keep dependencies updated and re-scan regularly."
        )

    top = affected[:8]
    more = max(0, len(affected) - len(top))
    pkg_list = ", ".join(top) + (f" (+{more} more)" if more else "")

    if score >= 70:
        tone = "High risk. Prioritize upgrades and patching now."
    elif score >= 40:
        tone = "Moderate risk. Plan upgrades soon, starting with the most-used packages."
    else:
        tone = "Low-to-moderate risk. Address findings during your next maintenance window."

    return (
        f"Risk score {score}/100. Found {total_vulns} known vulnerabilities affecting: {pkg_list}. "
        f"{tone} Focus on updating impacted dependencies and review advisories before deploying to production."
    )
