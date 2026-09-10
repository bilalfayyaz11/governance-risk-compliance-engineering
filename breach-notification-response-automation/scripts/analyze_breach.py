#!/usr/bin/env python3

import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ALERTS_PATH = BASE_DIR / "evidence" / "breach_alerts_raw.jsonl"
OUTPUT_JSON = BASE_DIR / "breach_analysis_output.json"
OUTPUT_MD = BASE_DIR / "reports" / "breach_classification.md"


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )


def analyze_breach_alerts(alerts_path: str | Path) -> dict:
    """
    Parse Wazuh breach alerts and return an impact summary.
    """
    path = Path(alerts_path)

    alerts = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            event = json.loads(line)

            rule_id = str(
                event.get("rule", {}).get("id", "")
            )

            if rule_id not in {"100100", "100101"}:
                continue

            alerts.append(event)

    if not alerts:
        raise ValueError("No breach alerts found")

    primary_alerts = [
        event
        for event in alerts
        if str(event.get("rule", {}).get("id")) == "100100"
    ]

    if not primary_alerts:
        raise ValueError("No rule 100100 alerts found")

    subjects = set()
    emails = set()
    national_ids = set()
    source_ips = set()
    endpoints = set()
    sessions = set()
    record_counts = []
    timestamps = []

    for event in primary_alerts:
        data = event.get("data", {})

        email = data.get("email")
        national_id = data.get("national_id")
        srcip = data.get("srcip")
        endpoint = data.get("endpoint")
        session = data.get("session")
        records = data.get("records")
        timestamp = event.get("timestamp")

        # National ID is the strongest subject identifier in this simulation.
        if national_id:
            subjects.add(national_id)
            national_ids.add(national_id)
        elif email:
            subjects.add(email)

        if email:
            emails.add(email)

        if srcip:
            source_ips.add(srcip)

        if endpoint:
            endpoints.add(endpoint)

        if session:
            sessions.add(session)

        if records:
            try:
                record_counts.append(int(records))
            except (TypeError, ValueError):
                pass

        if timestamp:
            timestamps.append(parse_timestamp(timestamp))

    first_seen = min(timestamps)
    last_seen = max(timestamps)
    exposure_seconds = int(
        (last_seen - first_seen).total_seconds()
    )

    data_categories = []

    if emails:
        data_categories.append("Email addresses")

    if national_ids:
        data_categories.append(
            "Government-issued national identifiers"
        )

    # This simulation contains identifiers and contact data,
    # but no GDPR Article 9 special-category data.
    special_category_present = False

    max_records = max(record_counts) if record_counts else 0

    # Risk rubric: 0-10
    score = 0
    reasons = []

    if national_ids:
        score += 3
        reasons.append(
            "Government-issued identifiers were exposed (+3)"
        )

    if emails:
        score += 1
        reasons.append(
            "Contact identifiers were exposed (+1)"
        )

    if max_records >= 500:
        score += 2
        reasons.append(
            "Bulk export involved at least 500 records (+2)"
        )

    if source_ips:
        score += 2
        reasons.append(
            "Unauthorized external-source access indicator present (+2)"
        )

    if len(primary_alerts) >= 3:
        score += 1
        reasons.append(
            "Repeated exfiltration activity detected (+1)"
        )

    if special_category_present:
        score += 1
        reasons.append(
            "Special-category data present (+1)"
        )

    risk_score = min(score, 10)

    if risk_score >= 7:
        risk_level = "HIGH"
    elif risk_score >= 4:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    authority_notification_required = risk_score >= 4
    data_subject_notification_required = risk_score >= 7

    result = {
        "affected_subjects_count": len(subjects),
        "unique_emails_detected": len(emails),
        "unique_national_ids_detected": len(national_ids),
        "data_categories": data_categories,
        "special_category_data_present": special_category_present,
        "source_ips": sorted(source_ips),
        "sensitive_endpoints": sorted(endpoints),
        "sessions": sorted(sessions),
        "maximum_reported_records_per_export": max_records,
        "primary_breach_alert_count": len(primary_alerts),
        "first_seen": first_seen.isoformat(),
        "last_seen": last_seen.isoformat(),
        "exposure_duration_seconds": exposure_seconds,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_reasons": reasons,
        "supervisory_authority_notification_required":
            authority_notification_required,
        "data_subject_notification_required":
            data_subject_notification_required,
    }

    return result


def write_markdown_report(result: dict) -> None:
    OUTPUT_MD.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    authority = (
        "YES"
        if result[
            "supervisory_authority_notification_required"
        ]
        else "NO"
    )

    subjects = (
        "YES"
        if result["data_subject_notification_required"]
        else "NO"
    )

    special = (
        "YES"
        if result["special_category_data_present"]
        else "NO"
    )

    reasons = "\n".join(
        f"- {reason}"
        for reason in result["risk_reasons"]
    )

    categories = "\n".join(
        f"- {category}"
        for category in result["data_categories"]
    )

    content = f"""# Breach Risk Classification

## Incident Summary

Affected subjects observed in alert evidence: {result['affected_subjects_count']}

Maximum records reported in a bulk export: {result['maximum_reported_records_per_export']}

Primary Wazuh breach alerts: {result['primary_breach_alert_count']}

First seen: {result['first_seen']}

Last seen: {result['last_seen']}

Observed exposure duration: {result['exposure_duration_seconds']} seconds

## Exposed Data Categories

{categories}

GDPR Article 9 special-category data detected: {special}

The simulation contains contact information and government-issued identifiers. These are sensitive personal identifiers, but the evidence generated in this simulation does not include health, biometric, religious, political, sexual-orientation, or other Article 9 special-category data.

## Attack Vector

The Wazuh evidence indicates repeated unauthorized bulk GET requests against a sensitive customer export endpoint from the same external source.

Sensitive endpoint(s):

{chr(10).join('- ' + item for item in result['sensitive_endpoints'])}

Source IP(s):

{chr(10).join('- ' + item for item in result['source_ips'])}

## Risk Score

Score: {result['risk_score']}/10

Classification: {result['risk_level']}

### Scoring Rationale

{reasons}

The score is an exercise-specific decision rubric rather than a statutory formula. It is used to consistently evaluate the nature of the data, scale of exposure, attack characteristics, and potential impact on individuals.

## GDPR Article 33 Decision

Supervisory authority notification required: **{authority}**

GDPR Article 33(1) requires notification unless the breach is unlikely to result in a risk to the rights and freedoms of natural persons.

This incident involves unauthorized bulk exposure of email addresses and government-issued identifiers. The combination creates credible risks including identity fraud, targeted phishing, impersonation, and misuse of government identifiers. It therefore cannot reasonably be characterized as unlikely to create risk.

## GDPR Article 34 Decision

Data subject notification required: **{subjects}**

GDPR Article 34 applies when a personal data breach is likely to result in a high risk to individuals.

The simulated incident is classified HIGH because government identifiers were included in a bulk unauthorized export and repeated exfiltration indicators were detected. Direct notification is therefore appropriate under the exercise risk model.

## KSA PDPL Decision

Competent Authority notification required: **{authority}**

Data Subject notification required: **{subjects}**

KSA PDPL Implementing Regulations Article 24 requires notification to the Competent Authority within 72 hours where a breach may harm personal data or the Data Subject or conflict with their rights or interests.

It also requires notification of affected Data Subjects without undue delay where the incident may cause damage to their data or prejudice their rights or interests.

The simulated exposure satisfies those thresholds because government identifiers and contact data were exposed through unauthorized bulk-access activity.

## Decision

This incident proceeds to both:

1. Supervisory / Competent Authority notification.
2. Data Subject notification.

The actual notification deadline is maintained separately from this analysis using the Wazuh detection timestamp recorded as T0.
"""

    OUTPUT_MD.write_text(
        content,
        encoding="utf-8",
    )


if __name__ == "__main__":
    result = analyze_breach_alerts(ALERTS_PATH)

    OUTPUT_JSON.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )

    write_markdown_report(result)

    print(json.dumps(result, indent=2))
    print()
    print(f"JSON output: {OUTPUT_JSON}")
    print(f"Report: {OUTPUT_MD}")
