#!/usr/bin/env python3

import re
from typing import Dict, List

from sqlalchemy import create_engine, text


DATABASE_URL = "postgresql+psycopg2:///gcc_grc_map"


OVERLAY_PATTERNS: Dict[str, List[str]] = {
    "data_residency": [
        r"\bdata residency\b",
        r"\bin[- ]country\b",
        r"\bwithin (?:the )?kingdom\b",
        r"\bwithin qatar\b",
        r"\bwithin (?:the )?uae\b",
        r"\bwithin saudi arabia\b",
        r"\bcross[- ]border data\b",
        r"\bdomestic processing\b",
        r"\bregulated data.*(?:stored|processed).*(?:kingdom|qatar|uae|country)\b",
        r"\brestricted.*information.*remain within\b",
    ],

    "arabic_logging": [
        r"\barabic\b.*\b(?:log|logs|logging|audit|evidence|report|reporting|record|records)\b",
        r"\b(?:log|logs|logging|audit|evidence|report|reporting|record|records)\b.*\barabic\b",
        r"\blocal[- ]language\b.*\b(?:audit|log|report|evidence)\b",
    ],

    "national_cert_reporting": [
        r"\bnational cert\b",
        r"\bcert\b.*\b(?:report|notify|notification)\b",
        r"\bnational cybersecurity authority\b",
        r"\bnational incident response\b",
        r"\bcompetent national cybersecurity authority\b",
        r"\bcybersecurity authority\b.*\b(?:report|reported|notify|notification)\b",
        r"\b(?:incident|incidents)\b.*\b(?:reported|report|notify|notified)\b.*\b(?:authority|cert|regulator)\b",
        r"\bregulator\b.*\b(?:incident|notification|report)\b",
    ],

    "local_hosting_mandate": [
        r"\blocal hosting\b",
        r"\blocal cloud\b",
        r"\blocal cloud regions?\b",
        r"\blocal or nationally approved hosting\b",
        r"\bnationally approved hosting\b",
        r"\bapproved (?:uae|qatar|saudi|national) (?:hosting|locations?|cloud)\b",
        r"\bhosted in approved (?:uae|qatar|saudi|national) locations?\b",
        r"\bin[- ]country infrastructure\b",
        r"\bdomestic cloud\b",
        r"\bregulated (?:services|workloads).*hosting\b",
    ],
}


def normalize_text(value: str) -> str:
    """
    Normalize control text for deterministic overlay detection.
    """
    if value is None:
        return ""

    value = value.lower()

    value = re.sub(
        r"\s+",
        " ",
        value,
    ).strip()

    return value


def detect_overlay_requirements(
    control_description: str,
) -> List[str]:
    """
    Scan regulatory control text for GCC-specific overlay triggers.

    Returns a deterministic list of matched overlay tags.
    """
    normalized = normalize_text(
        control_description
    )

    matches: List[str] = []

    for overlay_name, patterns in OVERLAY_PATTERNS.items():
        for pattern in patterns:
            if re.search(
                pattern,
                normalized,
                flags=re.IGNORECASE,
            ):
                matches.append(
                    overlay_name
                )
                break

    return sorted(
        set(matches)
    )


def get_overlay_ids(engine) -> Dict[str, int]:
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT
                    id,
                    name
                FROM overlays
                ORDER BY name
                """
            )
        ).mappings().all()

    return {
        row["name"]: int(row["id"])
        for row in rows
    }


def validate_overlay_definitions(
    engine,
) -> None:
    required = {
        "data_residency",
        "arabic_logging",
        "national_cert_reporting",
        "local_hosting_mandate",
    }

    overlay_ids = get_overlay_ids(
        engine
    )

    present = set(
        overlay_ids
    )

    missing = required - present

    if missing:
        raise ValueError(
            "Missing overlay definitions: "
            + ", ".join(
                sorted(missing)
            )
        )


def tag_controls_with_overlays(
    engine,
) -> int:
    """
    Recompute all overlay mappings.

    Existing junction rows are removed before detection so repeated
    execution remains deterministic and stale tags do not survive
    changes to detection logic.
    """
    validate_overlay_definitions(
        engine
    )

    overlay_ids = get_overlay_ids(
        engine
    )

    with engine.connect() as conn:
        controls = conn.execute(
            text(
                """
                SELECT
                    c.id,
                    c.control_ref,
                    c.title,
                    c.description,
                    f.name AS framework_name
                FROM controls c
                JOIN frameworks f
                    ON f.id = c.framework_id
                ORDER BY
                    f.name,
                    c.control_ref
                """
            )
        ).mappings().all()

    tagged = 0

    with engine.begin() as conn:
        conn.execute(
            text(
                "DELETE FROM control_overlays"
            )
        )

        for control in controls:
            searchable_text = (
                f"{control['title']} "
                f"{control['description']}"
            )

            matches = (
                detect_overlay_requirements(
                    searchable_text
                )
            )

            for overlay_name in matches:
                overlay_id = overlay_ids[
                    overlay_name
                ]

                conn.execute(
                    text(
                        """
                        INSERT INTO control_overlays (
                            control_id,
                            overlay_id
                        )
                        VALUES (
                            :control_id,
                            :overlay_id
                        )
                        ON CONFLICT (
                            control_id,
                            overlay_id
                        )
                        DO NOTHING
                        """
                    ),
                    {
                        "control_id":
                            control["id"],
                        "overlay_id":
                            overlay_id,
                    },
                )

                tagged += 1

    return tagged


def print_overlay_summary(
    engine,
) -> None:
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT
                    o.name AS overlay,
                    COUNT(co.control_id) AS tagged_controls
                FROM overlays o
                LEFT JOIN control_overlays co
                    ON co.overlay_id = o.id
                GROUP BY
                    o.id,
                    o.name
                ORDER BY o.name
                """
            )
        ).mappings().all()

    print(
        "\nOVERLAY SUMMARY"
    )

    print(
        "=" * 60
    )

    for row in rows:
        print(
            f"{row['overlay']:<28} "
            f"{row['tagged_controls']} controls"
        )


def print_tagged_controls(
    engine,
) -> None:
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT
                    f.name AS framework,
                    c.control_ref,
                    c.title,
                    o.name AS overlay
                FROM control_overlays co
                JOIN controls c
                    ON c.id = co.control_id
                JOIN frameworks f
                    ON f.id = c.framework_id
                JOIN overlays o
                    ON o.id = co.overlay_id
                ORDER BY
                    o.name,
                    f.name,
                    c.control_ref
                """
            )
        ).mappings().all()

    print(
        "\nTAGGED CONTROLS"
    )

    print(
        "=" * 100
    )

    for row in rows:
        print(
            f"{row['overlay']:<27} | "
            f"{row['framework']:<12} | "
            f"{row['control_ref']:<12} | "
            f"{row['title']}"
        )


def main() -> None:
    engine = create_engine(
        DATABASE_URL
    )

    tagged = tag_controls_with_overlays(
        engine
    )

    print(
        f"Overlay mappings created: {tagged}"
    )

    print_overlay_summary(
        engine
    )

    print_tagged_controls(
        engine
    )


if __name__ == "__main__":
    main()
