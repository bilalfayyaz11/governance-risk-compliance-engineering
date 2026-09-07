#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib

BASE = Path("/opt/conmon")
METRICS = BASE / "metrics"
REPORTS = BASE / "reports"

latest = METRICS / "latest.json"

if not latest.exists():
    raise SystemExit("No ConMon metrics available")

data = json.loads(latest.read_text())

now = datetime.now(timezone.utc)

health = data["conmon_health"]
services = data["stack"]["services"]
ports = data["stack"]["ports"]

risk_items = []

if not health["stack_healthy"]:
    risk_items.append(
        "One or more Wazuh platform services are unavailable."
    )

if not health["required_ports_available"]:
    risk_items.append(
        "One or more required monitoring interfaces are unavailable."
    )

if not health["fim_operational"]:
    risk_items.append(
        "File Integrity Monitoring completion evidence was not observed."
    )

if not health["sca_operational"]:
    risk_items.append(
        "Security Configuration Assessment completion evidence was not observed."
    )

if not risk_items:
    risk_statement = (
        "No immediate degradation of the continuous-monitoring "
        "platform was identified in the collected evidence."
    )
    risk_rating = "Low"
else:
    risk_statement = " ".join(risk_items)
    risk_rating = "Moderate"

report = f"""# Monthly Continuous Monitoring Report

## Reporting Period

Generated: {now.isoformat()}

## Executive Summary

The continuous-monitoring program evaluated platform availability, file integrity monitoring, security configuration assessment, and monitoring infrastructure health.

Current residual monitoring risk: **{risk_rating}**

{risk_statement}

## Platform Status

| Component | State |
|---|---|
| Wazuh Indexer | {services.get('wazuh-indexer')} |
| Wazuh Manager | {services.get('wazuh-manager')} |
| Filebeat | {services.get('filebeat')} |
| Wazuh Dashboard | {services.get('wazuh-dashboard')} |

## Control Effectiveness Indicators

| Indicator | Result |
|---|---|
| Complete Wazuh stack operational | {health['stack_healthy']} |
| Required monitoring ports available | {health['required_ports_available']} |
| FIM operational evidence observed | {health['fim_operational']} |
| SCA operational evidence observed | {health['sca_operational']} |
| Ubuntu 24.04 CIS policy observed | {data['sca']['ubuntu_24_04_cis_policy_observed']} |

## Monitoring Cadence

- Security events: continuous
- Agent availability: hourly
- File integrity monitoring: every 6 hours
- Security configuration assessment: daily
- Vulnerability review: daily
- Monitoring coverage review: weekly
- Risk and POA&M review: weekly
- AO continuous-monitoring report: monthly

## Risk Escalation

Immediate escalation is required for:

- unauthorized changes to critical assets
- Critical vulnerabilities
- material authentication anomalies
- loss of monitoring capability
- significant increase in residual risk

High-risk findings must be incorporated into remediation tracking and POA&M governance where applicable.

## Authorizing Official Decision Support

The Authorizing Official should review:

1. control-effectiveness degradation
2. overdue remediation items
3. configuration drift
4. emerging vulnerabilities
5. changes to system risk posture
6. monitoring coverage gaps

Continuous monitoring supports ongoing authorization decisions but does not replace formal reassessment when significant system or risk changes occur.

## Evidence Source

Metrics record:

{latest}
"""

name = (
    REPORTS
    / f"monthly-conmon-report-{now.strftime('%Y-%m')}.md"
)

name.write_text(report)

digest = hashlib.sha256(
    name.read_bytes()
).hexdigest()

hash_file = name.with_suffix(".sha256")
hash_file.write_text(
    f"{digest}  {name.name}\n"
)

print(report)
print(f"\nReport: {name}")
print(f"SHA-256: {digest}")
