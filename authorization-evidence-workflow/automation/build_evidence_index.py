import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

EXCLUDED_PATHS = {
    "evidence/evidence-index.json",
    "evidence/evidence-index.json.sig",
}

EXCLUDED_PARTS = {
    ".git",
    "__pycache__",
}


def compute_sha256(filepath: str) -> str:
    digest = hashlib.sha256()

    with open(filepath, "rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)

    return digest.hexdigest()


def build_index(base_dir: str, output_path: str) -> None:
    base = Path(base_dir).resolve()
    output = Path(output_path)

    if not output.is_absolute():
        output = base / output

    entries = []
    indexed_at = (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )

    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue

        relative = path.relative_to(base)
        relative_string = relative.as_posix()

        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue

        if relative_string in EXCLUDED_PATHS:
            continue

        entries.append(
            {
                "relative_path": relative_string,
                "sha256": compute_sha256(str(path)),
                "size_bytes": path.stat().st_size,
                "indexed_at": indexed_at,
            }
        )

    document = {
        "schema_version": "1.0",
        "hash_algorithm": "SHA-256",
        "package_root": ".",
        "generated_at": indexed_at,
        "artifact_count": len(entries),
        "entries": entries,
    }

    output.parent.mkdir(parents=True, exist_ok=True)

    temporary = output.with_suffix(output.suffix + ".tmp")

    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(document, handle, indent=2)
        handle.write("\n")

    temporary.replace(output)

    print(f"Evidence index written: {output}")
    print(f"Indexed artifacts: {len(entries)}")


if __name__ == "__main__":
    build_index(".", "evidence/evidence-index.json")
