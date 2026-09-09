#!/usr/bin/env python3

from pathlib import Path
from typing import Dict, List

import pandas as pd
from sqlalchemy import create_engine, text


DATABASE_URL = "postgresql+psycopg2:///gcc_grc_map"

GCC_FRAMEWORKS = [
    "NCA_ECC",
    "SAMA_CSF",
    "UAE_ISR",
    "QATAR_NIA",
]

REFERENCE_FRAMEWORKS = [
    "NIST_800_53",
    "ISO_27001",
]

OVERLAY_NAMES = [
    "data_residency",
    "arabic_logging",
    "national_cert_reporting",
    "local_hosting_mandate",
]


def load_control_inventory(engine) -> pd.DataFrame:
    query = text(
        """
        SELECT
            c.id AS control_id,
            f.name AS framework,
            f.version,
            f.jurisdiction,
            c.control_ref,
            c.domain,
            c.title,
            c.description
        FROM controls c
        JOIN frameworks f
            ON f.id = c.framework_id
        ORDER BY
            c.domain,
            f.name,
            c.control_ref
        """
    )

    return pd.read_sql(
        query,
        engine,
    )


def load_crosswalks(engine) -> pd.DataFrame:
    query = text(
        """
        SELECT
            cw.source_control_id,
            cw.target_control_id,
            cw.mapping_strength,
            cw.rationale,

            c1.id AS control_1_id,
            f1.name AS framework_1,
            c1.control_ref AS control_1_ref,
            c1.domain AS control_1_domain,

            c2.id AS control_2_id,
            f2.name AS framework_2,
            c2.control_ref AS control_2_ref,
            c2.domain AS control_2_domain

        FROM crosswalks cw

        JOIN controls c1
            ON c1.id = cw.source_control_id
        JOIN frameworks f1
            ON f1.id = c1.framework_id

        JOIN controls c2
            ON c2.id = cw.target_control_id
        JOIN frameworks f2
            ON f2.id = c2.framework_id
        """
    )

    return pd.read_sql(
        query,
        engine,
    )


def load_overlays(engine) -> pd.DataFrame:
    query = text(
        """
        SELECT
            c.id AS control_id,
            f.name AS framework,
            c.control_ref,
            c.domain,
            o.name AS overlay
        FROM control_overlays co
        JOIN controls c
            ON c.id = co.control_id
        JOIN frameworks f
            ON f.id = c.framework_id
        JOIN overlays o
            ON o.id = co.overlay_id
        ORDER BY
            c.domain,
            f.name,
            c.control_ref,
            o.name
        """
    )

    return pd.read_sql(
        query,
        engine,
    )


def get_gcc_reference_mappings(
    crosswalks: pd.DataFrame,
) -> pd.DataFrame:
    rows: List[Dict] = []

    for _, row in crosswalks.iterrows():
        framework_1 = row[
            "framework_1"
        ]

        framework_2 = row[
            "framework_2"
        ]

        if (
            framework_1 in GCC_FRAMEWORKS
            and framework_2 in REFERENCE_FRAMEWORKS
        ):
            rows.append(
                {
                    "gcc_control_id":
                        row["control_1_id"],
                    "gcc_framework":
                        framework_1,
                    "gcc_control_ref":
                        row["control_1_ref"],
                    "gcc_domain":
                        row["control_1_domain"],
                    "reference_framework":
                        framework_2,
                    "reference_control_ref":
                        row["control_2_ref"],
                    "mapping_strength":
                        row["mapping_strength"],
                }
            )

        elif (
            framework_2 in GCC_FRAMEWORKS
            and framework_1 in REFERENCE_FRAMEWORKS
        ):
            rows.append(
                {
                    "gcc_control_id":
                        row["control_2_id"],
                    "gcc_framework":
                        framework_2,
                    "gcc_control_ref":
                        row["control_2_ref"],
                    "gcc_domain":
                        row["control_2_domain"],
                    "reference_framework":
                        framework_1,
                    "reference_control_ref":
                        row["control_1_ref"],
                    "mapping_strength":
                        row["mapping_strength"],
                }
            )

    return pd.DataFrame(
        rows
    )


def yes_no(
    condition: bool,
) -> str:
    return (
        "Yes"
        if condition
        else "No"
    )


def build_applicability_matrix(
    engine,
    output_path: str,
) -> None:
    controls = load_control_inventory(
        engine
    )

    crosswalks = load_crosswalks(
        engine
    )

    overlays = load_overlays(
        engine
    )

    gcc_controls = controls[
        controls[
            "framework"
        ].isin(
            GCC_FRAMEWORKS
        )
    ].copy()

    mappings = (
        get_gcc_reference_mappings(
            crosswalks
        )
    )

    domains = sorted(
        gcc_controls[
            "domain"
        ]
        .dropna()
        .unique()
    )

    rows: List[Dict] = []

    for domain in domains:
        domain_controls = gcc_controls[
            gcc_controls[
                "domain"
            ] == domain
        ]

        domain_control_ids = set(
            domain_controls[
                "control_id"
            ]
            .astype(int)
        )

        row: Dict = {
            "domain": domain,
        }

        for framework in GCC_FRAMEWORKS:
            framework_controls = domain_controls[
                domain_controls[
                    "framework"
                ] == framework
            ]

            row[
                framework
            ] = yes_no(
                not framework_controls.empty
            )

            row[
                f"{framework}_control_count"
            ] = int(
                len(
                    framework_controls
                )
            )

        if mappings.empty:
            domain_mappings = pd.DataFrame()
        else:
            domain_mappings = mappings[
                mappings[
                    "gcc_control_id"
                ].isin(
                    domain_control_ids
                )
            ]

        nist_mappings = (
            domain_mappings[
                domain_mappings[
                    "reference_framework"
                ] == "NIST_800_53"
            ]
            if not domain_mappings.empty
            else pd.DataFrame()
        )

        iso_mappings = (
            domain_mappings[
                domain_mappings[
                    "reference_framework"
                ] == "ISO_27001"
            ]
            if not domain_mappings.empty
            else pd.DataFrame()
        )

        row[
            "nist_mapping"
        ] = yes_no(
            not nist_mappings.empty
        )

        row[
            "iso_mapping"
        ] = yes_no(
            not iso_mappings.empty
        )

        row[
            "nist_mapping_count"
        ] = int(
            len(
                nist_mappings
            )
        )

        row[
            "iso_mapping_count"
        ] = int(
            len(
                iso_mappings
            )
        )

        if domain_control_ids:
            mapped_ids = (
                set(
                    domain_mappings[
                        "gcc_control_id"
                    ].astype(int)
                )
                if not domain_mappings.empty
                else set()
            )

            coverage = (
                len(
                    mapped_ids
                )
                / len(
                    domain_control_ids
                )
                * 100
            )
        else:
            coverage = 0.0

        row[
            "crosswalk_coverage_pct"
        ] = round(
            coverage,
            2,
        )

        for overlay in OVERLAY_NAMES:
            if overlays.empty:
                overlay_match = False
            else:
                overlay_match = not overlays[
                    (
                        overlays[
                            "domain"
                        ] == domain
                    )
                    &
                    (
                        overlays[
                            "overlay"
                        ] == overlay
                    )
                ].empty

            row[
                overlay
            ] = yes_no(
                overlay_match
            )

        rows.append(
            row
        )

    matrix = pd.DataFrame(
        rows
    )

    preferred_order = [
        "domain",

        "NCA_ECC",
        "SAMA_CSF",
        "UAE_ISR",
        "QATAR_NIA",

        "NCA_ECC_control_count",
        "SAMA_CSF_control_count",
        "UAE_ISR_control_count",
        "QATAR_NIA_control_count",

        "nist_mapping",
        "iso_mapping",

        "nist_mapping_count",
        "iso_mapping_count",

        "crosswalk_coverage_pct",

        "data_residency",
        "arabic_logging",
        "national_cert_reporting",
        "local_hosting_mandate",
    ]

    matrix = matrix[
        preferred_order
    ]

    output = Path(
        output_path
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    csv_output = output.with_suffix(
        ".csv"
    )

    matrix.to_csv(
        csv_output,
        index=False,
    )

    with pd.ExcelWriter(
        output,
        engine="openpyxl",
    ) as writer:
        matrix.to_excel(
            writer,
            sheet_name="Applicability Matrix",
            index=False,
        )

        controls.to_excel(
            writer,
            sheet_name="Control Inventory",
            index=False,
        )

        if mappings.empty:
            pd.DataFrame(
                columns=[
                    "gcc_control_id",
                    "gcc_framework",
                    "gcc_control_ref",
                    "gcc_domain",
                    "reference_framework",
                    "reference_control_ref",
                    "mapping_strength",
                ]
            ).to_excel(
                writer,
                sheet_name="Crosswalk Detail",
                index=False,
            )
        else:
            mappings.to_excel(
                writer,
                sheet_name="Crosswalk Detail",
                index=False,
            )

        overlays.to_excel(
            writer,
            sheet_name="Overlay Detail",
            index=False,
        )

    print(
        f"Created: {output}"
    )

    print(
        f"Created: {csv_output}"
    )

    print()
    print(
        "Applicability matrix:"
    )

    print(
        matrix.to_string(
            index=False
        )
    )


def main() -> None:
    engine = create_engine(
        DATABASE_URL
    )

    build_applicability_matrix(
        engine,
        "output/applicability_matrix.xlsx",
    )


if __name__ == "__main__":
    main()
