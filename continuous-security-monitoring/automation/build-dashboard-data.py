#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

BASE = Path("/opt/conmon")
METRICS = BASE / "metrics"
DASH = BASE / "dashboard" / "data"

latest = METRICS / "latest.json"

if not latest.exists():
    raise SystemExit("Missing /opt/conmon/metrics/latest.json")

data = json.loads(latest.read_text())
now = datetime.now(timezone.utc).isoformat()

health = data.get("conmon_health", {})
services = data.get("stack", {}).get("services", {})
ports = data.get("stack", {}).get("ports", {})

def status(condition):
    return "Effective" if condition else "Degraded"

controls = [
    {
        "control_family": "SI",
        "capability": "File Integrity Monitoring",
        "metric": "FIM operational evidence",
        "status": status(health.get("fim_operational", False)),
        "monitoring_frequency": "6 hours",
        "evidence_source": "Wazuh FIM"
    },
    {
        "control_family": "CA",
        "capability": "Security Configuration Assessment",
        "metric": "SCA operational evidence",
        "status": status(health.get("sca_operational", False)),
        "monitoring_frequency": "Daily",
        "evidence_source": "Wazuh SCA"
    },
    {
        "control_family": "CA",
        "capability": "Continuous Monitoring Infrastructure",
        "metric": "Wazuh stack availability",
        "status": status(health.get("stack_healthy", False)),
        "monitoring_frequency": "Continuous",
        "evidence_source": "systemd/Wazuh"
    },
    {
        "control_family": "CM",
        "capability": "Configuration Monitoring",
        "metric": "Required monitoring interfaces",
        "status": status(
            health.get("required_ports_available", False)
        ),
        "monitoring_frequency": "Continuous",
        "evidence_source": "Network listener validation"
    }
]

summary = {
    "timestamp_utc": now,
    "effective": sum(
        1 for item in controls
        if item["status"] == "Effective"
    ),
    "degraded": sum(
        1 for item in controls
        if item["status"] == "Degraded"
    ),
    "controls": controls,
    "service_state": services,
    "port_state": ports
}

output = DASH / "control-effectiveness.json"

output.write_text(
    json.dumps(summary, indent=2) + "\n"
)

print(json.dumps(summary, indent=2))
