# Third-Party Risk Management Engineering

## What This Does

This implementation provides an end-to-end third-party risk management workflow for evaluating, scoring, tiering, and continuously monitoring external vendors. It combines a structured security due diligence questionnaire with a weighted Python risk-scoring engine, tier-based monitoring requirements, an exception register, and a SQLite-backed reporting layer.

Vendor control maturity is normalized to a 0–4 scale and translated into Critical, High, Medium, or Low risk classifications. The workflow provides reproducible evidence for supplier security governance while keeping assessment definitions, scoring logic, monitoring requirements, exceptions, and reporting independently auditable.

## Architecture

    ┌─────────────────────────────────────────────────────────────────────┐
    │                    VENDOR DUE DILIGENCE                             │
    │                                                                     │
    │  Governance                 Access & Data Handling                  │
    │  NIST SP 800-161            ISO/IEC 27036-3                         │
    │                                                                     │
    │  Incident Response          Subcontractor Management                │
    │  NIST SP 800-161            ISO/IEC 27036-2                         │
    │                                                                     │
    │                  Business Continuity                                │
    │                  NIST SP 800-161                                    │
    └───────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    │ 15 security controls
                                    │ maturity values 0–4
                                    ▼
    ┌─────────────────────────────────────────────────────────────────────┐
    │                     RISK SCORING ENGINE                             │
    │                                                                     │
    │                 vendor_responses.csv                                │
    │                          │                                          │
    │                          ▼                                          │
    │                  score_vendors.py                                   │
    │                          │                                          │
    │               Weighted Control Scoring                              │
    │                          │                                          │
    │                          ▼                                          │
    │                   vendor_scores.csv                                 │
    │                          │                                          │
    │             Critical │ High │ Medium │ Low                          │
    └──────────────────────────┬──────────────────────────────────────────┘
                               │
                               ▼
    ┌─────────────────────────────────────────────────────────────────────┐
    │                    GOVERNANCE DATA LAYER                            │
    │                                                                     │
    │                         SQLite                                      │
    │                         tprm.db                                     │
    │                           │                                         │
    │              ┌────────────┴────────────┐                            │
    │              ▼                         ▼                            │
    │       Vendor Register           Exception Register                  │
    │       • Risk tier               • Control gaps                      │
    │       • Risk score              • Risk rating                       │
    │       • Last assessment         • Compensating controls             │
    │       • Next review             • Approval / expiry                 │
    └──────────────┬─────────────────────────┬────────────────────────────┘
                   │                         │
                   ▼                         ▼
    ┌────────────────────────────┐  ┌────────────────────────────────────┐
    │ MONITORING & KRI LAYER     │  │ REPORTING                         │
    │ Critical → Quarterly       │  │ CLI Risk Dashboard                │
    │ High → Semi-annual         │  │ Vendor Tier Summary               │
    │ Medium → Annual            │  │ Average Risk Scores               │
    │ Low → Biennial             │  │ Open Risk Exceptions              │
    └────────────────────────────┘  └────────────────────────────────────┘

## Prerequisites

- Ubuntu Linux
- Python 3
- SQLite 3
- Apache HTTP Server
- MariaDB
- PHP
- LimeSurvey Community Edition
- Git
- Bash
- PHP MySQL extension
- PHP GD extension
- PHP cURL extension
- PHP mbstring extension
- PHP XML extension
- PHP ZIP extension
- PHP Intl extension

## Setup & Installation

Install the required system dependencies:

    sudo apt update

    sudo apt install -y \
      apache2 \
      mariadb-server \
      php \
      libapache2-mod-php \
      php-mysql \
      php-gd \
      php-curl \
      php-mbstring \
      php-xml \
      php-zip \
      php-intl \
      sqlite3

    sudo systemctl enable --now apache2 mariadb

The Python components use only standard-library modules including `csv`, `sqlite3`, `datetime`, and `pathlib`. No external Python packages are required for the scoring, import, or reporting components.

## How to Reproduce

### 1. Define the Vendor Assessment

The version-controlled questionnaire definition is located at:

    questionnaires/vendor-due-diligence-assessment.csv

It contains 15 security controls across five domains:

1. Governance
2. Access & Data Handling
3. Incident Response
4. Subcontractor Management
5. Business Continuity

The controls reference supplier and supply-chain security concepts from NIST SP 800-161 and ISO/IEC 27036.

Each response uses the following normalized maturity model:

| Score | Control Maturity |
|---:|---|
| 0 | No / Not Implemented |
| 1 | Planned |
| 2 | Partially Implemented |
| 3 | Mostly Implemented |
| 4 | Fully Implemented |

Lower control maturity represents greater vendor risk.

### 2. Prepare Vendor Responses

Assessment responses are stored in:

    responses/vendor_responses.csv

Each row represents one vendor. Individual control columns contain maturity values from 0 through 4.

### 3. Execute Weighted Risk Scoring

Run:

    python3 scripts/score_vendors.py

The scoring engine applies differentiated weights based on security significance.

Higher weighting is assigned to controls covering:

- Multi-factor authentication
- Encryption and data protection
- Incident response readiness
- Incident notification requirements
- Business continuity
- Disaster recovery

The weighted score is calculated as:

    Weighted Score =
    Σ(Control Score × Control Weight)
    ─────────────────────────────────
            Σ(Control Weight)

Risk tiers are assigned using the following thresholds:

| Weighted Score | Risk Tier |
|---:|---|
| < 1.0 | Critical |
| 1.0–1.99 | High |
| 2.0–2.99 | Medium |
| 3.0–4.0 | Low |

The scoring engine produces:

    reports/vendor_scores.csv

### 4. Import Vendors into the Risk Register

Run:

    python3 scripts/import_vendors.py

The importer loads scored vendors into SQLite and calculates the next reassessment date according to risk tier.

| Risk Tier | Reassessment Cadence |
|---|---|
| Critical | Quarterly |
| High | Semi-annual |
| Medium | Annual |
| Low | Biennial |

The vendor register records:

- Vendor name
- Weighted score
- Risk tier
- Last assessment date
- Next review date

### 5. Manage Risk Exceptions

The SQLite backend maintains an exception register for control deficiencies requiring formal risk treatment.

Each exception records:

- Vendor
- Control gap
- Risk rating
- Compensating control
- Approver
- Expiration date

Example query:

    sqlite3 -header -column tprm.db "
    SELECT
        v.name AS vendor,
        e.risk_rating,
        e.control_gap,
        e.compensating_control,
        e.approved_by,
        e.expiry_date
    FROM exceptions e
    JOIN vendors v ON v.id = e.vendor_id;
    "

This allows temporary risk acceptance to remain visible, owned, time-bound, and auditable.

### 6. Query Vendor Risk Distribution

Run:

    sqlite3 -header -column tprm.db "
    SELECT
        tier,
        COUNT(*) AS vendor_count,
        ROUND(AVG(score),2) AS avg_score
    FROM vendors
    GROUP BY tier;
    "

This provides the number of vendors and average control-maturity score within each risk tier.

### 7. Generate the Risk Dashboard

Run:

    python3 scripts/generate_dashboard.py

The reporting layer provides:

- Vendor risk distribution
- Average scores by tier
- Individual vendor classifications
- Last assessment dates
- Next reassessment dates
- Open risk exceptions
- Exception expiration dates

A persistent report is stored at:

    reports/tprm-dashboard.txt

### 8. Review Continuous Monitoring Requirements

The monitoring model is documented in:

    monitoring_plan.md

It defines:

- Risk-based reassessment cadence
- Key Risk Indicators
- Evidence sources
- Escalation conditions
- Exception triggers
- Early reassessment conditions

Critical vendors receive the strongest oversight, while lower-risk vendors operate under progressively lighter monitoring requirements.

## Tools Used

- Python 3
- SQLite
- MariaDB
- Apache HTTP Server
- PHP
- LimeSurvey Community Edition
- Bash
- Git
- NIST SP 800-161
- ISO/IEC 27036

## Key Skills Demonstrated

- Third-party security risk engineering
- Vendor due diligence design
- Supply-chain security control mapping
- Quantitative security risk scoring
- Weighted risk algorithm development in Python
- Structured security assessment data processing
- Vendor risk classification and tiering
- SQLite relational data modeling
- Automated governance data ingestion
- Risk-based reassessment scheduling
- Third-party exception management
- Compensating-control documentation
- Key Risk Indicator design
- Continuous vendor monitoring
- Security governance automation
- CLI-based operational reporting
- Reproducible governance workflows
- End-to-end control validation

## Real-World Use Case

A security, governance, procurement, or third-party risk team can use this workflow during supplier onboarding and ongoing vendor oversight. Vendors are evaluated against a standardized security-control model, their responses are converted into weighted maturity scores, and the resulting risk tier determines the intensity and frequency of monitoring.

Higher-risk vendors can be subjected to more frequent evidence collection, remediation tracking, and reassessment. Control deficiencies can be recorded through the exception register with explicit compensating controls, ownership, approval, and expiration dates. The architecture can later be integrated with procurement systems, ticketing platforms, security operations pipelines, or enterprise GRC platforms.

## Lessons Learned

- Vendor questionnaires become significantly more useful when responses are normalized into machine-processable control maturity values.
- Weighted scoring prevents low-impact governance controls from masking serious weaknesses in authentication, incident response, data protection, or resilience.
- Risk classification becomes operationally useful when each tier drives a different reassessment and monitoring cadence.
- Exceptions require ownership, compensating controls, approvals, and expiration dates to prevent temporary risk acceptance from becoming permanent unmanaged exposure.
- Separating questionnaire definitions, raw responses, scoring logic, governance records, monitoring requirements, and reporting makes the workflow easier to audit and extend.
- CLI-first implementation improves reproducibility in headless or restricted infrastructure environments.

## Troubleshooting Log

### Ubuntu Runtime Difference

The execution environment provided Ubuntu 24.04 rather than the originally expected Ubuntu 22.04. Dependencies were validated against the actual environment before deployment.

### LimeSurvey Version Compatibility

The original deployment instructions referenced an older LimeSurvey 5.x release pattern. The deployment was adjusted for the PHP version available in the Ubuntu 24.04 environment.

### Invalid LimeSurvey Download Endpoint

An initially constructed LimeSurvey archive URL returned HTTP 404. The failed download occurred while the shell was configured with `set -e`, causing the remote shell to terminate immediately after the failed command.

The issue was isolated to the invalid artifact URL rather than incorrectly treating the resulting SSH disconnect as an infrastructure outage.

### Apache Virtual Host Handling

The default Apache virtual host could take precedence over the dedicated LimeSurvey configuration. The default site was disabled and the dedicated virtual host explicitly enabled.

### MariaDB Authentication

Database provisioning used local privileged MariaDB authentication rather than relying on an unnecessary interactive root-password workflow. A dedicated application account was granted access only to the LimeSurvey database.

### Headless Environment

The runtime did not provide GUI access. The vendor assessment was therefore maintained as a version-controlled CLI questionnaire definition rather than claiming completion of a browser-generated survey export.

The CLI implementation preserves the control domains, framework mappings, normalized scoring model, risk calculations, monitoring requirements, and downstream governance workflow while remaining fully reproducible from the terminal.
