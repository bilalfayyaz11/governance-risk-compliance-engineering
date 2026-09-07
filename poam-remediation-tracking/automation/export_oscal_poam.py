import json
import os
import re
import uuid
from datetime import datetime, timezone

import requests

REDMINE_URL = os.environ["REDMINE_URL"]
API_KEY = os.environ["REDMINE_API_KEY"]
PROJECT_ID = os.environ["REDMINE_PROJECT_ID"]

OSCAL_VERSION = "1.2.2"
CUSTOM_NS = "https://example.local/ns/security-remediation"


def api_headers():
    return {
        "X-Redmine-API-Key": API_KEY,
        "Content-Type": "application/json",
    }


def deterministic_uuid(category: str, value: str) -> str:
    return str(
        uuid.uuid5(
            uuid.NAMESPACE_URL,
            f"urn:poam:{category}:{value}"
        )
    )


def fetch_all_issues(project_id: str) -> list:
    response = requests.get(
        f"{REDMINE_URL}/issues.json",
        headers=api_headers(),
        params={
            "project_id": project_id,
            "limit": 100,
            "status_id": "*",
        },
        timeout=15,
    )

    response.raise_for_status()

    issues = response.json().get("issues", [])

    detailed = []

    for issue in issues:
        detail_response = requests.get(
            f"{REDMINE_URL}/issues/{issue['id']}.json",
            headers=api_headers(),
            params={"include": "journals"},
            timeout=15,
        )

        detail_response.raise_for_status()
        detailed.append(detail_response.json()["issue"])

    return detailed


def get_description_value(description: str, label: str):
    pattern = rf"^{re.escape(label)}:\s*(.+)$"

    for line in description.splitlines():
        match = re.match(pattern, line.strip(), flags=re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None


def get_custom_field(issue: dict, name: str):
    for field in issue.get("custom_fields", []):
        if field.get("name") == name:
            value = field.get("value")

            if isinstance(value, list):
                return ", ".join(str(v) for v in value)

            return value

    return None


def prop(name: str, value) -> dict:
    if value is None:
        value = ""

    return {
        "name": name,
        "ns": CUSTOM_NS,
        "value": str(value),
    }


def severity_to_priority(severity: str) -> int:
    return {
        "Critical": 1,
        "High": 2,
        "Medium": 3,
        "Low": 4,
    }.get(severity, 5)


def severity_to_risk_statement(severity: str, title: str) -> str:
    return (
        f"{severity} security risk associated with {title}. "
        "The weakness may affect confidentiality, integrity, "
        "availability, or control effectiveness until formally "
        "remediated or accepted."
    )


def risk_response_type(decision: str) -> str:
    mapping = {
        "Risk Accepted": "accept",
        "Transferred": "transfer",
        "Remediate": "mitigate",
    }

    return mapping.get(decision, "mitigate")


def build_oscal_poam(issues: list) -> dict:
    now = datetime.now(timezone.utc).replace(microsecond=0)
    timestamp = now.isoformat().replace("+00:00", "Z")

    document_uuid = deterministic_uuid(
        "document",
        "security-remediation-poam"
    )

    system_uuid = deterministic_uuid(
        "system",
        "security-remediation-tracking-system"
    )

    risks = []
    poam_items = []

    for issue in issues:
        subject = issue.get("subject", "")
        description = issue.get("description", "")

        finding_id = (
            get_description_value(description, "SAR Finding ID")
            or subject.split(":", 1)[0]
        )

        control = (
            get_description_value(description, "NIST Control")
            or "Unknown"
        )

        severity = (
            get_description_value(description, "Severity")
            or issue.get("priority", {}).get("name", "Unknown")
        )

        risk_decision = (
            get_custom_field(issue, "Risk_Decision")
            or "Remediate"
        )

        residual_risk = (
            get_custom_field(issue, "Residual_Risk")
            or "Pending assessment"
        )

        assignee = issue.get(
            "assigned_to",
            {}
        ).get("name", "Unassigned")

        milestone = issue.get(
            "fixed_version",
            {}
        ).get("name", "Unassigned")

        due_date = issue.get("due_date")

        redmine_status = issue.get(
            "status",
            {}
        ).get("name", "Unknown")

        issue_closed = issue.get(
            "status",
            {}
        ).get("is_closed", False)

        risk_uuid = deterministic_uuid(
            "risk",
            finding_id
        )

        poam_uuid = deterministic_uuid(
            "poam-item",
            finding_id
        )

        risk_status = (
            "closed"
            if issue_closed
            else (
                "deviation-approved"
                if risk_decision == "Risk Accepted"
                else "remediating"
            )
        )

        risk_props = [
            {
                "name": "priority",
                "value": str(
                    severity_to_priority(severity)
                ),
            },
            prop("finding-id", finding_id),
            prop("severity", severity),
            prop("control-id", control),
            prop("risk-decision", risk_decision),
            prop("residual-risk", residual_risk),
        ]

        if risk_decision == "Risk Accepted":
            risk_props.append({
                "name": "accepted",
                "value": "true",
            })

        remediation = {
            "uuid": deterministic_uuid(
                "risk-response",
                finding_id
            ),
            "lifecycle": "planned",
            "title": (
                f"{risk_decision} response for {finding_id}"
            ),
            "description": (
                f"Disposition recorded in Redmine as "
                f"{risk_decision}. Owner: {assignee}. "
                f"Milestone: {milestone}."
            ),
            "props": [
                {
                    "name": "type",
                    "value": risk_response_type(
                        risk_decision
                    ),
                },
                prop("owner", assignee),
                prop("milestone", milestone),
            ],
        }

        risk = {
            "uuid": risk_uuid,
            "title": subject,
            "description": (
                f"SAR finding {finding_id} mapped to "
                f"NIST control {control}; severity {severity}."
            ),
            "statement": severity_to_risk_statement(
                severity,
                subject
            ),
            "props": risk_props,
            "status": risk_status,
            "remediations": [remediation],
        }

        if due_date:
            risk["deadline"] = f"{due_date}T23:59:59Z"

        risks.append(risk)

        poam_props = [
            prop("finding-id", finding_id),
            prop("redmine-issue-id", issue["id"]),
            prop("control-id", control),
            prop("severity", severity),
            prop("ticket-status", redmine_status),
            prop("owner", assignee),
            prop("milestone", milestone),
            prop("risk-decision", risk_decision),
            prop("residual-risk", residual_risk),
        ]

        if due_date:
            poam_props.append(
                prop("target-close-date", due_date)
            )

        poam_item = {
            "uuid": poam_uuid,
            "title": subject,
            "description": (
                f"POA&M tracking item for SAR finding "
                f"{finding_id}. Control: {control}. "
                f"Severity: {severity}. "
                f"Current disposition: {risk_decision}."
            ),
            "props": poam_props,
            "related-risks": [
                {
                    "risk-uuid": risk_uuid
                }
            ],
        }

        poam_items.append(poam_item)

    document = {
        "plan-of-action-and-milestones": {
            "uuid": document_uuid,
            "metadata": {
                "title": (
                    "Security Remediation Plan of Action "
                    "and Milestones"
                ),
                "last-modified": timestamp,
                "version": "1.0",
                "oscal-version": OSCAL_VERSION,
                "remarks": (
                    "Generated from structured Redmine "
                    "security remediation tracking records."
                ),
            },
            "system-id": str(system_uuid),
            "risks": risks,
            "poam-items": poam_items,
        }
    }

    return document


def main():
    issues = fetch_all_issues(PROJECT_ID)

    if len(issues) != 3:
        print(
            f"WARNING: expected 3 issues, found {len(issues)}"
        )

    output = build_oscal_poam(issues)

    with open(
        "poam_export.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(output, f, indent=2)

    print(
        f"OSCAL POA&M exported with "
        f"{len(issues)} items"
    )


if __name__ == "__main__":
    main()
