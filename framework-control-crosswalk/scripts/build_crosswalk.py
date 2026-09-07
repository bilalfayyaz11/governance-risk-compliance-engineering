from pathlib import Path
import pandas as pd

BASE = Path.home() / "crosswalk-lab"
DATA = BASE / "data"
OUTPUT = BASE / "output"


def load_catalog(filepath: str, source_name: str) -> pd.DataFrame:
    """
    Load a normalized control catalog and tag it with its source framework.

    Expected normalized schema:
        control_id, control_title, category
    """
    df = pd.read_csv(filepath, dtype=str)

    expected = {"control_id", "control_title", "category"}
    missing = expected - set(df.columns)

    if missing:
        raise ValueError(
            f"{source_name} catalog missing required columns: {sorted(missing)}"
        )

    df = df[["control_id", "control_title", "category"]].copy()
    df["source"] = source_name

    return df


def lookup_control(df: pd.DataFrame, control_id: str) -> dict:
    """
    Resolve a control by ID.

    Returns empty values if the control ID is blank.
    Raises an error if a non-empty ID is not found.
    """
    if not control_id:
        return {
            "control_id": "",
            "control_title": "",
            "category": "",
        }

    match = df[df["control_id"] == control_id]

    if match.empty:
        raise ValueError(f"Control ID not found: {control_id}")

    row = match.iloc[0]

    return {
        "control_id": row["control_id"],
        "control_title": row["control_title"],
        "category": row["category"],
    }


def build_mapping(
    iso_df: pd.DataFrame,
    nist_df: pd.DataFrame,
    sama_df: pd.DataFrame,
    mapping_rules: list,
) -> pd.DataFrame:
    """
    Build framework crosswalk rows from mapping rules.
    """
    rows = []

    for rule in mapping_rules:
        iso = lookup_control(iso_df, rule.get("iso", ""))
        nist = lookup_control(nist_df, rule.get("nist", ""))
        sama = lookup_control(sama_df, rule.get("sama", ""))

        has_gap = any(
            not value
            for value in [
                rule.get("iso", ""),
                rule.get("nist", ""),
                rule.get("sama", ""),
            ]
        )

        status = "Gap" if has_gap else rule.get("status", "Equivalent")

        rows.append(
            {
                "control_theme": rule["theme"],
                "mapping_status": status,
                "mapping_rationale": rule["rationale"],
                "iso_control_id": iso["control_id"],
                "iso_control_title": iso["control_title"],
                "iso_category": iso["category"],
                "nist_control_id": nist["control_id"],
                "nist_control_title": nist["control_title"],
                "nist_category": nist["category"],
                "sama_control_id": sama["control_id"],
                "sama_control_title": sama["control_title"],
                "sama_category": sama["category"],
            }
        )

    return pd.DataFrame(rows)


def find_gaps(crosswalk_df: pd.DataFrame) -> pd.DataFrame:
    """
    Return crosswalk rows containing mapping gaps.
    """
    return crosswalk_df[
        crosswalk_df["mapping_status"] == "Gap"
    ].copy()


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)

    iso_df = load_catalog(
        DATA / "normalized_iso27001.csv",
        "ISO27001",
    )

    nist_df = load_catalog(
        DATA / "normalized_nist_csf.csv",
        "NIST_CSF",
    )

    sama_df = load_catalog(
        DATA / "normalized_sama_csf.csv",
        "SAMA_CSF",
    )

    mapping_rules = [
        {
            "theme": "Policy",
            "iso": "A.5.1",
            "nist": "GV.PO-01",
            "sama": "3.1.3",
            "status": "Equivalent",
            "rationale": (
                "All three frameworks require documented and governed "
                "cybersecurity or information security policy."
            ),
        },
        {
            "theme": "Vulnerability Management",
            "iso": "A.8.8",
            "nist": "ID.RA-01",
            "sama": "3.3.17",
            "status": "Equivalent",
            "rationale": (
                "Each framework requires vulnerabilities to be identified "
                "and managed through an established process."
            ),
        },
        {
            "theme": "Monitoring",
            "iso": "A.8.16",
            "nist": "DE.CM-01",
            "sama": "3.3.14",
            "status": "Equivalent",
            "rationale": (
                "The controls align around continuous security monitoring, "
                "event detection, and operational visibility."
            ),
        },
        {
            "theme": "Incident Management",
            "iso": "A.5.24",
            "nist": "RS.MA-01",
            "sama": "3.3.15",
            "status": "Equivalent",
            "rationale": (
                "All three frameworks require formal preparation and "
                "execution of incident-management activities."
            ),
        },
        {
            "theme": "Identity and Access Management",
            "iso": "A.5.15",
            "nist": "PR.AA-01",
            "sama": "3.3.5",
            "status": "Equivalent",
            "rationale": (
                "Controls establish identity, authorization, and access "
                "governance expectations."
            ),
        },
        {
            "theme": "Configuration Management",
            "iso": "A.8.9",
            "nist": "PR.PS-01",
            "sama": "",
            "status": "Gap",
            "rationale": (
                "ISO and NIST have explicit configuration-management "
                "references in this catalog extract, while no directly "
                "mapped SAMA control was selected."
            ),
        },
        {
            "theme": "Logging",
            "iso": "A.8.15",
            "nist": "DE.CM-01",
            "sama": "3.3.14",
            "status": "Equivalent",
            "rationale": (
                "Logging and monitoring requirements support detection "
                "and security-event management across the frameworks."
            ),
        },
        {
            "theme": "Recovery Planning",
            "iso": "",
            "nist": "RC.RP-01",
            "sama": "",
            "status": "Gap",
            "rationale": (
                "A recovery-specific NIST outcome is present in the sample "
                "catalog, but equivalent ISO and SAMA controls were not "
                "included in this simplified extract."
            ),
        },
    ]

    crosswalk_df = build_mapping(
        iso_df,
        nist_df,
        sama_df,
        mapping_rules,
    )

    gaps_df = find_gaps(crosswalk_df)

    crosswalk_path = OUTPUT / "crosswalk.csv"
    gaps_path = OUTPUT / "crosswalk_gaps.csv"

    crosswalk_df.to_csv(crosswalk_path, index=False)
    gaps_df.to_csv(gaps_path, index=False)

    print(f"Crosswalk rows: {len(crosswalk_df)}")
    print(
        "Equivalent mappings:",
        (crosswalk_df["mapping_status"] == "Equivalent").sum(),
    )
    print(
        "Gap mappings:",
        (crosswalk_df["mapping_status"] == "Gap").sum(),
    )

    print(f"PASS: {crosswalk_path}")
    print(f"PASS: {gaps_path}")
