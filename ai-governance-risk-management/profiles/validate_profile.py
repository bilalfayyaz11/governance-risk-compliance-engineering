#!/usr/bin/env python3

from pathlib import Path
from typing import List

import yaml
from jsonschema import validate
from jsonschema.exceptions import ValidationError


PROFILE_SCHEMA = {
    "type": "object",
    "required": [
        "system",
        "Govern",
        "Map",
        "Measure",
        "Manage",
    ],
    "properties": {
        "system": {
            "type": "object",
            "required": [
                "name",
                "description",
                "intended_use",
                "prohibited_use",
            ],
        },
        "Govern": {"type": "object"},
        "Map": {"type": "object"},
        "Measure": {"type": "object"},
        "Manage": {"type": "object"},
    },
}


RMF_FUNCTIONS = [
    "Govern",
    "Map",
    "Measure",
    "Manage",
]


def load_profile(path: str) -> dict:
    """Load YAML profile mapping."""
    profile_path = Path(path)

    if not profile_path.exists():
        raise FileNotFoundError(
            f"Profile not found: {profile_path}"
        )

    with profile_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        profile = yaml.safe_load(file)

    if not isinstance(profile, dict):
        raise ValueError(
            "Profile root must be a YAML mapping."
        )

    return profile


def is_populated(value) -> bool:
    """
    Return True when a YAML value contains meaningful data.
    """
    if value is None:
        return False

    if isinstance(value, str):
        return bool(value.strip())

    if isinstance(value, dict):
        return bool(value)

    if isinstance(value, list):
        return bool(value)

    return True


def validate_profile_completeness(
    profile: dict,
) -> List[str]:
    """
    Check that Govern, Map, Measure, Manage sections exist
    and each has at least 3 populated sub-fields.

    Return a list of missing or incomplete sections.
    """
    gaps: List[str] = []

    for function in RMF_FUNCTIONS:
        if function not in profile:
            gaps.append(
                f"{function}: section missing"
            )
            continue

        section = profile[function]

        if not isinstance(section, dict):
            gaps.append(
                f"{function}: section must be a mapping"
            )
            continue

        populated = [
            key
            for key, value in section.items()
            if is_populated(value)
        ]

        if len(populated) < 3:
            gaps.append(
                f"{function}: only {len(populated)} "
                "populated sub-fields; minimum is 3"
            )

    return gaps


def validate_schema(profile: dict) -> None:
    """
    Validate high-level profile structure with jsonschema.
    """
    validate(
        instance=profile,
        schema=PROFILE_SCHEMA,
    )


def print_summary(profile: dict) -> None:
    print(
        "\nAI RMF PROFILE VALIDATION SUMMARY"
    )
    print("=" * 72)

    for function in RMF_FUNCTIONS:
        section = profile.get(
            function,
            {},
        )

        if isinstance(section, dict):
            populated = [
                key
                for key, value in section.items()
                if is_populated(value)
            ]

            print(
                f"{function:<8} "
                f"populated sub-fields: "
                f"{len(populated)}"
            )

            for key in populated:
                print(
                    f"  - {key}"
                )
        else:
            print(
                f"{function:<8} INVALID"
            )

        print()


def main() -> int:
    path = (
        "profiles/use_case_profile.yaml"
    )

    try:
        profile = load_profile(path)

        validate_schema(profile)

        gaps = (
            validate_profile_completeness(
                profile
            )
        )

    except (
        FileNotFoundError,
        ValueError,
        ValidationError,
        yaml.YAMLError,
    ) as exc:
        print(
            f"FAIL | Profile validation "
            f"error: {exc}"
        )
        return 1

    print_summary(profile)

    if gaps:
        print(
            "PROFILE STATUS: INCOMPLETE"
        )

        for gap in gaps:
            print(
                f"FAIL | {gap}"
            )

        return 1

    print(
        "PASS | JSON Schema "
        "validation successful"
    )

    print(
        "PASS | Govern section complete"
    )

    print(
        "PASS | Map section complete"
    )

    print(
        "PASS | Measure section complete"
    )

    print(
        "PASS | Manage section complete"
    )

    print(
        "\nPROFILE STATUS: COMPLETE"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
