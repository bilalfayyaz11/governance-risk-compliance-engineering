# FIPS 199 Security Categorization

## What This Does

This implementation performs a structured security categorization of a healthcare appointment scheduling system using FIPS 199 and NIST SP 800-60 guidance. It maps system information to relevant NIST information types, establishes confidentiality, integrity, and availability impact levels, applies operational-context adjustments, and calculates the final system security category using the FIPS 199 high-water-mark methodology.

The resulting evidence package provides a repeatable and auditable basis for security control selection, risk assessment, and authorization activities.

## Architecture

    ┌─────────────────────────────────────────────────────────────┐
    │          Patient Appointment Scheduling System              │
    └─────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                 INFORMATION TYPE MAPPING                    │
    │                                                             │
    │  D.14.1  Access to Care                                    │
    │  C.2.8.9 Personal Identity and Authentication              │
    └─────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                    C-I-A IMPACT ANALYSIS                    │
    │                                                             │
    │  Access to Care       LOW / MODERATE / MODERATE            │
    │  Identity & Auth      MODERATE / MODERATE / MODERATE       │
    └─────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
    ┌─────────────────────────────────────────────────────────────┐
    │              PYTHON HIGH-WATER-MARK ENGINE                 │
    │                                                             │
    │  Confidentiality = MODERATE                                │
    │  Integrity       = MODERATE                                │
    │  Availability    = MODERATE                                │
    │                                                             │
    │             Overall Impact = MODERATE                      │
    └──────────────────────┬──────────────────────┬───────────────┘
                           │                      │
                           ▼                      ▼
              ┌──────────────────────┐  ┌──────────────────────┐
              │ Categorization       │  │ Categorization       │
              │ Workbook             │  │ Memo                 │
              │                      │  │                      │
              │ Ratings + Evidence   │  │ Authorization        │
              └──────────────────────┘  │ Evidence             │
                                        └──────────┬───────────┘
                                                   │
                                                   ▼
                                        ┌──────────────────────┐
                                        │ SHA-256 Integrity    │
                                        │ Marker               │
                                        └──────────────────────┘

## Prerequisites

- Linux environment
- Python 3
- LibreOffice
- GNU Coreutils (`sha256sum`)
- Git
- NIST FIPS 199
- NIST SP 800-60 Volume 2 Revision 1

No cloud account, external API, or cloud credentials are required.

## Setup & Installation

Install the required packages on Ubuntu:

    sudo apt update
    sudo apt install -y python3 libreoffice git

Verify the environment:

    python3 --version
    libreoffice --version
    git --version
    sha256sum --version

## How to Reproduce

Clone the repository and enter the implementation directory:

    git clone https://github.com/bilalfayyaz11/governance-risk-compliance-engineering.git
    cd governance-risk-compliance-engineering/fips-199-security-categorization

Review the identified information types:

    cat information_types.txt

Run the automated high-water-mark calculation:

    python3 calculate_impact.py

Expected system-level result:

    Overall Confidentiality: Moderate
    Overall Integrity: Moderate
    Overall Availability: Moderate

    Overall System Impact: Moderate
    SC = {(confidentiality, MODERATE), (integrity, MODERATE), (availability, MODERATE)}

Review the categorization memo:

    cat categorization_memo.txt

Verify the memo against its SHA-256 integrity marker:

    sha256sum -c categorization_memo.sig

Expected result:

    categorization_memo.txt: OK

Open the evidence workbook in an environment with graphical display support:

    libreoffice categorization_workbook.ods

## Tools Used

- NIST FIPS 199
- NIST SP 800-60
- Python 3
- LibreOffice
- OpenDocument Spreadsheet
- SHA-256
- GNU Coreutils
- Linux
- Git

## Key Skills Demonstrated

- FIPS 199 information-system security categorization
- NIST SP 800-60 information-type mapping
- Confidentiality, integrity, and availability impact analysis
- Operational-context risk adjustment
- High-water-mark security categorization
- Python-based compliance automation
- Governance and authorization evidence generation
- Compliance artifact integrity verification
- Traceable security-risk justification
- Technical GRC documentation

## Real-World Use Case

Organizations following the NIST Risk Management Framework need to determine the potential impact of a security failure before selecting appropriate safeguards. This workflow demonstrates how a healthcare workload can be mapped to applicable information types, evaluated against confidentiality, integrity, and availability objectives, adjusted for operational consequences, and converted into auditable categorization evidence.

The resulting security category can serve as an input to downstream security control selection, tailoring, risk assessment, and authorization decisions.

## Lessons Learned

- Provisional SP 800-60 impact values provide a starting point rather than an automatic final system categorization.
- Operational context can justify increasing an impact level when mission or business consequences exceed the provisional baseline.
- FIPS 199 applies the high-water-mark principle independently across confidentiality, integrity, and availability.
- Accurate information-type mapping is critical because incorrect mappings can propagate into inappropriate security requirements.
- Deterministic categorization logic can be automated to improve repeatability and reduce manual comparison errors.

## Troubleshooting Log

- The supplied scheduling example referenced `D.16.3`, which did not represent the healthcare scheduling workload. The workload was mapped to `D.14.1 - Access to Care`.
- Patient identity and contact information was represented using `C.2.8.9 - Personal Identity and Authentication` rather than relying on a generic PII label.
- Access-to-Care availability was adjusted from Low to Moderate because prolonged scheduling disruption could seriously affect timely access to care and continuity of patient services.
- The execution environment did not expose a graphical display session, so the OpenDocument workbook was generated through LibreOffice headless conversion.
- OSCAL tooling was excluded because no OSCAL artifact was generated or validated by this workflow.
- SHA-256 is documented as an integrity checksum rather than a cryptographic digital signature because no private-key signing operation is performed.

## Repository Artifacts

    fips-199-security-categorization/
    ├── README.md
    ├── calculate_impact.py
    ├── categorization_memo.sig
    ├── categorization_memo.txt
    ├── categorization_workbook.ods
    └── information_types.txt
