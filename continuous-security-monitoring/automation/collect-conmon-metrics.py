#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, timezone
import json
import subprocess
import re

BASE = Path("/opt/conmon")
METRICS = BASE / "metrics"
METRICS.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now(timezone.utc)
stamp = timestamp.strftime("%Y%m%dT%H%M%SZ")

def command(cmd):
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout + result.stderr
    except Exception as exc:
        return f"ERROR: {exc}"

ossec_log = Path("/var/ossec/logs/ossec.log")

log_text = ""
if ossec_log.exists():
    try:
        log_text = ossec_log.read_text(errors="ignore")
    except Exception:
        log_text = ""

fim_started = len(re.findall(
    r"File integrity monitoring scan started",
    log_text
))

fim_finished = len(re.findall(
    r"File integrity monitoring scan ended",
    log_text
))

sca_finished = len(re.findall(
    r"Security Configuration Assessment scan finished",
    log_text
))

sca_policy = bool(re.search(
    r"cis_ubuntu24-04\.yml",
    log_text
))

services = {}

for service in [
    "wazuh-indexer",
    "wazuh-manager",
    "filebeat",
    "wazuh-dashboard"
]:
    state = command(
        f"systemctl is-active {service} 2>/dev/null"
    ).strip()

    services[service] = state

ports_output = command(
    "ss -lnt 2>/dev/null"
)

ports = {}

for port in [
    443,
    1514,
    1515,
    55000,
    9200,
    9300
]:
    ports[str(port)] = (
        f":{port} " in ports_output
        or f":{port}\n" in ports_output
    )

critical_file = Path(
    "/opt/conmon/critical-files/application.conf"
)

critical_file_state = {}

if critical_file.exists():
    critical_file_state = {
        "exists": True,
        "size_bytes": critical_file.stat().st_size,
        "mtime_utc": datetime.fromtimestamp(
            critical_file.stat().st_mtime,
            timezone.utc
        ).isoformat()
    }
else:
    critical_file_state = {
        "exists": False
    }

manager_active = (
    services.get("wazuh-manager") == "active"
)

stack_active = all(
    services.get(service) == "active"
    for service in services
)

monitoring_ports_ok = all([
    ports["443"],
    ports["1514"],
    ports["1515"],
    ports["55000"],
    ports["9200"],
])

record = {
    "collection_timestamp_utc": timestamp.isoformat(),
    "stack": {
        "services": services,
        "all_services_active": stack_active,
        "ports": ports
    },
    "fim": {
        "scan_start_events_observed": fim_started,
        "scan_completion_events_observed": fim_finished,
        "manager_active": manager_active
    },
    "sca": {
        "scan_completion_events_observed": sca_finished,
        "ubuntu_24_04_cis_policy_observed": sca_policy
    },
    "controlled_asset": critical_file_state,
    "conmon_health": {
        "stack_healthy": stack_active,
        "required_ports_available": monitoring_ports_ok,
        "fim_operational": fim_finished > 0,
        "sca_operational": sca_finished > 0 and sca_policy
    }
}

output = METRICS / f"conmon-metrics-{stamp}.json"

output.write_text(
    json.dumps(record, indent=2) + "\n"
)

latest = METRICS / "latest.json"
latest.write_text(
    json.dumps(record, indent=2) + "\n"
)

print(json.dumps(record, indent=2))
print(f"\nEvidence written to: {output}")
