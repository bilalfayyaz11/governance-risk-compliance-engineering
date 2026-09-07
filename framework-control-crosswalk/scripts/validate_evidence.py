from pathlib import Path
import pandas as pd

BASE = Path.home() / "crosswalk-lab"
OUTPUT = BASE / "output"
DATA = BASE / "data"

crosswalk_path = OUTPUT / "crosswalk.csv"
evidence_path = DATA / "evidence_requirements.csv"

crosswalk = pd.read_csv(crosswalk_path, dtype=str).fillna("")
evidence = pd.read_csv(evidence_path, dtype=str).fillna("")

required_crosswalk_columns = {
    "control_theme",
    "mapping_status",
}

required_evidence_columns = {
    "control_theme",
    "mapping_status",
    "required_evidence",
}

missing_crosswalk = required_crosswalk_columns - set(crosswalk.columns)
missing_evidence = required_evidence_columns - set(evidence.columns)

if missing_crosswalk:
    raise ValueError(
        f"Crosswalk missing required columns: {sorted(missing_crosswalk)}"
    )

if missing_evidence:
    raise ValueError(
        f"Evidence catalog missing required columns: {sorted(missing_evidence)}"
    )

# Validate evidence against both theme and mapping status so that
# Equivalent and Gap requirements remain distinguishable.
validated = crosswalk.merge(
    evidence,
    on=["control_theme", "mapping_status"],
    how="left",
    validate="many_to_one",
)

validated["required_evidence"] = (
    validated["required_evidence"]
    .fillna("")
    .str.strip()
)

validated["evidence_validation"] = validated["required_evidence"].apply(
    lambda value: "PASS" if value else "MISSING"
)

validated["evidence_gap"] = validated["required_evidence"].apply(
    lambda value: "" if value else "Evidence requirement not defined"
)

validated_path = OUTPUT / "crosswalk_with_evidence.csv"
validated.to_csv(validated_path, index=False)

missing = validated[
    validated["evidence_validation"] == "MISSING"
].copy()

missing_path = OUTPUT / "evidence_gaps.csv"
missing.to_csv(missing_path, index=False)

print(f"Crosswalk rows validated: {len(validated)}")
print(
    "Evidence requirements matched:",
    (validated["evidence_validation"] == "PASS").sum(),
)
print(
    "Missing evidence definitions:",
    (validated["evidence_validation"] == "MISSING").sum(),
)

print(f"PASS: {validated_path}")
print(f"PASS: {missing_path}")
