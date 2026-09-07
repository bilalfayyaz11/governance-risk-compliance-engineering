import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ALLOWED_DECISIONS = {
    "Authorize",
    "Authorize with Conditions",
    "Deny",
}


def canonical_json(data: dict) -> bytes:
    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def calculate_record_hash(record: dict) -> str:
    content = {
        key: value
        for key, value in record.items()
        if key != "record_hash"
    }

    return hashlib.sha256(
        canonical_json(content)
    ).hexdigest()


def read_previous_hash(output: Path) -> str:
    if not output.exists() or output.stat().st_size == 0:
        return "GENESIS"

    lines = [
        line.strip()
        for line in output.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    if not lines:
        return "GENESIS"

    previous = json.loads(lines[-1])

    previous_hash = previous.get("record_hash")

    if not previous_hash:
        raise ValueError(
            "Existing ledger entry has no record_hash"
        )

    return previous_hash


def record_decision(
    decision: str,
    ao_name: str,
    justification: str,
    evidence_index_hash: str,
    output_path: str,
) -> dict:

    if decision not in ALLOWED_DECISIONS:
        raise ValueError(
            "Decision must be one of: "
            + ", ".join(sorted(ALLOWED_DECISIONS))
        )

    if len(evidence_index_hash) != 64:
        raise ValueError(
            "Evidence index hash must be a SHA-256 digest"
        )

    try:
        int(evidence_index_hash, 16)
    except ValueError as exc:
        raise ValueError(
            "Evidence index hash must contain hexadecimal characters"
        ) from exc

    output = Path(output_path)
    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    previous_hash = read_previous_hash(output)

    record = {
        "record_version": "1.0",
        "timestamp": (
            datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        ),
        "decision": decision,
        "authorization_type": (
            "Interim ATO"
            if decision == "Authorize with Conditions"
            else (
                "Full ATO"
                if decision == "Authorize"
                else "Denial"
            )
        ),
        "ao_name": ao_name,
        "justification": justification,
        "evidence_index_hash": evidence_index_hash,
        "previous_record_hash": previous_hash,
    }

    record["record_hash"] = calculate_record_hash(
        record
    )

    with output.open(
        "a",
        encoding="utf-8",
    ) as handle:
        handle.write(
            json.dumps(
                record,
                sort_keys=True,
            )
            + "\n"
        )

    return record


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Append a hash-chained authorization "
            "decision to the ATO ledger."
        )
    )

    parser.add_argument(
        "--decision",
        required=True,
        choices=sorted(ALLOWED_DECISIONS),
    )

    parser.add_argument(
        "--ao-name",
        required=True,
    )

    parser.add_argument(
        "--justification",
        required=True,
    )

    parser.add_argument(
        "--evidence-index-hash",
        required=True,
    )

    parser.add_argument(
        "--output",
        default="decision/ato-decision-log.jsonl",
    )

    args = parser.parse_args()

    record = record_decision(
        decision=args.decision,
        ao_name=args.ao_name,
        justification=args.justification,
        evidence_index_hash=args.evidence_index_hash,
        output_path=args.output,
    )

    print(
        json.dumps(
            record,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
