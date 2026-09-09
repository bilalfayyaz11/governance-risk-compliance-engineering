#!/usr/bin/env python3

import csv
from datetime import date
from pathlib import Path
import sys


VALID_SEVERITIES = {
    "Major",
    "Minor",
    "Observation",
}


FIELDNAMES = [
    "Finding_ID",
    "Date",
    "Control_ID",
    "Description",
    "Severity",
    "Evidence_Ref",
    "Recommendation",
]


def ensure_register(csv_path: Path) -> None:
    """
    Create the findings register with a header if it does not exist.
    """
    if csv_path.exists():
        return

    csv_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=FIELDNAMES,
        )

        writer.writeheader()


def next_finding_id(csv_path: Path) -> str:
    """
    Generate the next sequential ID:
        F001
        F002
        ...
    """
    ensure_register(
        csv_path
    )

    with csv_path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as handle:
        reader = csv.DictReader(
            handle
        )

        rows = list(
            reader
        )

    max_number = 0

    for row in rows:
        finding_id = (
            row.get(
                "Finding_ID",
                "",
            )
            .strip()
            .upper()
        )

        if (
            finding_id.startswith("F")
            and finding_id[1:].isdigit()
        ):
            max_number = max(
                max_number,
                int(
                    finding_id[1:]
                ),
            )

    return (
        f"F{max_number + 1:03d}"
    )


def add_finding(
    csv_path: str,
    control_id: str,
    description: str,
    severity: str,
    evidence_ref: str,
    recommendation: str,
) -> None:
    """
    Append a new finding row to the nonconformity register.
    """
    path = Path(
        csv_path
    )

    severity = (
        severity
        .strip()
        .title()
    )

    if severity not in VALID_SEVERITIES:
        raise ValueError(
            "Severity must be one of: "
            + ", ".join(
                sorted(
                    VALID_SEVERITIES
                )
            )
        )

    if not description.strip():
        raise ValueError(
            "Description cannot be empty"
        )

    if not recommendation.strip():
        raise ValueError(
            "Recommendation cannot be empty"
        )

    ensure_register(
        path
    )

    finding_id = next_finding_id(
        path
    )

    row = {
        "Finding_ID":
            finding_id,

        "Date":
            date.today().isoformat(),

        "Control_ID":
            control_id.strip(),

        "Description":
            description.strip(),

        "Severity":
            severity,

        "Evidence_Ref":
            evidence_ref.strip(),

        "Recommendation":
            recommendation.strip(),
    }

    with path.open(
        "a",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=FIELDNAMES,
        )

        writer.writerow(
            row
        )

    print(
        f"PASS | Added {finding_id} "
        f"[{severity}] "
        f"{control_id}"
    )


def main() -> None:
    if len(sys.argv) == 7:
        add_finding(
            csv_path=sys.argv[1],
            control_id=sys.argv[2],
            description=sys.argv[3],
            severity=sys.argv[4],
            evidence_ref=sys.argv[5],
            recommendation=sys.argv[6],
        )

        return

    add_finding(
        "../findings/nonconformity_register.csv",
        control_id="A.8.9",
        description=(
            "Password maximum age exceeds the "
            "organizational policy limit of 90 days."
        ),
        severity="Minor",
        evidence_ref=(
            "../evidence/"
            "A8_9_password_policy_evidence.txt"
        ),
        recommendation=(
            "Review applicable local accounts and "
            "update the approved password-aging "
            "configuration so PASS_MAX_DAYS does not "
            "exceed 90 days where local password "
            "authentication is used."
        ),
    )


if __name__ == "__main__":
    main()
