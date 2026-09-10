import sqlite3
import json
import hashlib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "tickets" / "customer.db"


def fetch_customer_data(email: str) -> dict:
    """
    Query customer.db for the record matching the given email.

    Returns:
        Dictionary of customer fields
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        row = conn.execute(
            """
            SELECT id, name, email, address, signup_date
            FROM customers
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

    if row is None:
        raise ValueError(f"No customer record found for email: {email}")

    return dict(row)


def build_json_bundle(data: dict, output_path: str) -> str:
    """
    Write data to a JSON file and return a SHA-256 checksum.

    Args:
        data: Customer data dictionary
        output_path: File path to write JSON bundle

    Returns:
        Hex checksum string
    """
    output = Path(output_path)

    if not output.is_absolute():
        output = BASE_DIR / output

    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
        file.write("\n")

    return hashlib.sha256(output.read_bytes()).hexdigest()


if __name__ == "__main__":
    data = fetch_customer_data("ahmed@example.com")

    checksum = build_json_bundle(
        data,
        "reports/portability_bundle.json",
    )

    print("Portability bundle created successfully.")
    print(f"Customer: {data['name']}")
    print(f"Email: {data['email']}")
    print(f"SHA-256: {checksum}")
