import hashlib
import json
import re
import sys
from pathlib import Path

ALLOWED_DECISIONS = {
    "Authorize",
    "Authorize with Conditions",
    "Deny",
}

SHA256_PATTERN = re.compile(
    r"^[0-9a-f]{64}$"
)


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


def verify_ledger(path: str) -> bool:
    ledger = Path(path)

    if not ledger.is_file():
        print(f"FAIL: ledger missing: {ledger}")
        return False

    lines = [
        line.strip()
        for line in ledger.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    if not lines:
        print("FAIL: ledger contains no records")
        return False

    previous_hash = "GENESIS"
    valid = True

    for number, line in enumerate(
        lines,
        start=1,
    ):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            print(
                f"FAIL: record {number} "
                f"is invalid JSON: {exc}"
            )
            valid = False
            continue

        required = {
            "timestamp",
            "decision",
            "authorization_type",
            "ao_name",
            "justification",
            "evidence_index_hash",
            "previous_record_hash",
            "record_hash",
        }

        missing = required - record.keys()

        if missing:
            print(
                f"FAIL: record {number} missing: "
                + ", ".join(sorted(missing))
            )
            valid = False
            continue

        if record["decision"] not in ALLOWED_DECISIONS:
            print(
                f"FAIL: record {number} "
                "contains invalid decision"
            )
            valid = False

        if not SHA256_PATTERN.fullmatch(
            record["evidence_index_hash"]
        ):
            print(
                f"FAIL: record {number} has "
                "invalid evidence index hash"
            )
            valid = False

        if record["previous_record_hash"] != previous_hash:
            print(
                f"FAIL: record {number} "
                "breaks hash chain"
            )
            valid = False

        expected_hash = calculate_record_hash(
            record
        )

        if record["record_hash"] != expected_hash:
            print(
                f"FAIL: record {number} "
                "record hash mismatch"
            )
            valid = False
        else:
            print(
                f"PASS: record {number} "
                f"{record['record_hash'][:16]}..."
            )

        previous_hash = record["record_hash"]

    print()

    if valid:
        print(
            f"ATO DECISION LEDGER: PASS "
            f"({len(lines)} record(s))"
        )
    else:
        print("ATO DECISION LEDGER: FAIL")

    return valid


if __name__ == "__main__":
    success = verify_ledger(
        "decision/ato-decision-log.jsonl"
    )

    sys.exit(0 if success else 1)
