import pandas as pd
from pathlib import Path


def classify_sensitivity(row: dict) -> str:
    """
    Classify a personal-data element as critical, sensitive, or standard.
    """

    data_element = str(row.get("data_element", "")).strip().lower()
    emirates_id = str(row.get("is_emirates_id", "")).strip().lower()

    # Emirates ID receives the highest handling classification.
    if emirates_id == "true":
        return "critical"

    # Financial information requires increased protection.
    financial_terms = (
        "transaction",
        "bank account",
        "account number",
    )

    if any(term in data_element for term in financial_terms):
        return "sensitive"

    return "standard"


def generate_report(csv_path: str, output_path: str) -> None:
    """
    Read the personal-data inventory, classify each row,
    and generate a human-readable report.
    """

    csv_file = Path(csv_path)
    output_file = Path(output_path)

    if not csv_file.exists():
        raise FileNotFoundError(f"Inventory not found: {csv_file}")

    df = pd.read_csv(csv_file)

    required_columns = {
        "data_element",
        "source_system",
        "storage_location",
        "processing_purpose",
        "is_emirates_id",
        "retention_days",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    df["classification"] = df.apply(
        lambda row: classify_sensitivity(row.to_dict()),
        axis=1,
    )

    counts = (
        df["classification"]
        .value_counts()
        .reindex(
            ["critical", "sensitive", "standard"],
            fill_value=0,
        )
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as report:
        report.write("FINTECH PERSONAL DATA FLOW REPORT\n")
        report.write("=" * 72 + "\n\n")

        report.write("CLASSIFICATION SUMMARY\n")
        report.write("-" * 30 + "\n")

        for classification, count in counts.items():
            report.write(
                f"{classification.capitalize()}: {count}\n"
            )

        report.write("\nPERSONAL DATA INVENTORY\n")
        report.write("-" * 72 + "\n")

        report.write(df.to_string(index=False))
        report.write("\n")


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent

    generate_report(
        base_dir / "data" / "data_inventory.csv",
        base_dir / "docs" / "data_flow_report.txt",
    )
