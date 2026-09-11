import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def load_baseline(path: str) -> dict:
    """
    Load control baseline JSON.
    """
    baseline_path = BASE_DIR / path

    with baseline_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def review_response(
    row: dict,
    baseline: dict,
) -> str:
    """
    Compare a questionnaire row against the configured baseline.

    Returns:
        PASS
        FAIL
        MISSING
        N/A
    """

    control_id = row["control_id"].strip()
    response = row["response"].strip()

    if not response:
        return "MISSING"

    if control_id not in baseline:
        return "N/A"

    required_keyword = (
        baseline[control_id]["required_keyword"]
        .strip()
        .lower()
    )

    if required_keyword in response.lower():
        return "PASS"

    return "FAIL"


def generate_report(
    csv_path: str,
    baseline_path: str,
    output_path: str,
) -> None:
    """
    Review vendor questionnaire responses and write a gap report.
    """

    questionnaire_path = BASE_DIR / csv_path
    output_file = BASE_DIR / output_path

    baseline = load_baseline(baseline_path)

    with questionnaire_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    results = []

    for row in rows:
        control_id = row["control_id"].strip()

        status = review_response(
            row,
            baseline,
        )

        severity = (
            baseline.get(
                control_id,
                {},
            ).get(
                "severity",
                "N/A",
            )
        )

        result = dict(row)
        result["status"] = status
        result["severity"] = severity

        results.append(result)

    fieldnames = [
        "control_id",
        "control_domain",
        "question",
        "response",
        "evidence_link",
        "status",
        "severity",
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
        writer.writerows(results)


if __name__ == "__main__":
    generate_report(
        "responses/vendor_acme_response.csv",
        "tracker/baseline.json",
        "tracker/vendor_acme_gap_report.csv",
    )
