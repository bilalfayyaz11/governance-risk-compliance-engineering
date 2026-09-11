#!/usr/bin/env python3

from pathlib import Path
import html
import subprocess
import xml.etree.ElementTree as ET


BASE = Path(__file__).resolve().parent.parent
DIAGRAMS = BASE / "diagrams"

DRAWIO_PATH = DIAGRAMS / "idverify_dfd.drawio"
DOT_PATH = DIAGRAMS / "idverify_dfd.dot"
PNG_PATH = DIAGRAMS / "idverify_dfd.png"


def vertex(
    root,
    cell_id,
    label,
    x,
    y,
    width,
    height,
    style,
):
    cell = ET.SubElement(
        root,
        "mxCell",
        {
            "id": cell_id,
            "value": html.escape(label),
            "style": style,
            "vertex": "1",
            "parent": "1",
        },
    )

    ET.SubElement(
        cell,
        "mxGeometry",
        {
            "x": str(x),
            "y": str(y),
            "width": str(width),
            "height": str(height),
            "as": "geometry",
        },
    )


def edge(
    root,
    cell_id,
    label,
    source,
    target,
):
    cell = ET.SubElement(
        root,
        "mxCell",
        {
            "id": cell_id,
            "value": html.escape(label),
            "style": (
                "edgeStyle=orthogonalEdgeStyle;"
                "rounded=0;"
                "orthogonalLoop=1;"
                "jettySize=auto;"
                "html=1;"
                "endArrow=block;"
            ),
            "edge": "1",
            "parent": "1",
            "source": source,
            "target": target,
        },
    )

    ET.SubElement(
        cell,
        "mxGeometry",
        {
            "relative": "1",
            "as": "geometry",
        },
    )


def build_drawio():
    mxfile = ET.Element(
        "mxfile",
        {
            "host": "app.diagrams.net",
            "modified": "2026-09-12T00:00:00.000Z",
            "agent": "CLI-generated",
            "version": "24.7.17",
        },
    )

    diagram = ET.SubElement(
        mxfile,
        "diagram",
        {
            "id": "idverify-dfd",
            "name": "IDVerify Privacy DFD",
        },
    )

    model = ET.SubElement(
        diagram,
        "mxGraphModel",
        {
            "dx": "1400",
            "dy": "900",
            "grid": "1",
            "gridSize": "10",
            "guides": "1",
            "tooltips": "1",
            "connect": "1",
            "arrows": "1",
            "fold": "1",
            "page": "1",
            "pageScale": "1",
            "pageWidth": "1600",
            "pageHeight": "1000",
            "math": "0",
            "shadow": "0",
        },
    )

    root = ET.SubElement(model, "root")

    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(
        root,
        "mxCell",
        {
            "id": "1",
            "parent": "0",
        },
    )

    entity_style = (
        "rounded=0;"
        "whiteSpace=wrap;"
        "html=1;"
        "strokeWidth=2;"
    )

    process_style = (
        "rounded=1;"
        "whiteSpace=wrap;"
        "html=1;"
        "strokeWidth=2;"
    )

    datastore_style = (
        "shape=cylinder;"
        "whiteSpace=wrap;"
        "html=1;"
        "boundedLbl=1;"
        "strokeWidth=2;"
    )

    boundary_style = (
        "rounded=0;"
        "whiteSpace=wrap;"
        "html=1;"
        "dashed=1;"
        "strokeWidth=2;"
        "fillColor=none;"
        "verticalAlign=top;"
        "fontStyle=2;"
    )

    # Trust boundaries
    vertex(
        root,
        "tb1",
        "Trust Boundary 1: Public Client ↔ Fintech Backend",
        250,
        40,
        440,
        760,
        boundary_style,
    )

    vertex(
        root,
        "tb2",
        "Trust Boundary 2: Fintech Backend ↔ Third-Party ML Provider",
        720,
        40,
        360,
        300,
        boundary_style,
    )

    # Core DFD elements
    vertex(
        root,
        "mobile",
        "Mobile Client",
        40,
        180,
        150,
        70,
        entity_style,
    )

    vertex(
        root,
        "gateway",
        "API Gateway",
        300,
        160,
        160,
        70,
        process_style,
    )

    vertex(
        root,
        "idverify",
        "IDVerify Service",
        300,
        300,
        160,
        70,
        process_style,
    )

    vertex(
        root,
        "ocr",
        "Third-Party OCR / Face-Match API",
        800,
        160,
        220,
        80,
        entity_style,
    )

    vertex(
        root,
        "postgres",
        "PostgreSQL Datastore",
        300,
        480,
        180,
        90,
        datastore_style,
    )

    vertex(
        root,
        "audit",
        "Audit Logging Service",
        540,
        480,
        180,
        80,
        process_style,
    )

    vertex(
        root,
        "admin",
        "Admin Dashboard",
        300,
        660,
        180,
        70,
        entity_style,
    )

    # Data flows
    edge(
        root,
        "f1",
        "ID image + selfie",
        "mobile",
        "gateway",
    )

    edge(
        root,
        "f2",
        "Verification request + session token",
        "gateway",
        "idverify",
    )

    edge(
        root,
        "f3",
        "ID image + selfie (biometric processing)",
        "idverify",
        "ocr",
    )

    edge(
        root,
        "f4",
        "OCR fields + face-match score",
        "ocr",
        "idverify",
    )

    edge(
        root,
        "f5",
        "Extracted PII + verification status",
        "idverify",
        "postgres",
    )

    edge(
        root,
        "f6",
        "Audit event + subject/session reference",
        "idverify",
        "audit",
    )

    edge(
        root,
        "f7",
        "Flagged verification case",
        "postgres",
        "admin",
    )

    edge(
        root,
        "f8",
        "Review decision + officer identity",
        "admin",
        "idverify",
    )

    edge(
        root,
        "f9",
        "Verification result",
        "idverify",
        "gateway",
    )

    edge(
        root,
        "f10",
        "Approved / rejected / manual review",
        "gateway",
        "mobile",
    )

    tree = ET.ElementTree(mxfile)

    ET.indent(tree, space="  ")

    tree.write(
        DRAWIO_PATH,
        encoding="utf-8",
        xml_declaration=True,
    )


def build_dot():
    dot = r'''
digraph IDVerify {
    rankdir=LR;
    graph [
        label="IDVerify Privacy Data Flow Diagram",
        labelloc=t,
        fontsize=20
    ];

    node [
        shape=box,
        style="rounded",
        fontsize=10
    ];

    subgraph cluster_backend {
        label="Trust Boundary 1: Fintech Backend";
        style=dashed;

        gateway [label="API Gateway"];
        idverify [label="IDVerify Service"];
        postgres [
            label="PostgreSQL Datastore",
            shape=cylinder
        ];
        audit [label="Audit Logging Service"];
        admin [label="Admin Dashboard"];
    }

    subgraph cluster_thirdparty {
        label="Trust Boundary 2: Third-Party ML Provider";
        style=dashed;

        ocr [
            label="Third-Party OCR / Face-Match API"
        ];
    }

    mobile [
        label="Mobile Client"
    ];

    mobile -> gateway [
        label="ID image + selfie"
    ];

    gateway -> idverify [
        label="Verification request\n+ session token"
    ];

    idverify -> ocr [
        label="ID image + selfie\n(biometric processing)"
    ];

    ocr -> idverify [
        label="OCR fields +\nface-match score"
    ];

    idverify -> postgres [
        label="Extracted PII +\nverification status"
    ];

    idverify -> audit [
        label="Audit event +\nsubject/session reference"
    ];

    postgres -> admin [
        label="Flagged verification case"
    ];

    admin -> idverify [
        label="Review decision +\nofficer identity"
    ];

    idverify -> gateway [
        label="Verification result"
    ];

    gateway -> mobile [
        label="Approved / rejected /\nmanual review"
    ];
}
'''

    DOT_PATH.write_text(
        dot.strip() + "\n",
        encoding="utf-8",
    )

    subprocess.run(
        [
            "dot",
            "-Tpng",
            str(DOT_PATH),
            "-o",
            str(PNG_PATH),
        ],
        check=True,
    )


def validate():
    required_labels = [
        "Mobile Client",
        "API Gateway",
        "IDVerify Service",
        "Third-Party OCR / Face-Match API",
        "PostgreSQL Datastore",
        "Audit Logging Service",
        "Admin Dashboard",
    ]

    xml_text = DRAWIO_PATH.read_text(
        encoding="utf-8"
    )

    for label in required_labels:
        if label not in xml_text:
            raise ValueError(
                f"Missing DFD element: {label}"
            )

    tree = ET.parse(DRAWIO_PATH)
    root = tree.getroot()

    cells = root.findall(".//mxCell")

    vertices = [
        c for c in cells
        if c.attrib.get("vertex") == "1"
    ]

    edges = [
        c for c in cells
        if c.attrib.get("edge") == "1"
    ]

    boundaries = [
        c for c in vertices
        if "Trust Boundary" in html.unescape(
            c.attrib.get("value", "")
        )
    ]

    print(
        f"DFD elements including boundaries: {len(vertices)}"
    )

    print(
        f"Labeled data flows: {len(edges)}"
    )

    print(
        f"Trust boundaries: {len(boundaries)}"
    )

    if len(vertices) < 6:
        raise ValueError(
            "DFD has fewer than 6 elements"
        )

    if len(edges) < 7:
        raise ValueError(
            "DFD has fewer than 7 data flows"
        )

    if len(boundaries) < 2:
        raise ValueError(
            "DFD has fewer than 2 trust boundaries"
        )


if __name__ == "__main__":
    DIAGRAMS.mkdir(
        parents=True,
        exist_ok=True,
    )

    build_drawio()
    build_dot()
    validate()

    print()
    print(f"draw.io: {DRAWIO_PATH}")
    print(f"DOT:     {DOT_PATH}")
    print(f"PNG:     {PNG_PATH}")
