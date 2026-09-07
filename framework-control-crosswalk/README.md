# Multi-Framework Security Control Crosswalk

A reproducible governance and compliance workflow for normalizing, mapping, and evaluating security controls across ISO/IEC 27001 Annex A, NIST Cybersecurity Framework 2.0, and the SAMA Cyber Security Framework.

The workflow converts heterogeneous framework references into a standardized control model, applies explicit crosswalk rules, identifies coverage gaps, associates control themes with expected audit evidence, and generates a stakeholder-ready assessment report.

## Architecture

    ISO/IEC 27001 ─┐
                   │
    NIST CSF 2.0 ──┼──> Normalization
                   │         │
    SAMA CSF ──────┘         v
                      Standard Control Model
                              │
                              v
                       Crosswalk Engine
                         /          \
                        v            v
                 Equivalent      Coverage
                  Mappings         Gaps
                        \            /
                         v          v
                       Evidence Mapping
                              │
                              v
                     Stakeholder Report

## Capabilities

- Normalizes control catalogs into a common schema.
- Maps security requirements across three major frameworks.
- Separates equivalent mappings from coverage gaps.
- Maintains mapping rationale alongside control relationships.
- Associates mapped themes with expected assessment evidence.
- Detects undefined evidence requirements automatically.
- Generates dedicated gap-analysis outputs.
- Produces a stakeholder-readable Markdown assessment report.
- Keeps source data, automation logic, and generated results separated.

## Standardized Data Model

Framework-specific fields such as `domain`, `function`, and `principle` are normalized into:

    control_id
    control_title
    category

This provides a consistent interface for downstream reconciliation.

## Crosswalk Model

The mapping engine evaluates common security themes including:

- Security policy
- Vulnerability management
- Security monitoring
- Incident management
- Identity and access management
- Configuration management
- Logging
- Recovery planning

Each relationship records the corresponding framework identifiers, titles, mapping status, and mapping rationale.

A mapping marked `Equivalent` represents thematic alignment within the assessed scope.

A mapping marked `Gap` represents missing coverage within the simplified catalog used by this workflow. It does not establish that the complete authoritative framework lacks a related requirement.

## Evidence Validation

Framework mapping alone does not demonstrate implementation.

The evidence-validation layer associates control themes with expected assessment artifacts such as:

- Approved policies and review records
- Vulnerability scan reports
- Remediation tickets
- SIEM and monitoring records
- Incident investigation documentation
- Access review records
- Configuration baselines
- Recovery testing evidence

The validation engine identifies any crosswalk entry without a defined evidence requirement and exports those exceptions separately.

## Workflow

    Raw framework catalogs
            |
            v
    normalize_catalogs.py
            |
            v
    Normalized catalogs
            |
            v
    build_crosswalk.py
            |
            +----> crosswalk.csv
            |
            +----> crosswalk_gaps.csv
            |
            v
    validate_evidence.py
            |
            +----> crosswalk_with_evidence.csv
            |
            +----> evidence_gaps.csv
            |
            v
    generate_report.py
            |
            v
    crosswalk_report.md

## Repository Structure

    framework-control-crosswalk/
    ├── data/
    │   ├── iso27001.csv
    │   ├── nist_csf.csv
    │   ├── sama_csf.csv
    │   ├── normalized_iso27001.csv
    │   ├── normalized_nist_csf.csv
    │   ├── normalized_sama_csf.csv
    │   └── evidence_requirements.csv
    ├── scripts/
    │   ├── normalize_catalogs.py
    │   ├── build_crosswalk.py
    │   ├── validate_evidence.py
    │   └── generate_report.py
    ├── output/
    │   ├── crosswalk.csv
    │   ├── crosswalk_gaps.csv
    │   ├── crosswalk_with_evidence.csv
    │   ├── evidence_gaps.csv
    │   └── crosswalk_report.md
    ├── requirements.txt
    └── README.md

## Running the Workflow

Create an isolated Python environment:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Normalize the framework data:

    python scripts/normalize_catalogs.py

Build the framework crosswalk:

    python scripts/build_crosswalk.py

Validate evidence requirements:

    python scripts/validate_evidence.py

Generate the stakeholder report:

    python scripts/generate_report.py

## Outputs

### Crosswalk

`output/crosswalk.csv`

Contains the mapped framework relationships, control themes, mapping status, framework identifiers, titles, categories, and mapping rationale.

### Gap Analysis

`output/crosswalk_gaps.csv`

Provides a focused view of control themes where the sampled framework catalogs do not provide complete three-way coverage.

### Evidence-Enriched Crosswalk

`output/crosswalk_with_evidence.csv`

Extends the framework crosswalk with required evidence and evidence-validation status.

### Evidence Exceptions

`output/evidence_gaps.csv`

Identifies mappings for which an expected evidence definition has not been established.

### Stakeholder Report

`output/crosswalk_report.md`

Provides executive metrics, framework coverage, gap analysis, evidence requirements, the full framework crosswalk, and assessment notes.

## Design Principles

**Reproducibility**

Normalization, mapping, validation, and reporting are implemented as executable Python workflows rather than relying solely on manual spreadsheet analysis.

**Traceability**

Mappings retain framework identifiers and explicit rationale so relationships can be reviewed instead of existing as unexplained equivalence claims.

**Evidence Awareness**

Control alignment is kept separate from evidence of implementation. A mapped requirement does not automatically imply compliance.

**Conservative Gap Interpretation**

A gap in this dataset means that the selected control extract does not contain a mapped requirement. Production assessments should evaluate the complete authoritative framework before concluding that a regulatory or security requirement is absent.

## Production Considerations

This implementation uses intentionally scoped framework extracts to demonstrate the crosswalk architecture.

A production implementation should additionally include:

- Complete licensed or authoritative framework datasets
- Mapping provenance and reviewer approval
- Mapping confidence scores
- Version tracking for each framework
- Effective and retirement dates
- Many-to-many control relationships
- Organizational applicability criteria
- Evidence ownership and collection status
- Automated regression testing when framework versions change
- Formal governance for approving cross-framework equivalence

## Security and Compliance Context

This workflow demonstrates how security teams can reduce duplicated compliance effort when operating across multiple regulatory or assurance frameworks.

Rather than maintaining independent evidence and control inventories for every framework, organizations can establish a normalized control model, trace external requirements to common security outcomes, identify genuine differences, and reuse validated evidence where appropriate.

The result is a more maintainable foundation for control rationalization, audit preparation, regulatory mapping, and multi-framework governance.
