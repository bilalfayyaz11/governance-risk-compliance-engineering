#!/usr/bin/env python3

from pathlib import Path
from typing import Dict

import pandas as pd
from sqlalchemy import create_engine, text


DATABASE_URL = "postgresql+psycopg2:///gcc_grc_map"

REQUIRED_COLUMNS = {
    "control_id",
    "domain",
    "title",
    "description",
    "control_type",
}

FRAMEWORK_METADATA: Dict[str, Dict[str, str]] = {
    "NCA_ECC": {
        "version": "2-2024",
        "jurisdiction": "Saudi Arabia",
        "authority": "National Cybersecurity Authority",
    },
    "SAMA_CSF": {
        "version": "1.0",
        "jurisdiction": "Saudi Arabia",
        "authority": "Saudi Central Bank",
    },
    "UAE_ISR": {
        "version": "Current Representative Extract",
        "jurisdiction": "United Arab Emirates",
        "authority": "Dubai Electronic Security Center",
    },
    "QATAR_NIA": {
        "version": "2.1",
        "jurisdiction": "Qatar",
        "authority": "National Cyber Security Agency",
    },
    "NIST_800_53": {
        "version": "Rev 5",
        "jurisdiction": "United States / Reference",
        "authority": "National Institute of Standards and Technology",
    },
    "ISO_27001": {
        "version": "2022",
        "jurisdiction": "International / Reference",
        "authority": "ISO/IEC",
    },
}


def validate_csv_schema(df: pd.DataFrame, csv_path: str) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(
            f"{csv_path} missing columns: {sorted(missing)}"
        )

    if df.empty:
        raise ValueError(
            f"{csv_path} contains no controls"
        )

    for column in [
        "control_id",
        "domain",
        "title",
        "description",
    ]:
        if df[column].isna().any():
            raise ValueError(
                f"{csv_path} contains null values in {column}"
            )

        if (
            df[column]
            .astype(str)
            .str.strip()
            .eq("")
            .any()
        ):
            raise ValueError(
                f"{csv_path} contains blank values in {column}"
            )

    duplicate_refs = (
        df["control_id"]
        .astype(str)
        .duplicated()
    )

    if duplicate_refs.any():
        duplicates = (
            df.loc[
                duplicate_refs,
                "control_id",
            ]
            .astype(str)
            .tolist()
        )

        raise ValueError(
            f"{csv_path} duplicate control IDs: {duplicates}"
        )


def get_or_create_framework(
    framework_name: str,
    engine,
) -> int:
    if framework_name not in FRAMEWORK_METADATA:
        raise ValueError(
            f"Unknown framework: {framework_name}"
        )

    metadata = FRAMEWORK_METADATA[
        framework_name
    ]

    with engine.begin() as conn:
        framework_id = conn.execute(
            text(
                """
                INSERT INTO frameworks (
                    name,
                    version,
                    jurisdiction,
                    authority
                )
                VALUES (
                    :name,
                    :version,
                    :jurisdiction,
                    :authority
                )
                ON CONFLICT (name, version)
                DO UPDATE SET
                    jurisdiction = EXCLUDED.jurisdiction,
                    authority = EXCLUDED.authority
                RETURNING id
                """
            ),
            {
                "name": framework_name,
                **metadata,
            },
        ).scalar_one()

    return int(
        framework_id
    )


def load_framework_csv(
    csv_path: str,
    framework_name: str,
    engine,
) -> int:
    """
    Load a normalized regulator or reference control catalog.

    Existing controls are updated by framework + control_ref,
    making the loader idempotent across repeated executions.
    """
    df = pd.read_csv(
        csv_path
    )

    validate_csv_schema(
        df,
        csv_path,
    )

    framework_id = get_or_create_framework(
        framework_name,
        engine,
    )

    rows_processed = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(
                text(
                    """
                    INSERT INTO controls (
                        framework_id,
                        control_ref,
                        domain,
                        title,
                        description,
                        control_type
                    )
                    VALUES (
                        :framework_id,
                        :control_ref,
                        :domain,
                        :title,
                        :description,
                        :control_type
                    )
                    ON CONFLICT (
                        framework_id,
                        control_ref
                    )
                    DO UPDATE SET
                        domain = EXCLUDED.domain,
                        title = EXCLUDED.title,
                        description = EXCLUDED.description,
                        control_type = EXCLUDED.control_type
                    """
                ),
                {
                    "framework_id":
                        framework_id,
                    "control_ref":
                        str(
                            row[
                                "control_id"
                            ]
                        ).strip(),
                    "domain":
                        str(
                            row[
                                "domain"
                            ]
                        ).strip(),
                    "title":
                        str(
                            row[
                                "title"
                            ]
                        ).strip(),
                    "description":
                        str(
                            row[
                                "description"
                            ]
                        ).strip(),
                    "control_type":
                        str(
                            row[
                                "control_type"
                            ]
                        ).strip(),
                },
            )

            rows_processed += 1

    return rows_processed


def validate_catalog_integrity(
    engine,
) -> dict:
    """
    Return counts per framework and identify malformed controls.
    """
    with engine.connect() as conn:
        counts = conn.execute(
            text(
                """
                SELECT
                    f.name,
                    f.version,
                    COUNT(c.id) AS control_count
                FROM frameworks f
                LEFT JOIN controls c
                    ON c.framework_id = f.id
                GROUP BY
                    f.id,
                    f.name,
                    f.version
                ORDER BY f.name
                """
            )
        ).mappings().all()

        invalid = conn.execute(
            text(
                """
                SELECT
                    c.id,
                    f.name,
                    c.control_ref
                FROM controls c
                JOIN frameworks f
                    ON f.id = c.framework_id
                WHERE
                    c.control_ref IS NULL
                    OR BTRIM(c.control_ref) = ''
                    OR c.domain IS NULL
                    OR BTRIM(c.domain) = ''
                    OR c.title IS NULL
                    OR BTRIM(c.title) = ''
                    OR c.description IS NULL
                    OR BTRIM(c.description) = ''
                """
            )
        ).mappings().all()

    return {
        "counts": [
            dict(row)
            for row in counts
        ],
        "invalid_controls": [
            dict(row)
            for row in invalid
        ],
    }


def main() -> None:
    engine = create_engine(
        DATABASE_URL
    )

    catalogs = [
        (
            "data/nca_ecc.csv",
            "NCA_ECC",
        ),
        (
            "data/sama_csf.csv",
            "SAMA_CSF",
        ),
        (
            "data/uae_isr.csv",
            "UAE_ISR",
        ),
        (
            "data/qatar_nia.csv",
            "QATAR_NIA",
        ),
        (
            "data/nist_800_53.csv",
            "NIST_800_53",
        ),
        (
            "data/iso_27001.csv",
            "ISO_27001",
        ),
    ]

    total = 0

    for csv_path, framework in catalogs:
        inserted = load_framework_csv(
            csv_path,
            framework,
            engine,
        )

        total += inserted

        print(
            f"{framework}: "
            f"{inserted} controls processed"
        )

    print(
        f"\nTotal controls processed: {total}"
    )

    integrity = validate_catalog_integrity(
        engine
    )

    print(
        "\nCATALOG INTEGRITY"
    )

    print(
        "=" * 72
    )

    for item in integrity[
        "counts"
    ]:
        print(
            f"{item['name']:<15} "
            f"{item['version']:<30} "
            f"{item['control_count']} controls"
        )

    if integrity[
        "invalid_controls"
    ]:
        print(
            "\nFAIL | Invalid controls detected:"
        )

        for row in integrity[
            "invalid_controls"
        ]:
            print(
                row
            )

        raise SystemExit(1)

    print(
        "\nPASS | No controls missing required fields"
    )


if __name__ == "__main__":
    main()
