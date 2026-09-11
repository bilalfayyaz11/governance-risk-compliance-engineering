from pathlib import Path
from datetime import date


def build_index(
    docs_dir: str,
    data_dir: str,
    output_file: str,
) -> None:
    """
    Generate an index Markdown file listing dossier components
    with completion status and today's date.
    """

    docs_path = Path(docs_dir)
    data_path = Path(data_dir)
    output_path = Path(output_file)

    required_artifacts = [
        (
            "Personal Data Inventory",
            data_path / "data_inventory.csv",
        ),
        (
            "Data Flow Classification Report",
            docs_path / "data_flow_report.txt",
        ),
        (
            "Lawful Basis and DPO Appointment Plan",
            docs_path / "lawful_basis_dpo_plan.md",
        ),
        (
            "Consent Record Store",
            data_path / "consents.json",
        ),
        (
            "Breach Notification Procedure",
            docs_path / "breach_notification_procedure.md",
        ),
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# UAE PDPL Compliance Dossier",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "## Compliance Artifact Checklist",
        "",
    ]

    for name, path in required_artifacts:
        status = "x" if path.exists() and path.stat().st_size > 0 else " "
        lines.append(
            f"- [{status}] {name} — `{path.as_posix()}`"
        )

    lines.extend([
        "",
        "## Dossier Coverage",
        "",
        "- Personal data inventory and processing-purpose mapping",
        "- Data sensitivity classification",
        "- Lawful basis documentation",
        "- DPO appointment planning",
        "- Consent record management",
        "- Data subject rights request handling",
        "- Personal-data breach response procedure",
        "- Compliance evidence indexing",
        "",
        "## Generated Files",
        "",
        "### Documentation",
    ])

    for path in sorted(docs_path.glob("*")):
        if path.is_file() and path != output_path:
            lines.append(f"- `{path.name}`")

    lines.extend([
        "",
        "### Data and Evidence",
    ])

    for path in sorted(data_path.glob("*")):
        if path.is_file():
            lines.append(f"- `{path.name}`")

    lines.extend([
        "",
        "## Status",
        "",
    ])

    complete = all(
        path.exists() and path.stat().st_size > 0
        for _, path in required_artifacts
    )

    if complete:
        lines.append(
            "**READY — all required compliance artifacts are present.**"
        )
    else:
        lines.append(
            "**INCOMPLETE — one or more required artifacts are missing.**"
        )

    output_path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent

    build_index(
        base_dir / "docs",
        base_dir / "data",
        base_dir / "docs" / "dossier_index.md",
    )
