import json
import os
from datetime import date, timedelta

import requests

REDMINE_URL = os.environ["REDMINE_URL"]
API_KEY = os.environ["REDMINE_API_KEY"]
PROJECT_ID = os.environ["REDMINE_PROJECT_ID"]

OWNER_ID = int(os.environ["OWNER_ID"])
Q1_VERSION_ID = int(os.environ["Q1_VERSION_ID"])
Q2_VERSION_ID = int(os.environ["Q2_VERSION_ID"])

SLA_DAYS = {
    "High": 30,
    "Medium": 60,
    "Low": 90,
}

MILESTONE_MAP = {
    "High": Q1_VERSION_ID,
    "Medium": Q1_VERSION_ID,
    "Low": Q2_VERSION_ID,
}


def headers():
    return {
        "X-Redmine-API-Key": API_KEY,
        "Content-Type": "application/json",
    }


def fetch_issues():
    response = requests.get(
        f"{REDMINE_URL}/issues.json",
        headers=headers(),
        params={
            "project_id": PROJECT_ID,
            "limit": 100,
        },
        timeout=15,
    )

    response.raise_for_status()
    return response.json().get("issues", [])


def extract_severity(issue):
    description = issue.get("description", "")

    for line in description.splitlines():
        if line.startswith("Severity:"):
            return line.split(":", 1)[1].strip()

    raise ValueError(
        f"Severity missing from issue #{issue['id']}"
    )


def update_ticket_dates(
    issue_id: int,
    due_date: str,
    assigned_to_id: int,
    fixed_version_id: int,
) -> None:

    payload = {
        "issue": {
            "due_date": due_date,
            "assigned_to_id": assigned_to_id,
            "fixed_version_id": fixed_version_id,
            "notes": (
                "POA&M ownership and target remediation date "
                "assigned according to severity-based SLA."
            ),
        }
    }

    response = requests.put(
        f"{REDMINE_URL}/issues/{issue_id}.json",
        headers=headers(),
        json=payload,
        timeout=15,
    )

    if response.status_code != 204:
        raise RuntimeError(
            f"Issue #{issue_id} update failed: "
            f"HTTP {response.status_code} - {response.text}"
        )


def main():
    issues = fetch_issues()

    updated = []

    for issue in issues:
        severity = extract_severity(issue)

        if severity not in SLA_DAYS:
            print(
                f"SKIP: issue #{issue['id']} "
                f"unknown severity {severity}"
            )
            continue

        due = (
            date.today()
            + timedelta(days=SLA_DAYS[severity])
        ).isoformat()

        milestone = MILESTONE_MAP[severity]

        update_ticket_dates(
            issue["id"],
            due,
            OWNER_ID,
            milestone,
        )

        updated.append({
            "issue_id": issue["id"],
            "subject": issue["subject"],
            "severity": severity,
            "due_date": due,
            "assigned_to_id": OWNER_ID,
            "fixed_version_id": milestone,
        })

        print(
            f"PASS: #{issue['id']} "
            f"{severity} -> due {due}, "
            f"owner {OWNER_ID}, "
            f"version {milestone}"
        )

    with open(
        "assignment_results.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(updated, f, indent=2)

    print(f"\nUpdated issues: {len(updated)}")


if __name__ == "__main__":
    main()
