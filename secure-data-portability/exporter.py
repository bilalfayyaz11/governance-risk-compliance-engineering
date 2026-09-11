import csv
import json
from pathlib import Path

from sample_data import USER_RECORD, PORTABLE_FIELDS

BASE_DIR = Path(__file__).resolve().parent


def extract_portable_data(record: dict, fields: list) -> dict:
    """
    Filter the full record down to only portable fields.
    """
    return {
        key: record[key]
        for key in fields
        if key in record
    }


def export_to_json(data: dict, filename: str) -> None:
    """
    Save portable data as formatted JSON.
    """
    output_path = BASE_DIR / filename

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )

        file.write("\n")


def export_to_csv(data: dict, filename: str) -> None:
    """
    Save portable data as CSV.

    Nested structures are serialized as JSON strings so they remain
    machine-readable rather than Python-specific representations.
    """
    output_path = BASE_DIR / filename

    normalized = {}

    for key, value in data.items():
        if isinstance(value, (dict, list)):
            normalized[key] = json.dumps(
                value,
                separators=(",", ":"),
                ensure_ascii=False,
            )
        else:
            normalized[key] = value

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(normalized.keys()),
        )

        writer.writeheader()
        writer.writerow(normalized)


if __name__ == "__main__":
    portable_data = extract_portable_data(
        USER_RECORD,
        PORTABLE_FIELDS,
    )

    export_to_json(
        portable_data,
        "export.json",
    )

    export_to_csv(
        portable_data,
        "export.csv",
    )

    print(
        "Export complete: export.json and export.csv created."
    )
