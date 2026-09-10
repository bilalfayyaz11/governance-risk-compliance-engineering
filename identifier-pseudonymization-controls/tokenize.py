import psycopg2
import hmac
import hashlib
import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
KEY_PATH = BASE_DIR / "vault.key"
VAULT_PATH = BASE_DIR / "vault.json"

DB_CONFIG = {
    "dbname": "privacy_lab",
    "user": "lab_app",
    "password": "LabPass123",
    "host": "localhost",
}


def load_or_create_key() -> bytes:
    """
    Load the existing tokenization key or create it once.

    Returns:
        32-byte secret key
    """
    if KEY_PATH.exists():
        return KEY_PATH.read_bytes()

    key = os.urandom(32)

    with open(KEY_PATH, "wb") as key_file:
        key_file.write(key)

    os.chmod(KEY_PATH, 0o600)
    return key


SECRET_KEY = load_or_create_key()


def format_preserving_token(emirates_id: str, key: bytes) -> str:
    """
    Generate a deterministic format-preserving token for an Emirates ID.

    Input:
        784-YYYY-NNNNNNN-C

    Output:
        784-YYYY-TTTTTTT-T
    """
    parts = emirates_id.split("-")

    if len(parts) != 4:
        raise ValueError(f"Invalid Emirates ID format: {emirates_id}")

    country_code, year, serial, check_digit = parts

    if (
        country_code != "784"
        or len(year) != 4
        or len(serial) != 7
        or len(check_digit) != 1
        or not year.isdigit()
        or not serial.isdigit()
        or not check_digit.isdigit()
    ):
        raise ValueError(f"Invalid Emirates ID format: {emirates_id}")

    suffix = f"{serial}{check_digit}"

    digest = hmac.new(
        key,
        suffix.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    token_number = int(digest, 16) % (10 ** 8)
    token_digits = str(token_number).zfill(8)

    return (
        f"{country_code}-"
        f"{year}-"
        f"{token_digits[:7]}-"
        f"{token_digits[7]}"
    )


def build_token_vault(records: list) -> dict:
    """
    Build a mapping:
        token -> customer_id + original Emirates ID
    """
    vault = {}

    for customer_id, emirates_id in records:
        token = format_preserving_token(
            emirates_id,
            SECRET_KEY
        )

        if token in vault:
            raise ValueError(
                f"Token collision detected for token: {token}"
            )

        vault[token] = {
            "customer_id": customer_id,
            "original_id": emirates_id,
        }

    return vault


def fetch_customers(conn) -> list:
    """
    Fetch customer identifiers from raw_data.customers.
    """
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT customer_id, emirates_id
            FROM raw_data.customers
            ORDER BY customer_id
            """
        )

        return cursor.fetchall()


if __name__ == "__main__":
    conn = psycopg2.connect(**DB_CONFIG)

    try:
        records = fetch_customers(conn)

        vault = build_token_vault(records)

        with open(VAULT_PATH, "w", encoding="utf-8") as vault_file:
            json.dump(
                vault,
                vault_file,
                indent=2,
                sort_keys=True
            )
            vault_file.write("\n")

        os.chmod(VAULT_PATH, 0o600)

        print(f"Fetched records: {len(records)}")
        print(f"Vault entries: {len(vault)}")
        print(f"Vault written to: {VAULT_PATH}")
        print(f"Key written to: {KEY_PATH}")

        print("\nGenerated tokens:")

        for token, record in vault.items():
            print(
                f"customer_id={record['customer_id']} "
                f"token={token}"
            )

    finally:
        conn.close()
