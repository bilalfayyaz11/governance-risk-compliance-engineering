#!/usr/bin/env python3

from pathlib import Path

import pandas as pd


PATH = Path(
    "data/fair_factors.csv"
)

REQUIRED_COLUMNS = [
    "factor",
    "node_group",
    "min",
    "most_likely",
    "max",
    "unit",
    "distribution",
    "assumption",
]


def main() -> None:
    df = pd.read_csv(
        PATH
    )

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    if df.empty:
        raise ValueError(
            "Factor table is empty"
        )

    for column in [
        "factor",
        "node_group",
        "unit",
        "distribution",
        "assumption",
    ]:
        if (
            df[column]
            .isna()
            .any()
        ):
            raise ValueError(
                f"Null value detected in {column}"
            )

    numeric = [
        "min",
        "most_likely",
        "max",
    ]

    for column in numeric:
        df[column] = pd.to_numeric(
            df[column],
            errors="raise",
        )

    invalid_order = df[
        ~(
            (df["min"] <= df["most_likely"])
            &
            (df["most_likely"] <= df["max"])
        )
    ]

    if not invalid_order.empty:
        raise ValueError(
            "Invalid min/mode/max ordering:\n"
            + invalid_order[
                [
                    "factor",
                    "min",
                    "most_likely",
                    "max",
                ]
            ].to_string(
                index=False
            )
        )

    probability_rows = df[
        df["unit"]
        == "probability"
    ]

    probability_values = probability_rows[
        [
            "min",
            "most_likely",
            "max",
        ]
    ]

    if (
        (
            probability_values < 0
        )
        |
        (
            probability_values > 1
        )
    ).any().any():
        raise ValueError(
            "Probability estimates must remain between 0 and 1"
        )

    percentile_rows = df[
        df["unit"]
        == "percentile"
    ]

    percentile_values = percentile_rows[
        [
            "min",
            "most_likely",
            "max",
        ]
    ]

    if (
        (
            percentile_values < 0
        )
        |
        (
            percentile_values > 100
        )
    ).any().any():
        raise ValueError(
            "Percentiles must remain between 0 and 100"
        )

    print(
        "PASS | FAIR factor table schema valid"
    )

    print(
        f"Factors defined: {len(df)}"
    )

    print()
    print(
        df[
            [
                "factor",
                "node_group",
                "min",
                "most_likely",
                "max",
                "unit",
                "distribution",
            ]
        ].to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()
