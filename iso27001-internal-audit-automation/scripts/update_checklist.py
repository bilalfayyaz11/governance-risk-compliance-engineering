#!/usr/bin/env python3

from pathlib import Path
import sys

import pandas as pd


VALID_STATUSES = {
    "Not Tested",
    "Conforms",
    "Nonconformity",
    "Observation",
    "Partially Tested",
}


def update_control(
    csv_path: str,
    control_id: str,
    status: str,
    evidence_ref: str,
) -> None:
    path = Path(csv_path)

    if status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid status: {status}"
        )

    df = pd.read_csv(
        path,
        keep_default_na=False,
    )

    matches = (
        df["Control_ID"]
        == control_id
    )

    if matches.sum() != 1:
        raise ValueError(
            f"Expected exactly one row for {control_id}; "
            f"found {matches.sum()}"
        )

    df.loc[
        matches,
        "Status",
    ] = status

    df.loc[
        matches,
        "Evidence_Ref",
    ] = evidence_ref

    df.to_csv(
        path,
        index=False,
    )

    print(
        f"Updated {control_id} -> {status}"
    )


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise SystemExit(
            "Usage: update_checklist.py "
            "<csv> <control_id> <status> <evidence_ref>"
        )

    update_control(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3],
        sys.argv[4],
    )
