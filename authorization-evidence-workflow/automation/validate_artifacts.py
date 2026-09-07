import csv
import json
from pathlib import Path

REQUIRED_POAM_COLUMNS = [
    "id",
    "weakness",
    "control",
    "severity",
    "status",
    "milestone",
    "due_date",
]

ARTIFACTS = {
    "ssp": Path("ssp/system-security-plan.md"),
    "sar": Path("sar/security-assessment-report.md"),
    "poam": Path("poam/poam.csv"),
    "risk_assessment": Path("risk-assessment/risk-assessment.md"),
}


def nonempty_file(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def validate_package(base_dir: str) -> dict:
    base = Path(base_dir)

    result = {
        "ssp": False,
        "sar": False,
        "poam": False,
        "risk_assessment": False,
        "errors": [],
    }

    for name in ("ssp", "sar", "risk_assessment"):
        path = base / ARTIFACTS[name]

        if nonempty_file(path):
            result[name] = True
        else:
            result["errors"].append(
                f"Missing or empty artifact: {path}"
            )

    poam_path = base / ARTIFACTS["poam"]

    if not nonempty_file(poam_path):
        result["errors"].append(
            f"Missing or empty artifact: {poam_path}"
        )
        return result

    try:
        with poam_path.open(
            newline="",
            encoding="utf-8",
        ) as handle:
            reader = csv.DictReader(handle)

            columns = reader.fieldnames or []

            missing_columns = [
                column
                for column in REQUIRED_POAM_COLUMNS
                if column not in columns
            ]

            rows = list(reader)

            if missing_columns:
                result["errors"].append(
                    "POA&M missing required columns: "
                    + ", ".join(missing_columns)
                )

            if not rows:
                result["errors"].append(
                    "POA&M contains no finding records"
                )

            invalid_rows = []

            for line_number, row in enumerate(
                rows,
                start=2,
            ):
                missing_values = [
                    column
                    for column in REQUIRED_POAM_COLUMNS
                    if not str(
                        row.get(column, "")
                    ).strip()
                ]

                if missing_values:
                    invalid_rows.append(
                        {
                            "line": line_number,
                            "missing": missing_values,
                        }
                    )

            if invalid_rows:
                result["errors"].append(
                    "POA&M contains incomplete rows: "
                    + json.dumps(invalid_rows)
                )

            if (
                not missing_columns
                and rows
                and not invalid_rows
            ):
                result["poam"] = True

    except (OSError, csv.Error) as exc:
        result["errors"].append(
            f"Unable to parse POA&M: {exc}"
        )

    return result


if __name__ == "__main__":
    validation = validate_package(".")

    print(
        json.dumps(
            validation,
            indent=2,
        )
    )

    overall = all(
        validation[key]
        for key in (
            "ssp",
            "sar",
            "poam",
            "risk_assessment",
        )
    )

    print()
    print(
        "OVERALL: PASS"
        if overall
        else "OVERALL: FAIL"
    )
