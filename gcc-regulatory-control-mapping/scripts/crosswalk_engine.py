#!/usr/bin/env python3

import argparse
import math
import re
from collections import Counter
from typing import Dict, List, Literal, Tuple

from sqlalchemy import create_engine, text


DATABASE_URL = "postgresql+psycopg2:///gcc_grc_map"

MappingStrength = Literal[
    "exact",
    "partial",
    "related",
]


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "shall",
    "that",
    "the",
    "to",
    "with",
    "within",
}


DOMAIN_SYNONYMS = {
    "cybersecurity governance": "governance",
    "information security governance": "governance",
    "governance": "governance",

    "cybersecurity risk management": "risk management",
    "information security risk management": "risk management",
    "risk management": "risk management",

    "identity and access management": "identity and access management",

    "logging and monitoring": "logging and monitoring",

    "incident response": "incident response",

    "business continuity": "business continuity",

    "third-party security": "third-party security",

    "vulnerability management": "vulnerability management",

    "cryptography": "cryptography",

    "data protection": "data protection",

    "asset management": "asset management",

    "cloud security": "cloud security",

    "change management": "change management",

    "compliance": "compliance",
}


REFERENCE_FRAMEWORKS = {
    "NIST_800_53",
    "ISO_27001",
}


GCC_FRAMEWORKS = {
    "NCA_ECC",
    "SAMA_CSF",
    "UAE_ISR",
    "QATAR_NIA",
}


def normalize_text(value: str) -> str:
    value = value.lower()

    value = re.sub(
        r"[^a-z0-9\s-]",
        " ",
        value,
    )

    value = re.sub(
        r"\s+",
        " ",
        value,
    ).strip()

    return value


def tokenize(value: str) -> List[str]:
    text_value = normalize_text(
        value
    )

    tokens = [
        token
        for token in text_value.split()
        if (
            token not in STOPWORDS
            and len(token) > 2
        )
    ]

    return tokens


def cosine_similarity(
    left: str,
    right: str,
) -> float:
    left_tokens = tokenize(
        left
    )

    right_tokens = tokenize(
        right
    )

    if not left_tokens or not right_tokens:
        return 0.0

    left_counts = Counter(
        left_tokens
    )

    right_counts = Counter(
        right_tokens
    )

    vocabulary = set(
        left_counts
    ) | set(
        right_counts
    )

    dot_product = sum(
        left_counts[token]
        * right_counts[token]
        for token in vocabulary
    )

    left_norm = math.sqrt(
        sum(
            value * value
            for value in left_counts.values()
        )
    )

    right_norm = math.sqrt(
        sum(
            value * value
            for value in right_counts.values()
        )
    )

    if (
        left_norm == 0
        or right_norm == 0
    ):
        return 0.0

    return (
        dot_product
        / (
            left_norm
            * right_norm
        )
    )


def normalize_domain(
    value: str,
) -> str:
    normalized = normalize_text(
        value
    )

    return DOMAIN_SYNONYMS.get(
        normalized,
        normalized,
    )


def domain_similarity(
    left: str,
    right: str,
) -> float:
    left_domain = normalize_domain(
        left
    )

    right_domain = normalize_domain(
        right
    )

    if left_domain == right_domain:
        return 1.0

    left_tokens = set(
        tokenize(
            left_domain
        )
    )

    right_tokens = set(
        tokenize(
            right_domain
        )
    )

    if not left_tokens or not right_tokens:
        return 0.0

    intersection = (
        left_tokens
        & right_tokens
    )

    union = (
        left_tokens
        | right_tokens
    )

    return (
        len(intersection)
        / len(union)
    )


def get_control(
    control_id: int,
    engine,
) -> Dict:
    with engine.connect() as conn:
        row = conn.execute(
            text(
                """
                SELECT
                    c.id,
                    f.name AS framework_name,
                    f.version,
                    c.control_ref,
                    c.domain,
                    c.title,
                    c.description,
                    c.control_type
                FROM controls c
                JOIN frameworks f
                    ON f.id = c.framework_id
                WHERE c.id = :control_id
                """
            ),
            {
                "control_id":
                    control_id,
            },
        ).mappings().first()

    if row is None:
        raise ValueError(
            f"Control ID not found: {control_id}"
        )

    return dict(
        row
    )


def generate_crosswalk_candidates(
    gcc_control_id: int,
    reference_framework: str,
    engine,
) -> List[Dict]:
    """
    Generate ranked reference-framework candidates.

    Hybrid score:
      45% domain similarity
      20% title similarity
      35% description similarity

    This weighting is intentional because regulatory controls
    use short jargon-heavy descriptions. Domain alignment is
    generally more reliable than raw fuzzy string matching alone.
    """
    if reference_framework not in REFERENCE_FRAMEWORKS:
        raise ValueError(
            "reference_framework must be "
            "'NIST_800_53' or 'ISO_27001'"
        )

    source = get_control(
        gcc_control_id,
        engine,
    )

    if source[
        "framework_name"
    ] not in GCC_FRAMEWORKS:
        raise ValueError(
            f"Control {gcc_control_id} "
            "is not a GCC framework control"
        )

    with engine.connect() as conn:
        candidates = conn.execute(
            text(
                """
                SELECT
                    c.id,
                    c.control_ref,
                    c.domain,
                    c.title,
                    c.description
                FROM controls c
                JOIN frameworks f
                    ON f.id = c.framework_id
                WHERE f.name = :framework_name
                ORDER BY c.control_ref
                """
            ),
            {
                "framework_name":
                    reference_framework,
            },
        ).mappings().all()

    results: List[Dict] = []

    source_title_text = (
        f"{source['title']} "
        f"{source['domain']}"
    )

    source_description_text = (
        f"{source['title']} "
        f"{source['description']}"
    )

    for candidate in candidates:
        d_score = domain_similarity(
            source["domain"],
            candidate["domain"],
        )

        title_score = cosine_similarity(
            source_title_text,
            (
                f"{candidate['title']} "
                f"{candidate['domain']}"
            ),
        )

        description_score = cosine_similarity(
            source_description_text,
            (
                f"{candidate['title']} "
                f"{candidate['description']}"
            ),
        )

        final_score = (
            0.45 * d_score
            + 0.20 * title_score
            + 0.35 * description_score
        )

        results.append(
            {
                "source_control_id":
                    source["id"],

                "source_control_ref":
                    source["control_ref"],

                "source_framework":
                    source["framework_name"],

                "target_control_id":
                    candidate["id"],

                "target_control_ref":
                    candidate["control_ref"],

                "target_framework":
                    reference_framework,

                "target_title":
                    candidate["title"],

                "domain_similarity":
                    round(
                        d_score,
                        4,
                    ),

                "title_similarity":
                    round(
                        title_score,
                        4,
                    ),

                "description_similarity":
                    round(
                        description_score,
                        4,
                    ),

                "similarity_score":
                    round(
                        final_score,
                        4,
                    ),
            }
        )

    results.sort(
        key=lambda item:
            item[
                "similarity_score"
            ],
        reverse=True,
    )

    return results[
        :5
    ]


def normalize_pair(
    source_id: int,
    target_id: int,
) -> Tuple[int, int]:
    if source_id == target_id:
        raise ValueError(
            "A control cannot map to itself"
        )

    return (
        min(
            source_id,
            target_id,
        ),
        max(
            source_id,
            target_id,
        ),
    )


def commit_crosswalk(
    source_id: int,
    target_id: int,
    strength: MappingStrength,
    rationale: str,
    engine,
) -> None:
    """
    Persist an analyst-confirmed crosswalk.

    Pair order is normalized so A-B and B-A become the
    same stored relationship.
    """
    if strength not in {
        "exact",
        "partial",
        "related",
    }:
        raise ValueError(
            f"Invalid mapping strength: {strength}"
        )

    if not rationale.strip():
        raise ValueError(
            "Mapping rationale cannot be empty"
        )

    left_id, right_id = normalize_pair(
        source_id,
        target_id,
    )

    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO crosswalks (
                    source_control_id,
                    target_control_id,
                    mapping_strength,
                    rationale
                )
                VALUES (
                    :source_control_id,
                    :target_control_id,
                    CAST(
                        :mapping_strength
                        AS mapping_strength_enum
                    ),
                    :rationale
                )
                ON CONFLICT (
                    source_control_id,
                    target_control_id
                )
                DO UPDATE SET
                    mapping_strength =
                        EXCLUDED.mapping_strength,
                    rationale =
                        EXCLUDED.rationale
                """
            ),
            {
                "source_control_id":
                    left_id,
                "target_control_id":
                    right_id,
                "mapping_strength":
                    strength,
                "rationale":
                    rationale.strip(),
            },
        )


def get_control_id(
    framework_name: str,
    control_ref: str,
    engine,
) -> int:
    with engine.connect() as conn:
        control_id = conn.execute(
            text(
                """
                SELECT c.id
                FROM controls c
                JOIN frameworks f
                    ON f.id = c.framework_id
                WHERE
                    f.name = :framework_name
                    AND c.control_ref = :control_ref
                """
            ),
            {
                "framework_name":
                    framework_name,
                "control_ref":
                    control_ref,
            },
        ).scalar()

    if control_id is None:
        raise ValueError(
            f"Control not found: "
            f"{framework_name} {control_ref}"
        )

    return int(
        control_id
    )


ANALYST_MAPPINGS = [
    {
        "source":
            (
                "NCA_ECC",
                "NCA-2-2",
            ),
        "target":
            (
                "NIST_800_53",
                "AC-6",
            ),
        "strength":
            "exact",
        "rationale":
            "Both controls explicitly require least-privilege access for privileged or authorized users.",
    },
    {
        "source":
            (
                "NCA_ECC",
                "NCA-2-2",
            ),
        "target":
            (
                "ISO_27001",
                "A.5.15",
            ),
        "strength":
            "partial",
        "rationale":
            "ISO access-control requirements cover the same access governance objective but are broader than the NCA privileged-access requirement.",
    },
    {
        "source":
            (
                "NCA_ECC",
                "NCA-2-5",
            ),
        "target":
            (
                "NIST_800_53",
                "AU-6",
            ),
        "strength":
            "exact",
        "rationale":
            "Both require security event or audit record review and analysis to identify suspicious activity.",
    },
    {
        "source":
            (
                "NCA_ECC",
                "NCA-2-5",
            ),
        "target":
            (
                "ISO_27001",
                "A.8.15",
            ),
        "strength":
            "exact",
        "rationale":
            "Both require generation retention protection and analysis of security-relevant logging information.",
    },
    {
        "source":
            (
                "NCA_ECC",
                "NCA-2-7",
            ),
        "target":
            (
                "NIST_800_53",
                "IR-6",
            ),
        "strength":
            "partial",
        "rationale":
            "NIST IR-6 addresses incident reporting but does not itself impose the Saudi national regulator reporting timeline.",
    },
    {
        "source":
            (
                "NCA_ECC",
                "NCA-2-3",
            ),
        "target":
            (
                "ISO_27001",
                "A.5.31",
            ),
        "strength":
            "related",
        "rationale":
            "ISO 27001 requires identification of legal and regulatory obligations but does not directly impose Saudi in-country data residency.",
    },
    {
        "source":
            (
                "SAMA_CSF",
                "SAMA-2-1",
            ),
        "target":
            (
                "NIST_800_53",
                "RA-3",
            ),
        "strength":
            "exact",
        "rationale":
            "Both controls require formal cybersecurity risk identification assessment and treatment inputs.",
    },
    {
        "source":
            (
                "SAMA_CSF",
                "SAMA-3-3",
            ),
        "target":
            (
                "NIST_800_53",
                "SI-4",
            ),
        "strength":
            "partial",
        "rationale":
            "Both address active security monitoring although SI-4 includes a wider set of system-monitoring objectives.",
    },
    {
        "source":
            (
                "SAMA_CSF",
                "SAMA-3-5",
            ),
        "target":
            (
                "ISO_27001",
                "A.5.19",
            ),
        "strength":
            "exact",
        "rationale":
            "Both require supplier security requirements and management of third-party information security risk.",
    },
    {
        "source":
            (
                "UAE_ISR",
                "ISR-3-2",
            ),
        "target":
            (
                "NIST_800_53",
                "AC-3",
            ),
        "strength":
            "partial",
        "rationale":
            "Both enforce logical access authorization although the UAE requirement additionally emphasizes business justification and least privilege.",
    },
    {
        "source":
            (
                "UAE_ISR",
                "ISR-3-4",
            ),
        "target":
            (
                "ISO_27001",
                "A.8.15",
            ),
        "strength":
            "exact",
        "rationale":
            "Both address generation retention protection and review of audit logs for security monitoring.",
    },
    {
        "source":
            (
                "UAE_ISR",
                "ISR-3-5",
            ),
        "target":
            (
                "ISO_27001",
                "A.5.31",
            ),
        "strength":
            "related",
        "rationale":
            "ISO compliance obligations support regulatory evidence requirements but do not explicitly require Arabic-language audit evidence.",
    },
    {
        "source":
            (
                "QATAR_NIA",
                "NIA-2-7",
            ),
        "target":
            (
                "NIST_800_53",
                "IR-6",
            ),
        "strength":
            "partial",
        "rationale":
            "IR-6 supports incident reporting but Qatar-specific national CERT notification obligations remain an overlay requirement.",
    },
    {
        "source":
            (
                "QATAR_NIA",
                "NIA-2-8",
            ),
        "target":
            (
                "NIST_800_53",
                "SR-3",
            ),
        "strength":
            "partial",
        "rationale":
            "Both address supply-chain risk but the Qatar requirement includes local contractual and assurance obligations.",
    },
    {
        "source":
            (
                "QATAR_NIA",
                "NIA-2-11",
            ),
        "target":
            (
                "ISO_27001",
                "A.8.8",
            ),
        "strength":
            "exact",
        "rationale":
            "Both require identification evaluation prioritization and remediation of technical vulnerabilities.",
    },
]


def seed_analyst_crosswalks(
    engine,
) -> int:
    committed = 0

    for mapping in ANALYST_MAPPINGS:
        source_id = get_control_id(
            mapping[
                "source"
            ][0],
            mapping[
                "source"
            ][1],
            engine,
        )

        target_id = get_control_id(
            mapping[
                "target"
            ][0],
            mapping[
                "target"
            ][1],
            engine,
        )

        commit_crosswalk(
            source_id,
            target_id,
            mapping[
                "strength"
            ],
            mapping[
                "rationale"
            ],
            engine,
        )

        committed += 1

    return committed


def print_crosswalk_summary(
    engine,
) -> None:
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT
                    c1.id AS stored_left_id,
                    f1.name AS framework_1,
                    c1.control_ref AS control_1,
                    c2.id AS stored_right_id,
                    f2.name AS framework_2,
                    c2.control_ref AS control_2,
                    cw.mapping_strength,
                    cw.rationale
                FROM crosswalks cw
                JOIN controls c1
                    ON c1.id = cw.source_control_id
                JOIN frameworks f1
                    ON f1.id = c1.framework_id
                JOIN controls c2
                    ON c2.id = cw.target_control_id
                JOIN frameworks f2
                    ON f2.id = c2.framework_id
                ORDER BY
                    cw.mapping_strength,
                    framework_1,
                    control_1
                """
            )
        ).mappings().all()

    for row in rows:
        print(
            f"{row['framework_1']} "
            f"{row['control_1']} "
            f"<-> "
            f"{row['framework_2']} "
            f"{row['control_2']} "
            f"[{row['mapping_strength']}]"
        )


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--seed",
        action="store_true",
        help="Commit analyst-reviewed mappings",
    )

    parser.add_argument(
        "--framework",
        choices=sorted(
            REFERENCE_FRAMEWORKS
        ),
    )

    parser.add_argument(
        "--control-id",
        type=int,
    )

    args = parser.parse_args()

    engine = create_engine(
        DATABASE_URL
    )

    if args.seed:
        count = (
            seed_analyst_crosswalks(
                engine
            )
        )

        print(
            f"Committed {count} analyst-reviewed mappings"
        )

        print_crosswalk_summary(
            engine
        )

        return

    if (
        args.framework
        and args.control_id
    ):
        matches = (
            generate_crosswalk_candidates(
                args.control_id,
                args.framework,
                engine,
            )
        )

        for rank, item in enumerate(
            matches,
            start=1,
        ):
            print(
                f"{rank}. "
                f"{item['target_framework']} "
                f"{item['target_control_ref']} "
                f"| {item['target_title']} "
                f"| score={item['similarity_score']}"
            )

        return

    parser.print_help()


if __name__ == "__main__":
    main()
