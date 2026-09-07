#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

BASE = Path("/opt/conmon")
DATA = BASE / "dashboard" / "data"

baseline_file = DATA / "configuration-baseline.json"

if not baseline_file.exists():
    raise SystemExit("Configuration baseline missing")

baseline = json.loads(baseline_file.read_text())

results = []

for asset in baseline["assets"]:

    path = Path(asset["path"])

    if not path.exists():
        results.append({
            "path": str(path),
            "status": "Missing",
            "baseline_sha256": asset.get("sha256"),
            "current_sha256": None
        })
        continue

    current_hash = hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

    baseline_hash = asset.get("sha256")

    if baseline_hash == current_hash:
        state = "Compliant"
    else:
        state = "Drift Detected"

    results.append({
        "path": str(path),
        "status": state,
        "baseline_sha256": baseline_hash,
        "current_sha256": current_hash,
        "checked_utc":
            datetime.now(timezone.utc).isoformat()
    })

summary = {
    "checked_utc":
        datetime.now(timezone.utc).isoformat(),

    "assets_checked":
        len(results),

    "compliant":
        sum(
            1 for item in results
            if item["status"] == "Compliant"
        ),

    "drifted":
        sum(
            1 for item in results
            if item["status"] == "Drift Detected"
        ),

    "missing":
        sum(
            1 for item in results
            if item["status"] == "Missing"
        ),

    "results": results
}

output = DATA / "configuration-drift.json"

output.write_text(
    json.dumps(summary, indent=2) + "\n"
)

print(json.dumps(summary, indent=2))
