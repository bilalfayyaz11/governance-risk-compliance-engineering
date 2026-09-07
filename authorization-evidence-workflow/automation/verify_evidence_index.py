import hashlib
import json
import sys
from pathlib import Path


def compute_sha256(filepath: Path) -> str:
    digest = hashlib.sha256()

    with filepath.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)

    return digest.hexdigest()


def verify_index(base_dir: str, index_path: str) -> bool:
    base = Path(base_dir).resolve()
    index_file = Path(index_path)

    if not index_file.is_absolute():
        index_file = base / index_file

    if not index_file.is_file():
        print(f"FAIL: evidence index missing: {index_file}")
        return False

    with index_file.open("r", encoding="utf-8") as handle:
        index = json.load(handle)

    entries = index.get("entries", [])

    valid = True

    print(f"Index entries: {len(entries)}")
    print()

    for entry in entries:
        relative = entry["relative_path"]
        expected_hash = entry["sha256"]
        expected_size = entry["size_bytes"]

        path = base / relative

        if not path.is_file():
            print(f"MISSING: {relative}")
            valid = False
            continue

        actual_size = path.stat().st_size
        actual_hash = compute_sha256(path)

        if actual_size != expected_size:
            print(
                f"SIZE MISMATCH: {relative} "
                f"expected={expected_size} actual={actual_size}"
            )
            valid = False
            continue

        if actual_hash != expected_hash:
            print(f"HASH MISMATCH: {relative}")
            valid = False
            continue

        print(f"PASS: {relative}")

    print()

    if valid:
        print("EVIDENCE VERIFICATION: PASS")
    else:
        print("EVIDENCE VERIFICATION: FAIL")

    return valid


if __name__ == "__main__":
    success = verify_index(
        ".",
        "evidence/evidence-index.json",
    )

    sys.exit(0 if success else 1)
