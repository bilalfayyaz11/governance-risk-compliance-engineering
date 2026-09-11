import csv
from datetime import date, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SEVERITY_DAYS = {
    "Critical": 7,
    "High": 14,
    "Medium": 30,
}

OWNER_MAP = {
    "C4": "Privacy Counsel",
    "C7": "Vendor Risk Manager",
}


def build_tracker(
    gap_report_path: str,
    output_path: str,
) -> None:
    """
    Build remediation tracker from FAIL/MISSING vendor controls.

    Output columns:
        control_id
        issue
        severity
        owner
        due_date
        status
    """

    gap_path = BASE_DIR / gap_report_path
    output_file = BASE_DIR / output_path

    with gap_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        rows = list(csv.DictReader(file))

    today = date.today()

    remediation_rows = []

    for row in rows:
        status = row["status"].strip()

        if status not in {"FAIL", "MISSING"}:
            continue

        control_id = row["control_id"].strip()
        severity = row["severity"].strip()

        if severity not in SEVERITY_DAYS:
            raise ValueError(
                f"Unsupported severity '{severity}' "
                f"for control {control_id}"
            )

        due_date = (
            today
            + timedelta(
                days=SEVERITY_DAYS[severity]
            )
        )

        if status == "MISSING":
            issue = (
                f"Missing vendor response/evidence for "
                f"{row['control_domain']}: "
                f"{row['question']}"
            )
        else:
            issue = (
                f"Vendor response does not meet baseline for "
                f"{row['control_domain']}: "
                f"{row['question']}"
            )

        remediation_rows.append(
            {
                "control_id": control_id,
                "issue": issue,
                "severity": severity,
                "owner": OWNER_MAP.get(
                    control_id,
                    "TBD",
                ),
                "due_date": due_date.isoformat(),
                "status": "Open",
            }
        )

    fieldnames = [
        "control_id",
        "issue",
        "severity",
        "owner",
        "due_date",
        "status",
    ]

    with output_file.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(remediation_rows)


if __name__ == "__main__":
    build_tracker(
        "tracker/vendor_acme_gap_report.csv",
        "tracker/remediation_tracker.csv",
    )
