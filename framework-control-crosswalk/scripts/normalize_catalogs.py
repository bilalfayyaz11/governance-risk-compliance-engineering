from pathlib import Path
import pandas as pd

BASE = Path.home() / "crosswalk-lab" / "data"

catalogs = {
    "iso27001.csv": {
        "output": "normalized_iso27001.csv",
        "category_column": "domain",
    },
    "nist_csf.csv": {
        "output": "normalized_nist_csf.csv",
        "category_column": "function",
    },
    "sama_csf.csv": {
        "output": "normalized_sama_csf.csv",
        "category_column": "principle",
    },
}


def clean_text(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )


for filename, config in catalogs.items():
    input_path = BASE / filename
    output_path = BASE / config["output"]
    category_column = config["category_column"]

    df = pd.read_csv(input_path, dtype=str)

    required = {"control_id", "control_title", category_column}
    missing = required - set(df.columns)

    if missing:
        print(f"FAIL: {filename} missing columns: {sorted(missing)}")
        continue

    df["control_id"] = clean_text(df["control_id"])
    df["control_title"] = clean_text(df["control_title"])
    df[category_column] = clean_text(df[category_column])

    # Normalize schema across all three frameworks.
    df = df.rename(columns={category_column: "category"})

    df = df[
        ["control_id", "control_title", "category"]
    ]

    df = df.drop_duplicates(subset=["control_id"]).reset_index(drop=True)

    df.to_csv(output_path, index=False)

    print(f"\nPASS: {config['output']} created")
    print(f"Rows: {len(df)}")
    print("Categories:")
    for category in sorted(df["category"].dropna().unique()):
        print(f"  - {category}")

print("\nNormalization complete.")
