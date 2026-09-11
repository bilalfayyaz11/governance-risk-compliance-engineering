import json
from pathlib import Path

from jsonschema import validate, ValidationError, SchemaError

BASE_DIR = Path(__file__).resolve().parent


def load_json_file(filename: str) -> dict:
    """
    Load and return JSON content from a file.
    """
    path = BASE_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def validate_export(
    data_file: str,
    schema_file: str,
) -> bool:
    """
    Validate the exported data against the JSON schema.

    Returns:
        True when valid, otherwise False.
    """

    try:
        data = load_json_file(data_file)
        schema = load_json_file(schema_file)

        validate(
            instance=data,
            schema=schema,
        )

        print(
            f"PASS: {data_file} conforms to {schema_file}"
        )

        return True

    except ValidationError as exc:
        print("FAIL: export does not match schema")
        print(f"Validation error: {exc.message}")

        if exc.path:
            print(
                "Location:",
                " -> ".join(
                    str(item)
                    for item in exc.path
                ),
            )

        return False

    except SchemaError as exc:
        print("FAIL: schema itself is invalid")
        print(exc.message)
        return False


if __name__ == "__main__":
    result = validate_export(
        "export.json",
        "schema.json",
    )

    print(
        "Validation passed!"
        if result
        else "Validation FAILED."
    )

    raise SystemExit(
        0 if result else 1
    )
