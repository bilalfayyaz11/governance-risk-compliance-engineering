#!/usr/bin/env python3

from pathlib import Path
import subprocess
import yaml


REQUIRED_KEYS = {
    "data_categories",
    "subjects",
    "purpose",
    "transfer_frequency",
    "locations",
    "sub_processors",
}

VALID_TIERS = {
    "Public",
    "Internal",
    "Confidential",
    "Special Category",
}


def load_dataflow(yaml_path: str) -> dict:
    """
    Load and validate the data-flow definition.
    """
    path = Path(yaml_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Data-flow file not found: {path}"
        )

    with path.open("r", encoding="utf-8") as handle:
        flow = yaml.safe_load(handle)

    if not isinstance(flow, dict):
        raise ValueError(
            "Data-flow YAML must contain a top-level mapping"
        )

    missing = REQUIRED_KEYS - flow.keys()

    if missing:
        raise ValueError(
            "Missing required keys: "
            + ", ".join(sorted(missing))
        )

    if not flow["data_categories"]:
        raise ValueError(
            "data_categories cannot be empty"
        )

    if not flow["sub_processors"]:
        raise ValueError(
            "At least one sub-processor is required"
        )

    return flow


def classify_sensitivity(fields: list) -> dict:
    """
    Map each field to a sensitivity tier.
    """
    classifications = {}

    for item in fields:
        if not isinstance(item, dict):
            raise ValueError(
                "Each data category must be a mapping"
            )

        field_name = item.get("field")
        tier = item.get("tier")

        if not field_name:
            raise ValueError(
                "Data category missing field name"
            )

        if tier not in VALID_TIERS:
            raise ValueError(
                f"Invalid tier '{tier}' "
                f"for field '{field_name}'"
            )

        classifications[field_name] = tier

    return classifications


def escape_dot(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
    )


def render_diagram(flow: dict, output_path: str) -> None:
    """
    Generate DOT source and render a PNG using Graphviz.
    """
    output = Path(output_path)
    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    source = flow["locations"]["source"]
    destination = flow["locations"]["destination"]
    sub_processors = flow["sub_processors"]

    dot_path = output.with_suffix(".dot")

    source_label = (
        f"{flow['exporter']['entity']}\\n"
        f"{source['city']}, {source['country']}\\n"
        f"{source['system']}"
    )

    destination_label = (
        f"{flow['importer']['entity']}\\n"
        f"{destination['city']}, "
        f"{destination['country']}\\n"
        f"{destination['system']}"
    )

    lines = [
        "digraph DataFlow {",
        "  rankdir=LR;",
        '  graph [label="Cross-Border HR Data Flow", '
        'labelloc=t, fontsize=18];',
        '  node [shape=box, style="rounded", fontsize=11];',
        '  edge [fontsize=10];',
        "",
        f'  dubai [label="{escape_dot(source_label)}"];',
        f'  frankfurt [label="{escape_dot(destination_label)}"];',
        "",
        '  dubai -> frankfurt [label="Monthly HR / payroll transfer\\nTLS 1.3"];',
    ]

    for index, sub_processor in enumerate(
        sub_processors,
        start=1,
    ):
        node_name = f"subprocessor_{index}"

        label = (
            f"{sub_processor['entity']}\\n"
            f"{sub_processor['city']}, "
            f"{sub_processor['country']}\\n"
            f"{sub_processor['purpose']}"
        )

        lines.append(
            f'  {node_name} '
            f'[label="{escape_dot(label)}"];'
        )

        lines.append(
            f'  frankfurt -> {node_name} '
            '[label="Onward transfer\\nTLS 1.3\\n'
            'GDPR Chapter V assessment"];'
        )

    lines.append("}")

    dot_source = "\n".join(lines) + "\n"

    dot_path.write_text(
        dot_source,
        encoding="utf-8",
    )

    subprocess.run(
        [
            "dot",
            "-Tpng",
            str(dot_path),
            "-o",
            str(output),
        ],
        check=True,
    )


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent

    yaml_path = base_dir / "data" / "dataflow.yaml"
    png_path = base_dir / "diagrams" / "dataflow.png"

    flow = load_dataflow(str(yaml_path))

    classifications = classify_sensitivity(
        flow["data_categories"]
    )

    print("Sensitivity classification:")

    for field, tier in classifications.items():
        print(f"  {field}: {tier}")

    render_diagram(
        flow,
        str(png_path),
    )

    print()
    print(f"Diagram created: {png_path}")
