#!/usr/bin/env python3

from pathlib import Path
import json
import yaml


def load_inventory(filepath: str) -> dict:
    """
    Load the PII inventory YAML file.

    Args:
        filepath: Path to pii_inventory.yaml

    Returns:
        Parsed dictionary of inventory data.
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"Inventory file not found: {filepath}")

    with path.open("r", encoding="utf-8") as file:
        inventory = yaml.safe_load(file)

    if not isinstance(inventory, dict):
        raise ValueError("Inventory root must be a YAML mapping")

    if "data_elements" not in inventory:
        raise ValueError("Inventory is missing data_elements")

    if not isinstance(inventory["data_elements"], list):
        raise ValueError("data_elements must be a list")

    return inventory


def classify_records(inventory: dict) -> list:
    """
    Classify each data element by privacy risk tier.

    Rules:
        Critical:
            Special-category personal data.

        High:
            High-sensitivity personal data that is not
            already classified as special category.

        Medium:
            Medium-sensitivity identifiable data.

        Low:
            Remaining lower-sensitivity data.

    Returns:
        List of dictionaries with:
        - risk_tier
        - enhanced_safeguards_required
        - classification_reason
    """

    results = []

    for record in inventory["data_elements"]:
        item = dict(record)

        category = str(
            record.get("category", "")
        ).strip().lower()

        sensitivity = str(
            record.get("sensitivity", "")
        ).strip().lower()

        if "special category" in category:
            risk_tier = "Critical"
            enhanced = True
            reason = (
                "Special-category health or biometric data "
                "requires enhanced privacy safeguards."
            )

        elif sensitivity == "high":
            risk_tier = "High"
            enhanced = True
            reason = (
                "High-sensitivity identifiable personal data "
                "requires elevated protection."
            )

        elif sensitivity == "medium":
            risk_tier = "Medium"
            enhanced = False
            reason = (
                "Identifiable or linkable personal data with "
                "moderate privacy impact."
            )

        else:
            risk_tier = "Low"
            enhanced = False
            reason = (
                "Lower-sensitivity data with limited privacy impact."
            )

        item["risk_tier"] = risk_tier
        item["enhanced_safeguards_required"] = enhanced
        item["classification_reason"] = reason

        results.append(item)

    return results


def validate_results(results: list) -> None:
    """
    Validate classification output.
    """

    if not results:
        raise ValueError("No records were classified")

    valid_tiers = {
        "Low",
        "Medium",
        "High",
        "Critical"
    }

    for record in results:
        tier = record.get("risk_tier")

        if tier not in valid_tiers:
            raise ValueError(
                f"Invalid risk tier for {record.get('field')}: {tier}"
            )

    if not any(
        record["risk_tier"] == "Critical"
        for record in results
    ):
        raise ValueError(
            "At least one Critical record is required"
        )


def main() -> None:

    inventory = load_inventory(
        "data/pii_inventory.yaml"
    )

    results = classify_records(inventory)

    validate_results(results)

    print(
        f"{'FIELD':<22} "
        f"{'CATEGORY':<36} "
        f"{'SENSITIVITY':<12} "
        f"{'RISK TIER':<10} "
        f"{'ENHANCED SAFEGUARDS'}"
    )

    print("-" * 105)

    for record in results:
        print(
            f"{record['field']:<22} "
            f"{record['category']:<36} "
            f"{record['sensitivity']:<12} "
            f"{record['risk_tier']:<10} "
            f"{str(record['enhanced_safeguards_required'])}"
        )

    output = Path(
        "evidence/pii-classification-results.json"
    )

    output.write_text(
        json.dumps(results, indent=2) + "\n",
        encoding="utf-8"
    )

    print()
    print(f"Classification evidence: {output}")


if __name__ == "__main__":
    main()
