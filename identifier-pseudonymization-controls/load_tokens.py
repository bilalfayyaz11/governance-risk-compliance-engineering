import json
import psycopg2
from pathlib import Path

VAULT_PATH = Path.home() / "secure_vault" / "vault.json"

DB_CONFIG = {
    "dbname": "privacy_lab",
    "user": "lab_app",
    "password": "LabPass123",
    "host": "localhost",
}


def load_vault() -> dict:
    with VAULT_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def fetch_customer_metadata(conn) -> dict:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT customer_id, full_name, phone
            FROM raw_data.customers
            ORDER BY customer_id
            """
        )

        return {
            row[0]: {
                "full_name": row[1],
                "phone": row[2],
            }
            for row in cursor.fetchall()
        }


def load_tokenized_records(conn, vault: dict, metadata: dict) -> None:
    rows = []

    for token, record in vault.items():
        customer_id = record["customer_id"]

        if customer_id not in metadata:
            raise ValueError(
                f"Missing raw metadata for customer_id={customer_id}"
            )

        rows.append(
            (
                customer_id,
                metadata[customer_id]["full_name"],
                token,
                metadata[customer_id]["phone"],
            )
        )

    with conn.cursor() as cursor:
        cursor.execute(
            "DELETE FROM pseudonymized.customers"
        )

        cursor.executemany(
            """
            INSERT INTO pseudonymized.customers (
                customer_id,
                full_name,
                emirates_id_token,
                phone
            )
            VALUES (%s, %s, %s, %s)
            """,
            rows,
        )

    conn.commit()


if __name__ == "__main__":
    vault = load_vault()

    conn = psycopg2.connect(**DB_CONFIG)

    try:
        metadata = fetch_customer_metadata(conn)
        load_tokenized_records(conn, vault, metadata)

        print(f"Loaded tokenized records: {len(vault)}")

    finally:
        conn.close()
