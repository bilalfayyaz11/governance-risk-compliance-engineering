#!/usr/bin/env python3

import argparse
from pathlib import Path
from typing import Dict, List

import pandas as pd


REQUIRED_COLUMNS = [
    "risk_id",
    "ai_lifecycle_stage",
    "harm_category",
    "affected_rmf_function",
    "likelihood",
    "impact",
    "data_lineage_source",
    "bias_vector",
    "mapped_controls",
    "treatment_status",
]

SCHEMA_COLUMNS = REQUIRED_COLUMNS + ["risk_score"]

VALID_RMF_FUNCTIONS = {
    "Govern",
    "Map",
    "Measure",
    "Manage",
}

VALID_TREATMENT_STATUSES = {
    "Open",
    "Planned",
    "Mitigating",
    "Accepted",
    "Transferred",
    "Avoided",
    "Closed",
}


def load_register(path: str) -> pd.DataFrame:
    """
    Load an existing risk register CSV or initialize an empty register
    using the defined schema.
    """
    register_path = Path(path)

    if not register_path.exists():
        return pd.DataFrame(columns=SCHEMA_COLUMNS)

    df = pd.read_csv(register_path)

    missing = [
        column
        for column in SCHEMA_COLUMNS
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Existing register is missing columns: {', '.join(missing)}"
        )

    return df[SCHEMA_COLUMNS]


def validate_entry(entry: Dict) -> None:
    """
    Validate required fields and allowed values before a risk is added.
    """
    missing = [
        key
        for key in REQUIRED_COLUMNS
        if key not in entry
    ]

    if missing:
        raise ValueError(
            f"Risk entry missing required fields: {', '.join(missing)}"
        )

    empty = [
        key
        for key in REQUIRED_COLUMNS
        if entry.get(key) is None or str(entry.get(key)).strip() == ""
    ]

    if empty:
        raise ValueError(
            f"Risk entry contains empty required fields: {', '.join(empty)}"
        )

    if entry["affected_rmf_function"] not in VALID_RMF_FUNCTIONS:
        raise ValueError(
            "affected_rmf_function must be one of: "
            + ", ".join(sorted(VALID_RMF_FUNCTIONS))
        )

    if entry["treatment_status"] not in VALID_TREATMENT_STATUSES:
        raise ValueError(
            "Invalid treatment_status: "
            f"{entry['treatment_status']}"
        )

    for field in ("likelihood", "impact"):
        try:
            value = int(entry[field])
        except (TypeError, ValueError):
            raise ValueError(f"{field} must be an integer from 1 to 5")

        if not 1 <= value <= 5:
            raise ValueError(f"{field} must be between 1 and 5")


def add_risk_entry(df: pd.DataFrame, entry: Dict) -> pd.DataFrame:
    """
    Validate a risk entry, compute its risk score, and append it.
    """
    validate_entry(entry)

    risk_id = str(entry["risk_id"]).strip()

    if not df.empty and risk_id in df["risk_id"].astype(str).values:
        raise ValueError(f"Duplicate risk_id detected: {risk_id}")

    record = {
        key: entry[key]
        for key in REQUIRED_COLUMNS
    }

    record["likelihood"] = int(record["likelihood"])
    record["impact"] = int(record["impact"])
    record["risk_score"] = (
        record["likelihood"] * record["impact"]
    )

    return pd.concat(
        [df, pd.DataFrame([record], columns=SCHEMA_COLUMNS)],
        ignore_index=True,
    )


def export_register(df: pd.DataFrame, path: str) -> None:
    """
    Persist the risk register to CSV.
    """
    register_path = Path(path)
    register_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        register_path,
        index=False,
        columns=SCHEMA_COLUMNS,
    )


def build_initial_register() -> pd.DataFrame:
    """
    Build the initial clinical BCI AI risk register.
    """
    risks: List[Dict] = [
        {
            "risk_id": "AI-RISK-001",
            "ai_lifecycle_stage": "Monitoring",
            "harm_category": "Quality-of-service harm",
            "affected_rmf_function": "Measure",
            "likelihood": 4,
            "impact": 5,
            "data_lineage_source": (
                "Production BCI signal stream compared with "
                "baseline training distribution"
            ),
            "bias_vector": (
                "Population or device-distribution shift may "
                "degrade performance unevenly across cohorts"
            ),
            "mapped_controls": (
                "AI 600-1 supplemental: Harmful Bias or Homogenization; "
                "SP 800-53 RA-3, SI-4"
            ),
            "treatment_status": "Open",
        },
        {
            "risk_id": "AI-RISK-002",
            "ai_lifecycle_stage": "Training",
            "harm_category": "Representational harm",
            "affected_rmf_function": "Map",
            "likelihood": 4,
            "impact": 5,
            "data_lineage_source": (
                "Historical labeled BCI training dataset with "
                "incomplete cohort representation metadata"
            ),
            "bias_vector": (
                "Underrepresented patient cohorts may receive "
                "higher false-positive or false-negative rates"
            ),
            "mapped_controls": (
                "AI 600-1 supplemental: Harmful Bias or Homogenization; "
                "SP 800-53 RA-3, PT-2"
            ),
            "treatment_status": "Mitigating",
        },
        {
            "risk_id": "AI-RISK-003",
            "ai_lifecycle_stage": "Deployment",
            "harm_category": "Quality-of-service harm",
            "affected_rmf_function": "Govern",
            "likelihood": 4,
            "impact": 5,
            "data_lineage_source": (
                "Black-box neural-network model artifact and "
                "clinical inference output"
            ),
            "bias_vector": (
                "Clinicians may be unable to determine why a "
                "specific neural anomaly was flagged"
            ),
            "mapped_controls": (
                "AI 600-1 supplemental: Human-AI Configuration; "
                "SP 800-53 RA-3; no adequate SP 800-53 control fully "
                "addresses model explainability"
            ),
            "treatment_status": "Open",
        },
        {
            "risk_id": "AI-RISK-004",
            "ai_lifecycle_stage": "Deployment",
            "harm_category": "Quality-of-service harm",
            "affected_rmf_function": "Manage",
            "likelihood": 3,
            "impact": 5,
            "data_lineage_source": (
                "Live BCI sensor input entering the inference pipeline"
            ),
            "bias_vector": (
                "Crafted or corrupted signal inputs may induce "
                "incorrect anomaly classifications"
            ),
            "mapped_controls": (
                "AI 600-1 supplemental: Information Security; "
                "SP 800-53 SI-7, SI-4"
            ),
            "treatment_status": "Mitigating",
        },
        {
            "risk_id": "AI-RISK-005",
            "ai_lifecycle_stage": "Acquisition",
            "harm_category": "Informational harm",
            "affected_rmf_function": "Govern",
            "likelihood": 4,
            "impact": 4,
            "data_lineage_source": (
                "Third-party pretrained model, dependency metadata, "
                "training documentation, and supplier attestations"
            ),
            "bias_vector": (
                "Unknown training sources or undocumented preprocessing "
                "may conceal inherited bias and quality defects"
            ),
            "mapped_controls": (
                "AI 600-1 supplemental: Value-chain and component risk; "
                "SP 800-53 SR-3, SR-11"
            ),
            "treatment_status": "Open",
        },
        {
            "risk_id": "AI-RISK-006",
            "ai_lifecycle_stage": "Deployment",
            "harm_category": "Informational harm",
            "affected_rmf_function": "Manage",
            "likelihood": 3,
            "impact": 5,
            "data_lineage_source": (
                "Sensitive neural-signal features, model parameters, "
                "and inference interfaces"
            ),
            "bias_vector": (
                "Model inversion or inference attacks may expose "
                "patient-linked biometric or health information"
            ),
            "mapped_controls": (
                "AI 600-1 supplemental: Data Privacy; "
                "SP 800-53 PT-2, AC-4"
            ),
            "treatment_status": "Mitigating",
        },
        {
            "risk_id": "AI-RISK-007",
            "ai_lifecycle_stage": "Operation",
            "harm_category": "Allocative harm",
            "affected_rmf_function": "Govern",
            "likelihood": 4,
            "impact": 5,
            "data_lineage_source": (
                "Clinical decision-support alerts presented to physicians"
            ),
            "bias_vector": (
                "Automation bias may cause clinicians to over-weight "
                "model recommendations relative to independent judgment"
            ),
            "mapped_controls": (
                "AI 600-1 supplemental: Human-AI Configuration; "
                "SP 800-53 AT-3, RA-3; AI-specific human oversight "
                "controls remain necessary"
            ),
            "treatment_status": "Open",
        },
        {
            "risk_id": "AI-RISK-008",
            "ai_lifecycle_stage": "Retraining",
            "harm_category": "Quality-of-service harm",
            "affected_rmf_function": "Manage",
            "likelihood": 4,
            "impact": 5,
            "data_lineage_source": (
                "New clinical observations entering the retraining "
                "pipeline and replacement model artifact"
            ),
            "bias_vector": (
                "Retraining without cohort-level re-validation may "
                "introduce regression, drift, or new subgroup disparities"
            ),
            "mapped_controls": (
                "AI 600-1 supplemental: Harmful Bias or Homogenization; "
                "SP 800-53 SI-7, RA-3, RA-9"
            ),
            "treatment_status": "Open",
        },
    ]

    df = pd.DataFrame(columns=SCHEMA_COLUMNS)

    for risk in risks:
        df = add_risk_entry(df, risk)

    return df


def print_summary(df: pd.DataFrame) -> None:
    """
    Print a compact terminal summary of the register.
    """
    print("\nAI RISK REGISTER SUMMARY")
    print("=" * 80)

    display_columns = [
        "risk_id",
        "ai_lifecycle_stage",
        "affected_rmf_function",
        "likelihood",
        "impact",
        "risk_score",
        "treatment_status",
    ]

    print(
        df[display_columns].to_string(index=False)
    )

    print("\nRisk count:", len(df))
    print("Average risk score:", round(df["risk_score"].mean(), 2))
    print("Maximum risk score:", int(df["risk_score"].max()))
    print(
        "Open/unresolved risks:",
        int(
            df["treatment_status"]
            .isin(["Open", "Planned", "Mitigating"])
            .sum()
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clinical AI governance risk-register utility"
    )

    parser.add_argument(
        "--output",
        default="register/risk_register.csv",
        help="CSV output path",
    )

    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Rebuild the initial eight-risk register",
    )

    args = parser.parse_args()

    output_path = Path(args.output)

    if args.rebuild or not output_path.exists():
        df = build_initial_register()
        export_register(df, str(output_path))
    else:
        df = load_register(str(output_path))

    print_summary(df)


if __name__ == "__main__":
    main()
