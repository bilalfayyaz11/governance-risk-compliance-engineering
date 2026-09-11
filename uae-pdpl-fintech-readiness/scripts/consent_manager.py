import json
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONSENT_STORE = BASE_DIR / "data" / "consents.json"

ALLOWED_REQUEST_TYPES = {
    "access",
    "erasure",
    "rectification",
}


def load_consents() -> list:
    """
    Load existing consent records.

    Returns:
        List of stored consent records.
    """
    if not CONSENT_STORE.exists():
        return []

    try:
        with CONSENT_STORE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Consent store must contain a JSON list.")

        return data

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Consent store contains invalid JSON: {CONSENT_STORE}"
        ) from exc


def save_consents(records: list) -> None:
    """
    Persist consent records to the JSON store.
    """
    CONSENT_STORE.parent.mkdir(parents=True, exist_ok=True)

    with CONSENT_STORE.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)


def record_consent(
    user_id: str,
    purpose: str,
    granted: bool,
) -> dict:
    """
    Record a consent event for a user and persist it.

    Returns:
        The consent record dictionary created.
    """

    if not user_id.strip():
        raise ValueError("user_id cannot be empty")

    if not purpose.strip():
        raise ValueError("purpose cannot be empty")

    record = {
        "consent_id": str(uuid.uuid4()),
        "user_id": user_id,
        "purpose": purpose,
        "granted": bool(granted),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    records = load_consents()
    records.append(record)
    save_consents(records)

    return record


def handle_dsar(
    user_id: str,
    request_type: str,
) -> str:
    """
    Simulate handling a data subject request.

    Supported types:
        access
        erasure
        rectification

    Returns:
        Status message with an internal target due date.
    """

    request_type = request_type.strip().lower()

    if request_type not in ALLOWED_REQUEST_TYPES:
        allowed = ", ".join(sorted(ALLOWED_REQUEST_TYPES))
        raise ValueError(
            f"Invalid request_type '{request_type}'. "
            f"Allowed values: {allowed}"
        )

    if not user_id.strip():
        raise ValueError("user_id cannot be empty")

    received_at = datetime.now(timezone.utc)
    due_date = received_at + timedelta(days=30)

    return (
        f"DSAR accepted | user={user_id} | "
        f"type={request_type} | "
        f"received={received_at.date().isoformat()} | "
        f"internal_target_due_date={due_date.date().isoformat()} | "
        f"status=IN_PROGRESS"
    )


if __name__ == "__main__":
    consent = record_consent(
        "user123",
        "marketing_emails",
        True,
    )

    print("Consent recorded:")
    print(json.dumps(consent, indent=2))

    print()
    print("DSAR workflow:")
    print(handle_dsar("user123", "access"))
