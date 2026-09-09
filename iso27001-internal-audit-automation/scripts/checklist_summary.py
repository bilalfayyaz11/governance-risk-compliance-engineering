#!/usr/bin/env python3

from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = {
    "Control_ID",
    "Control_Name",
    "Category",
    "Status",
    "Evidence_Ref",
}


def load_checklist(csv_path: str | Path) -> pd.DataFrame:
    """
    Load the Annex A checklist CSV into a DataFrame.
    """
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Checklist not found: {path}"
        )

    df = pd.read_csv(
        path,
        keep_default_na=False,
    )

    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(sorted(missing))
        )

    return df


def summarize_status(df: pd.DataFrame) -> dict:
    """
    Count controls by audit status.
    """
    return (
        df["Status"]
        .value_counts()
        .to_dict()
    )


def summarize_categories(df: pd.DataFrame) -> dict:
    """
    Count controls by Annex A category.
    """
    return (
        df["Category"]
        .value_counts()
        .to_dict()
    )


def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent

    checklist_path = (
        base_dir
        / "plan"
        / "annex_a_checklist.csv"
    )

    df = load_checklist(
        checklist_path
    )

    print("ISO 27001:2022 ANNEX A CHECKLIST SUMMARY")
    print("=" * 55)

    print(f"Total selected controls: {len(df)}")

    print()
    print("Status summary:")
    print(
        summarize_status(df)
    )

    print()
    print("Category summary:")
    print(
        summarize_categories(df)
    )

    print()
    print(
        df[
            [
                "Control_ID",
                "Control_Name",
                "Category",
                "Status",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
