from pathlib import Path
from datetime import datetime, timezone
import pandas as pd

BASE = Path.home() / "crosswalk-lab"
OUTPUT = BASE / "output"


def safe(value) -> str:
    """Return Markdown-safe display value."""
    if pd.isna(value) or str(value).strip() == "":
        return "—"

    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def generate_report(crosswalk_csv: str, output_path: str) -> None:
    """
    Generate a stakeholder-ready Markdown report from the validated
    multi-framework crosswalk.
    """
    crosswalk_path = Path(crosswalk_csv)
    report_path = Path(output_path)

    df = pd.read_csv(crosswalk_path, dtype=str).fillna("")

    required = {
        "control_theme",
        "mapping_status",
        "mapping_rationale",
        "iso_control_id",
        "iso_control_title",
        "nist_control_id",
        "nist_control_title",
        "sama_control_id",
        "sama_control_title",
        "required_evidence",
        "evidence_validation",
    }

    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"Validated crosswalk missing columns: {sorted(missing)}"
        )

    total = len(df)
    equivalent = (df["mapping_status"] == "Equivalent").sum()
    gaps = (df["mapping_status"] == "Gap").sum()
    evidence_pass = (df["evidence_validation"] == "PASS").sum()
    evidence_missing = (
        df["evidence_validation"] == "MISSING"
    ).sum()

    equivalent_pct = (
        round((equivalent / total) * 100, 1)
        if total
        else 0
    )

    gap_pct = (
        round((gaps / total) * 100, 1)
        if total
        else 0
    )

    framework_coverage = {
        "ISO/IEC 27001": int(
            df["iso_control_id"].astype(bool).sum()
        ),
        "NIST CSF 2.0": int(
            df["nist_control_id"].astype(bool).sum()
        ),
        "SAMA CSF": int(
            df["sama_control_id"].astype(bool).sum()
        ),
    }

    gap_df = df[df["mapping_status"] == "Gap"]

    generated = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M UTC"
    )

    lines = [
        "# Security Control Framework Crosswalk Report",
        "",
        "## Executive Summary",
        "",
        (
            "This report presents a normalized security-control crosswalk "
            "across ISO/IEC 27001 Annex A, NIST Cybersecurity Framework "
            "2.0, and the SAMA Cyber Security Framework. It identifies "
            "aligned control themes, framework coverage gaps, and the "
            "evidence expected to support assessment activities."
        ),
        "",
        f"**Generated:** {generated}",
        "",
        "## Crosswalk Metrics",
        "",
        "| Metric | Result |",
        "|---|---:|",
        f"| Total control themes assessed | {total} |",
        f"| Equivalent mappings | {equivalent} |",
        f"| Framework coverage gaps | {gaps} |",
        f"| Equivalent coverage | {equivalent_pct}% |",
        f"| Gap rate | {gap_pct}% |",
        f"| Evidence requirements defined | {evidence_pass} |",
        f"| Missing evidence definitions | {evidence_missing} |",
        "",
        "## Framework Coverage",
        "",
        "| Framework | Themes with mapped control |",
        "|---|---:|",
    ]

    for framework, count in framework_coverage.items():
        lines.append(f"| {framework} | {count}/{total} |")

    lines.extend([
        "",
        "## Coverage Gap Analysis",
        "",
    ])

    if gap_df.empty:
        lines.append(
            "No framework coverage gaps were identified in the assessed scope."
        )
    else:
        lines.extend([
            "| Theme | ISO 27001 | NIST CSF 2.0 | SAMA CSF | Rationale |",
            "|---|---|---|---|---|",
        ])

        for _, row in gap_df.iterrows():
            lines.append(
                f"| {safe(row['control_theme'])} "
                f"| {safe(row['iso_control_id'])} "
                f"| {safe(row['nist_control_id'])} "
                f"| {safe(row['sama_control_id'])} "
                f"| {safe(row['mapping_rationale'])} |"
            )

    lines.extend([
        "",
        "## Evidence Requirements",
        "",
        "| Control Theme | Mapping Status | Validation | Required Evidence |",
        "|---|---|---|---|",
    ])

    for _, row in df.iterrows():
        lines.append(
            f"| {safe(row['control_theme'])} "
            f"| {safe(row['mapping_status'])} "
            f"| {safe(row['evidence_validation'])} "
            f"| {safe(row['required_evidence'])} |"
        )

    lines.extend([
        "",
        "## Full Framework Crosswalk",
        "",
        (
            "| Control Theme | Status | ISO 27001 | "
            "NIST CSF 2.0 | SAMA CSF |"
        ),
        "|---|---|---|---|---|",
    ])

    for _, row in df.iterrows():
        iso = (
            f"{safe(row['iso_control_id'])} — "
            f"{safe(row['iso_control_title'])}"
            if row["iso_control_id"]
            else "—"
        )

        nist = (
            f"{safe(row['nist_control_id'])} — "
            f"{safe(row['nist_control_title'])}"
            if row["nist_control_id"]
            else "—"
        )

        sama = (
            f"{safe(row['sama_control_id'])} — "
            f"{safe(row['sama_control_title'])}"
            if row["sama_control_id"]
            else "—"
        )

        lines.append(
            f"| {safe(row['control_theme'])} "
            f"| {safe(row['mapping_status'])} "
            f"| {iso} "
            f"| {nist} "
            f"| {sama} |"
        )

    lines.extend([
        "",
        "## Assessment Notes",
        "",
        (
            "- Equivalent mappings represent thematic alignment within "
            "the simplified control scope and should not be interpreted "
            "as proof that the frameworks are legally or technically "
            "interchangeable."
        ),
        (
            "- Gap status identifies where the sampled catalog does not "
            "contain a mapped control; it does not necessarily prove that "
            "the complete source framework lacks a related requirement."
        ),
        (
            "- Evidence requirements define expected assessment artifacts "
            "but do not establish that those artifacts have actually been "
            "collected or validated."
        ),
        (
            "- Production compliance assessments should validate mappings "
            "against the complete authoritative framework publications "
            "and organizational implementation context."
        ),
        "",
    ])

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"PASS: report generated at {report_path}")
    print(f"Total themes: {total}")
    print(f"Equivalent mappings: {equivalent}")
    print(f"Coverage gaps: {gaps}")
    print(f"Evidence requirements defined: {evidence_pass}")


if __name__ == "__main__":
    generate_report(
        OUTPUT / "crosswalk_with_evidence.csv",
        OUTPUT / "crosswalk_report.md",
    )
