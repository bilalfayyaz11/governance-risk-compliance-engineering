import json
from pathlib import Path

VAULT_PATH = Path.home() / "secure_vault" / "vault.json"


def reidentify_token(token: str, vault_path: str | Path = VAULT_PATH) -> dict:
    """
    Look up the original Emirates ID for a given token.

    Returns:
        Dict with original_id and customer_id,
        or {"error": "Token not found"}
    """
    path = Path(vault_path)

    if not path.exists():
        return {"error": "Vault not found"}

    with path.open("r", encoding="utf-8") as file:
        vault = json.load(file)

    record = vault.get(token.strip())

    if record is None:
        return {"error": "Token not found"}

    return {
        "customer_id": record["customer_id"],
        "original_id": record["original_id"],
    }


if __name__ == "__main__":
    test_token = input("Enter token to reidentify: ").strip()
    result = reidentify_token(test_token)
    print(result)
