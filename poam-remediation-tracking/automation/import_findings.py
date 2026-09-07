import json
import os
import requests

REDMINE_URL = "http://localhost:3000"
API_KEY = os.environ["REDMINE_API_KEY"]
PROJECT_ID = "poam-project"


def load_findings(filepath: str) -> list:
    with open(filepath, "r", encoding="utf-8") as f:
        findings = json.load(f)

    required = {"id", "title", "severity", "control"}

    for finding in findings:
        missing = required - finding.keys()
        if missing:
            raise ValueError(
                f"{finding.get('id', 'UNKNOWN')} missing fields: "
                f"{', '.join(sorted(missing))}"
            )

    return findings


def fetch_priorities() -> dict:
    response = requests.get(
        f"{REDMINE_URL}/enumerations/issue_priorities.json",
        headers={"X-Redmine-API-Key": API_KEY},
        timeout=15,
    )
    response.raise_for_status()

    priorities = response.json()["issue_priorities"]

    by_name = {
        p["name"].strip().lower(): p["id"]
        for p in priorities
    }

    print("Available Redmine priorities:")
    for p in priorities:
        print(f"  {p['id']}: {p['name']}")

    def first_match(names):
        for name in names:
            if name in by_name:
                return by_name[name]
        return None

    default_priority = next(
        (
            p["id"]
            for p in priorities
            if p.get("is_default")
        ),
        priorities[0]["id"],
    )

    return {
        "Critical": (
            first_match(["immediate", "urgent", "highest"])
            or default_priority
        ),
        "High": (
            first_match(["urgent", "high"])
            or default_priority
        ),
        "Medium": (
            first_match(["high", "normal"])
            or default_priority
        ),
        "Low": (
            first_match(["low", "normal"])
            or default_priority
        ),
    }


def existing_issue(finding_id: str):
    response = requests.get(
        f"{REDMINE_URL}/issues.json",
        headers={"X-Redmine-API-Key": API_KEY},
        params={
            "project_id": PROJECT_ID,
            "limit": 100,
        },
        timeout=15,
    )
    response.raise_for_status()

    prefix = f"{finding_id}:"

    for issue in response.json().get("issues", []):
        if issue.get("subject", "").startswith(prefix):
            return issue

    return None


def create_ticket(finding: dict, priority_map: dict) -> dict:
    duplicate = existing_issue(finding["id"])

    if duplicate:
        print(
            f"SKIP: {finding['id']} already exists "
            f"as Redmine issue #{duplicate['id']}"
        )
        return duplicate

    headers = {
        "X-Redmine-API-Key": API_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "issue": {
            "project_id": PROJECT_ID,
            "subject": (
                f"{finding['id']}: {finding['title']}"
            ),
            "description": (
                f"SAR Finding ID: {finding['id']}\n"
                f"NIST Control: {finding['control']}\n"
                f"Severity: {finding['severity']}\n\n"
                "Source: Security Assessment Report\n"
                "Disposition: Pending remediation review"
            ),
            "priority_id": priority_map[finding["severity"]],
        }
    }

    response = requests.post(
        f"{REDMINE_URL}/issues.json",
        headers=headers,
        json=payload,
        timeout=15,
    )

    if response.status_code != 201:
        raise RuntimeError(
            f"Failed creating {finding['id']}: "
            f"HTTP {response.status_code} - {response.text}"
        )

    return response.json()["issue"]


if __name__ == "__main__":
    findings = load_findings("sar_findings.json")
    priority_map = fetch_priorities()

    print("\nSeverity mapping:")
    for severity, priority_id in priority_map.items():
        print(f"  {severity}: priority_id={priority_id}")

    print()

    created = []

    for finding in findings:
        issue = create_ticket(finding, priority_map)
        created.append(issue)

        print(
            f"PASS: {finding['id']} -> "
            f"Redmine issue #{issue['id']}"
        )

    with open(
        "imported_issues.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(created, f, indent=2)

    print(f"\nProcessed findings: {len(created)}")
