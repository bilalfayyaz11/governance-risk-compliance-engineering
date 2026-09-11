# Vendor Risk Assessment and DPA Governance

## What This Does

This implementation builds an end-to-end third-party risk and privacy governance workflow for assessing a technology vendor before production approval.

It creates a structured security questionnaire, evaluates vendor responses against a defined control baseline, identifies compliance gaps automatically, converts those findings into contractual DPA requirements, evaluates cross-border processing risks, and generates a remediation tracker with severity-based deadlines.

The workflow demonstrates how vendor risk decisions can be supported by repeatable technical evidence rather than relying only on manually reviewed questionnaires and legal documents.

## Architecture

~~text
+-----------------------------+
| Vendor Security             |
| Questionnaire               |
+-------------+---------------+
              |
              v
+-----------------------------+
| Vendor Response             |
| Evidence + Disclosures      |
+-------------+---------------+
              |
              v
+-----------------------------+
| Automated Baseline Review   |
| review_responses.py         |
+-------------+---------------+
              |
       +------+------+
       |             |
       v             v
+------------+   +----------------+
| PASS / N/A |   | FAIL / MISSING |
+------------+   +-------+--------+
                        |
                +-------+---------+
                |                 |
                v                 v
        +---------------+  +------------------+
        | DPA Controls  |  | Transfer Review  |
        | Art. 28       |  | Ireland / India  |
        | UAE / KSA     |  | Safeguards       |
        +-------+-------+  +--------+---------+
                |                   |
                +---------+---------+
                          |
                          v
                +----------------------+
                | Remediation Tracker  |
                | Severity + Owner     |
                | Due Date + Status    |
                +----------------------+
~~

## Prerequisites

- Ubuntu or another Linux distribution
- Python 3.12+
- Python virtual environment support
- pip
- Git
- Basic understanding of third-party risk management
- Basic understanding of processor and sub-processor governance
- Access to current legal and regulatory guidance when applying the documents in production

Required Python packages:

- pandas
- tabulate

## Setup & Installation

~~bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv

python3 -m venv venv
source venv/bin/activate

python -m pip install --upgrade pip
python -m pip install pandas tabulate
~~

## How to Reproduce

Activate the environment:

~~bash
source venv/bin/activate
~~

Review the original questionnaire:

~~bash
column -s, -t < questionnaire/security_questionnaire.csv
~~

Review the completed vendor response:

~~bash
column -s, -t < responses/vendor_acme_response.csv
~~

Run the automated response assessment:

~~bash
python tracker/review_responses.py
column -s, -t < tracker/vendor_acme_gap_report.csv
~~

Inspect flagged controls:

~~bash
grep -E "FAIL|MISSING" tracker/vendor_acme_gap_report.csv
~~

Generate the remediation tracker:

~~bash
python tracker/build_tracker.py
column -s, -t < tracker/remediation_tracker.csv
~~

Validate the baseline:

~~bash
python -m json.tool tracker/baseline.json
~~

Check contractual documentation for unfinished placeholders:

~~bash
grep -c "TODO" \
    dpa/DPA_draft.md \
    dpa/cross_border_addendum.md
~~

Both files should return zero unresolved TODO entries.

## Control Baseline

The automated assessment evaluates selected controls using required response indicators.

| Control | Domain | Required Indicator | Severity |
|---|---|---|---|
| C1 | Access Control | MFA | High |
| C2 | Encryption at Rest | AES-256 | High |
| C3 | Encryption in Transit | TLS | High |
| C4 | Sub-processing | location | Critical |
| C6 | Breach Notification | hours | Medium |
| C7 | Data Deletion | 30 days | High |

Controls outside the configured automated baseline are retained in the questionnaire but reported as `N/A` by the scoring engine.

## Assessment Results

The simulated vendor response demonstrates both compliant and non-compliant conditions.

### Passing Controls

- C1 — MFA is enforced for privileged administrator access
- C2 — AES-256 encryption is stated for production storage
- C3 — TLS 1.2 / TLS 1.3 is stated for transport encryption
- C6 — 24-hour initial breach-notification target is documented

### Flagged Controls

#### C4 — Critical

The vendor disclosed:

- AWS in Ireland
- SubProcessor-X in India

However, the submitted response did not satisfy the configured baseline and did not provide sufficient detail for full approval.

Required remediation includes:

- complete legal entity details
- processing purposes
- all processing locations
- onward-transfer information
- applicable transfer mechanisms
- security safeguards

#### C7 — High

The vendor did not provide a response confirming deletion within the required contractual period.

Required remediation includes:

- documented deletion procedure
- deletion timeline
- backup handling
- sub-processor deletion obligations
- deletion certification or equivalent evidence

## DPA Governance

The DPA addresses:

- processing subject matter and duration
- categories of data subjects and personal data
- documented processing instructions
- confidentiality requirements
- security measures
- assistance obligations
- audit rights
- breach notification
- deletion and return
- sub-processor authorization
- sub-processor objection rights
- flow-down obligations
- international transfers

### GDPR

The agreement incorporates processor and sub-processor concepts aligned with GDPR Article 28, including authorization and contractual flow-down expectations.

### UAE PDPL

The agreement references processor obligations under UAE Federal Decree-Law No. 45 of 2021, including processing within documented instructions and maintaining appropriate safeguards.

### KSA PDPL

The agreement incorporates Saudi processor and subsequent sub-processor governance concepts, including Controller oversight and sub-processing controls.

Legal applicability should always be validated against current law, implementing regulations, regulatory guidance, and the actual contractual relationship.

## Sub-Processor Governance

Current disclosed processing relationships:

| Provider | Location | Role | Assessment |
|---|---|---|---|
| AWS | Ireland | Infrastructure / hosting | Disclosed |
| SubProcessor-X | India | Support / processing | Further review required |

The Processor must provide advance notice before introducing material sub-processor changes.

The Controller retains the ability to raise reasonable privacy or security objections.

Equivalent privacy and security obligations must flow down contractually to approved sub-processors.

## Cross-Border Transfer Governance

The transfer addendum evaluates international processing separately from basic vendor disclosure.

A disclosed processing location is not automatically an approved transfer.

The review considers:

- destination jurisdiction
- recipient identity
- processing purpose
- applicable transfer mechanism
- onward transfers
- security controls
- contractual safeguards
- transfer risk assessments
- supplementary technical and organizational measures

### Ireland

Ireland-based AWS infrastructure is within the EEA when processing remains in Ireland.

Additional review is still necessary for:

- remote administrative access
- support locations
- telemetry
- disaster recovery
- downstream sub-processors
- onward transfers

### India

Processing through SubProcessor-X in India remains subject to further approval.

Required evidence includes:

- legal entity details
- processing scope
- storage and remote-access locations
- transfer mechanism
- security safeguards
- onward-transfer arrangements
- deletion controls

## Remediation Automation

The remediation generator converts failed or missing controls into actionable entries.

Deadline logic:

~~text
Critical → 7 days
High     → 14 days
Medium   → 30 days
~~

Current ownership:

~~text
C4 → Privacy Counsel
C7 → Vendor Risk Manager
~~

Each remediation record contains:

- control ID
- issue
- severity
- owner
- due date
- status

This allows identified assessment gaps to move directly into a trackable remediation workflow.

## Repository Structure

~~text
vendor-risk-assessment/
├── README.md
├── questionnaire/
│   └── security_questionnaire.csv
├── responses/
│   └── vendor_acme_response.csv
├── dpa/
│   ├── DPA_draft.md
│   └── cross_border_addendum.md
└── tracker/
    ├── activity_log.txt
    ├── baseline.json
    ├── review_responses.py
    ├── vendor_acme_gap_report.csv
    ├── build_tracker.py
    └── remediation_tracker.csv
~~

## Tools Used

- Python 3
- CSV
- JSON
- pandas
- tabulate
- Markdown
- Bash
- Linux CLI
- Git

## Key Skills Demonstrated

- Third-party risk management
- Vendor security assessment
- Control-baseline design
- Automated questionnaire review
- Compliance gap analysis
- Privacy engineering
- Processor and sub-processor governance
- DPA structure and control mapping
- Cross-border transfer assessment
- Remediation automation
- Severity-based deadline management
- Evidence-driven vendor approval
- Compliance documentation
- Python-based governance tooling

## Real-World Use Case

A company onboarding a SaaS, infrastructure, analytics, or support vendor must determine whether that provider can safely process customer or employee information.

Security questionnaires alone are insufficient if responses are not evaluated consistently.

This implementation provides a repeatable workflow in which vendor statements are compared against defined control expectations, material gaps are escalated according to severity, contractual controls are documented, international processing is separately assessed, and unresolved findings become assigned remediation actions.

The pattern can be extended into a production third-party risk platform with workflow approvals, evidence attachments, vendor portals, continuous monitoring, ticketing integration, expiry dates, and executive risk reporting.

## Lessons Learned

- Vendor questionnaires are substantially more useful when responses are evaluated against explicit and reproducible acceptance criteria.
- Missing responses should be treated differently from responses that explicitly fail a control requirement.
- Contract drafting and technical vendor assessment should be connected rather than operating as isolated processes.
- Sub-processor disclosure does not itself establish that an international transfer is acceptable.
- Severity-based remediation deadlines create a practical bridge between assessment findings and operational closure.
- Legal article references should be verified before being embedded into reusable contractual templates.

## Troubleshooting Log

### Missing pip and Python Packages

The fresh environment contained Python but did not include pip or the required third-party packages.

Resolution:

~~bash
sudo apt-get install -y python3-pip python3-venv

python3 -m venv venv
source venv/bin/activate

python -m pip install pandas tabulate
~~

### Fragile Gap-Analysis Paths

The source workflow expected execution from the tracker directory while referencing paths that would resolve incorrectly from that location.

The implementation instead derives the application root using:

~~python
Path(__file__).resolve().parent.parent
~~

This makes the scoring script independent of the current shell directory.

### UAE Article Reference

The original contractual skeleton associated processor obligations with UAE PDPL Article 10.

The implementation corrected this reference and treats processor obligations under the appropriate processor provisions while avoiding blind reliance on the supplied article numbering.

### KSA Sub-Processor References

The original instructions broadly referenced KSA PDPL Articles 11-13 for sub-processing requirements.

The implementation instead frames the contractual language around current processor and subsequent sub-processor requirements and notes that legal applicability must be verified against current Saudi law and implementing regulations.

### C4 Baseline Failure

The vendor disclosed sub-processors but the configured baseline required the keyword `location`.

Because the vendor response did not contain that required indicator, C4 correctly evaluated as:

~~text
FAIL / Critical
~~

The failure demonstrates that automated keyword checks should be considered a screening mechanism rather than a substitute for substantive human review.

### C7 Missing Response

The vendor left its deletion response blank.

The review engine correctly distinguished this condition as:

~~text
MISSING / High
~~

rather than ordinary failure.

### Remediation Ownership

The original tracker design defaulted all owners to `TBD`.

The implementation maps known findings to accountable functions:

~~text
C4 → Privacy Counsel
C7 → Vendor Risk Manager
~~

This produces a more operationally useful remediation register.
