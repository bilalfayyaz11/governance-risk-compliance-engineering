# GCC Regulatory Control Mapping

## Overview

This implementation provides a normalized compliance-engineering workflow for reconciling cybersecurity requirements across major GCC regulatory frameworks and mapping them to international reference controls.

It combines PostgreSQL relational modeling, Python ETL, similarity-assisted control mapping, GCC-specific regulatory overlay detection, and automated CSV/XLSX reporting.

The workflow is designed to support regional compliance analysis, continuous monitoring, cross-framework reconciliation, and identification of requirements that cannot be represented accurately through generic NIST or ISO mappings alone.

## Architecture

    GCC Regulatory Catalogs
    ├── NCA ECC 2-2024
    ├── SAMA Cyber Security Framework
    ├── UAE Information Security Regulation
    └── Qatar NIA 2.1
             │
             ▼
    ┌─────────────────────────────┐
    │      Python ETL Layer       │
    │                             │
    │ • Schema validation         │
    │ • Framework upserts         │
    │ • Duplicate protection      │
    │ • Control normalization     │
    └──────────────┬──────────────┘
                   │
                   ▼
    ┌─────────────────────────────┐
    │        PostgreSQL           │
    │                             │
    │ frameworks                  │
    │ controls                    │
    │ crosswalks                  │
    │ overlays                    │
    │ control_overlays            │
    └──────────────┬──────────────┘
                   │
          ┌────────┴─────────┐
          │                  │
          ▼                  ▼
    Crosswalk Engine     Overlay Detector
          │                  │
          │                  ├── data_residency
          │                  ├── arabic_logging
          │                  ├── national_cert_reporting
          │                  └── local_hosting_mandate
          │
          ├── NIST SP 800-53
          └── ISO 27001:2022
                   │
                   ▼
    ┌─────────────────────────────┐
    │ Regional Applicability      │
    │ Matrix                      │
    │                             │
    │ • GCC framework presence    │
    │ • NIST mapping status       │
    │ • ISO mapping status        │
    │ • Crosswalk coverage        │
    │ • Regional overlays         │
    └─────────────────────────────┘
                   │
                   ▼
           CSV + XLSX Reports

## Regulatory Scope

The representative GCC catalogs used in this implementation are:

| Framework | Version / Scope | Jurisdiction |
|---|---|---|
| NCA ECC | 2-2024 | Saudi Arabia |
| SAMA Cyber Security Framework | 1.0 representative extract | Saudi Arabia |
| UAE Information Security Regulation | Representative extract | United Arab Emirates |
| Qatar NIA | 2.1 | Qatar |

Reference frameworks:

| Framework | Version |
|---|---|
| NIST SP 800-53 | Rev. 5 |
| ISO/IEC 27001 | 2022 |

The GCC CSV files are representative control extracts designed to demonstrate the data architecture and reconciliation workflow. They are not presented as complete authoritative reproductions of regulator publications.

## Database Design

The PostgreSQL schema is defined in:

    schema.sql

Core entities:

### frameworks

Stores framework identity and version metadata.

Fields include:

- name
- version
- jurisdiction
- authority

A new framework version receives a separate framework record. This preserves historical traceability when regulations change.

### controls

Stores normalized controls belonging to each framework.

Fields include:

- control reference
- domain
- title
- description
- control type

A unique constraint on framework and control reference prevents duplicate controls.

### crosswalks

Stores many-to-many control relationships.

Supported mapping strengths:

- exact
- partial
- related

Crosswalk pairs are stored using canonical numeric ordering:

    min(control_id), max(control_id)

This means:

    Control A ↔ Control B

is stored only once instead of creating duplicate A→B and B→A records.

### overlays

Stores GCC-specific regulatory requirements that should remain distinct from general cross-framework mappings.

### control_overlays

Provides the many-to-many relationship between controls and regional overlay requirements.

## Orphan Control Handling

Controls without a defensible NIST or ISO equivalent remain valid controls without a crosswalk record.

The database does not fabricate weak mappings simply to increase coverage.

An unmapped control therefore remains distinguishable from a reviewed and confirmed mapping.

This is important when dealing with jurisdiction-specific regulatory requirements.

## ETL Pipeline

The ingestion workflow is implemented in:

    scripts/load_controls.py

It performs:

- CSV schema validation
- Required-field validation
- Duplicate control detection
- Framework upserts
- Control upserts
- Bulk regulatory ingestion
- Integrity reporting

Representative source files:

    data/nca_ecc.csv
    data/sama_csf.csv
    data/uae_isr.csv
    data/qatar_nia.csv
    data/nist_800_53.csv
    data/iso_27001.csv

## Crosswalk Engine

The mapping engine is implemented in:

    scripts/crosswalk_engine.py

It provides two layers:

1. Similarity-assisted candidate generation
2. Analyst-confirmed control mapping

### Similarity Strategy

The candidate score combines:

    45% domain similarity
    20% title similarity
    35% description similarity

Domain alignment receives the highest weight because regulatory control descriptions are often short, repetitive, and jargon-heavy.

Pure fuzzy matching can overvalue generic terms such as:

- security
- information
- monitoring
- requirements

The hybrid approach instead uses domain context plus interpretable token overlap.

The similarity score is decision support only.

Final mapping strength remains an analyst-reviewed compliance decision.

## Mapping Strengths

### exact

The two controls express substantially equivalent security requirements.

### partial

The controls share the primary objective but differ in scope, implementation requirements, or jurisdiction-specific obligations.

### related

The controls are relevant to the same governance objective but should not be treated as equivalent.

## GCC Regulatory Overlays

Overlay detection is implemented in:

    scripts/overlay_detection.py

The detector identifies regional obligations that may not have direct NIST or ISO equivalents.

### data_residency

Detects requirements involving:

- in-country storage
- national processing restrictions
- data residency
- cross-border restrictions
- nationally approved locations

### arabic_logging

Detects requirements involving:

- Arabic-language audit evidence
- Arabic regulatory reporting
- Arabic compliance records
- local-language logging requirements

### national_cert_reporting

Detects:

- national CERT notification
- national cybersecurity authority reporting
- regulator notification obligations
- jurisdiction-specific incident reporting

### local_hosting_mandate

Detects:

- local cloud regions
- nationally approved hosting
- domestic infrastructure
- in-country hosting requirements

## Why Overlays Are Separate from Crosswalks

A GCC requirement may partially correspond to a NIST or ISO control while still containing an additional regional obligation.

Example:

    GCC Incident Reporting Requirement
                 │
                 ├── partial mapping ──> NIST IR-6
                 │
                 └── regional overlay ─> national_cert_reporting

The crosswalk captures shared security intent.

The overlay captures the jurisdiction-specific requirement.

This avoids falsely claiming that generic international controls fully satisfy local regulatory obligations.

## Regional Applicability Matrix

The reporting workflow is implemented in:

    scripts/generate_matrix.py

Generated outputs:

    output/applicability_matrix.csv
    output/applicability_matrix.xlsx

The XLSX workbook contains:

- Applicability Matrix
- Control Inventory
- Crosswalk Detail
- Overlay Detail

## Matrix Capabilities

The matrix reports, by control domain:

- Whether NCA ECC applies
- Whether SAMA CSF applies
- Whether UAE ISR applies
- Whether Qatar NIA applies
- Number of controls per framework
- Whether NIST mappings exist
- Whether ISO mappings exist
- NIST mapping count
- ISO mapping count
- Crosswalk coverage percentage
- Data residency overlays
- Arabic logging overlays
- National CERT reporting overlays
- Local hosting mandates

For example, the Logging and Monitoring domain can answer:

- Which GCC frameworks contain logging requirements?
- Is a NIST SP 800-53 mapping available?
- Is an ISO 27001 mapping available?
- What percentage of GCC controls are currently crosswalked?
- Does the domain contain an Arabic-language logging requirement?

## How to Run

Activate the Python environment:

    source venv/bin/activate

Load normalized control catalogs:

    python scripts/load_controls.py

Generate or review crosswalk mappings:

    python scripts/crosswalk_engine.py --seed

Apply regional overlays:

    python scripts/overlay_detection.py

Generate reporting outputs:

    python scripts/generate_matrix.py

## Database Queries

### Framework Control Counts

    psql -d gcc_grc_map -c "
    SELECT
        f.name,
        COUNT(*) AS control_count
    FROM frameworks f
    JOIN controls c
        ON f.id = c.framework_id
    GROUP BY f.name
    ORDER BY f.name;
    "

### Crosswalk Distribution

    psql -d gcc_grc_map -c "
    SELECT
        mapping_strength,
        COUNT(*) AS mapping_count
    FROM crosswalks
    GROUP BY mapping_strength;
    "

### Overlay Distribution

    psql -d gcc_grc_map -c "
    SELECT
        o.name,
        COUNT(*) AS control_count
    FROM control_overlays co
    JOIN overlays o
        ON co.overlay_id = o.id
    GROUP BY o.name
    ORDER BY o.name;
    "

## Repository Structure

    gcc-regulatory-control-mapping/
    ├── README.md
    ├── schema.sql
    ├── data/
    │   ├── nca_ecc.csv
    │   ├── sama_csf.csv
    │   ├── uae_isr.csv
    │   ├── qatar_nia.csv
    │   ├── nist_800_53.csv
    │   └── iso_27001.csv
    ├── scripts/
    │   ├── load_controls.py
    │   ├── crosswalk_engine.py
    │   ├── overlay_detection.py
    │   └── generate_matrix.py
    └── output/
        ├── applicability_matrix.csv
        └── applicability_matrix.xlsx

## Tools Used

- PostgreSQL
- Python 3
- pandas
- SQLAlchemy
- psycopg2
- openpyxl
- SQL
- Bash
- NIST SP 800-53
- ISO/IEC 27001
- GCC cybersecurity regulatory frameworks

## Key Skills Demonstrated

- Regulatory data modeling
- PostgreSQL schema architecture
- Many-to-many relationship design
- Framework versioning
- Python ETL engineering
- CSV reconciliation
- Data quality validation
- SQL joins and aggregation
- Compliance control crosswalking
- Similarity-assisted control mapping
- Analyst-reviewed mapping workflows
- Regulatory overlay modeling
- Data residency requirement detection
- Regional incident reporting analysis
- Regulatory reporting automation
- Excel reporting automation
- Continuous compliance monitoring
- Orphan control management
- Cross-framework coverage analysis

## Real-World Use Case

A multinational organization operating across GCC jurisdictions may need to comply with several national cybersecurity frameworks at the same time.

Without normalization, teams often maintain separate spreadsheets for each regulator and manually compare similar controls.

This architecture creates a central compliance data model capable of answering questions such as:

- Which controls are shared across jurisdictions?
- Which requirements have international equivalents?
- Where is only a partial mapping available?
- Which controls impose GCC-specific obligations?
- Where are compliance mappings still missing?
- Which domains have the weakest crosswalk coverage?
- Which regulatory requirements require local implementation differences?

The same architecture can be integrated into enterprise GRC platforms, control-assurance systems, compliance dashboards, or continuous-monitoring pipelines.

## Lessons Learned

- Regulatory crosswalking should support many-to-many relationships rather than assume one-to-one equivalence.
- Framework versioning must preserve historical control identity.
- Unmapped controls should remain visible rather than being assigned artificial mappings.
- Similarity scoring is useful for candidate discovery but should not replace analyst judgment.
- Domain similarity is particularly useful for short, jargon-heavy regulatory controls.
- GCC-specific requirements should be modeled separately from generic international controls.
- Data residency and local-hosting requirements are regulatory deltas rather than ordinary security mappings.
- Incident-reporting controls may map to NIST while still requiring separate national notification obligations.
- Deterministic overlay rules improve explainability and auditability.
- A normalized database makes multi-jurisdiction regulatory monitoring substantially easier to automate.

## Implementation Notes

### Framework Version Normalization

The source instructions referenced inconsistent framework labels and versions.

The implementation uses explicit framework-version metadata so regulatory catalogs can be updated without overwriting older control sets.

### Representative Catalogs

Public regulatory catalogs are not distributed through one unified machine-readable format.

Representative normalized extracts are therefore used to demonstrate the ingestion, reconciliation, mapping, and reporting architecture.

The architecture is designed so larger authoritative datasets can replace the representative extracts without changing the relational model.

### Canonical Crosswalk Storage

Crosswalks are stored once using canonical control-ID ordering.

This prevents duplicate bidirectional relationships while allowing applications to traverse mappings from either side.

### Overlay Detection

Regional overlays are detected using deterministic regular expressions and keyword patterns.

This approach was selected because jurisdiction-specific obligations frequently contain identifiable legal or operational phrases, making explainable rule-based detection preferable to opaque classification.

### Separation of Mapping and Applicability

A partial NIST or ISO mapping does not imply complete compliance with a GCC control.

The applicability matrix therefore preserves both the international mapping and any additional regional overlay requirements.
