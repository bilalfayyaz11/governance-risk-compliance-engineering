import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "tickets" / "dsar.db"

SLA_DAYS = 30
ALLOWED_REQUEST_TYPES = {
    "access",
    "deletion",
    "portability",
    "rectification",
}


def create_request(email: str, request_type: str) -> int:
    """
    Insert a new DSAR ticket into the database.

    Args:
        email: Data subject's email address
        request_type: One of 'access', 'deletion', 'portability', 'rectification'

    Returns:
        The new request ID
    """

    email = email.strip()
    request_type = request_type.strip().lower()

    if not email:
        raise ValueError("Email address cannot be empty")

    if request_type not in ALLOWED_REQUEST_TYPES:
        raise ValueError(
            f"Invalid request type: {request_type}. "
            f"Allowed values: {', '.join(sorted(ALLOWED_REQUEST_TYPES))}"
        )

    now = datetime.now()
    sla_deadline = now + timedelta(days=SLA_DAYS)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO requests (
                subject_email,
                request_type,
                status,
                created_at,
                sla_deadline,
                verified
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                email,
                request_type,
                "received",
                now.isoformat(timespec="seconds"),
                sla_deadline.isoformat(timespec="seconds"),
                0,
            ),
        )

        conn.commit()
        return cursor.lastrowid


if __name__ == "__main__":
    request_id = create_request(
        "subject@example.com",
        "access",
    )

    print(f"DSAR request created successfully. ID: {request_id}")
