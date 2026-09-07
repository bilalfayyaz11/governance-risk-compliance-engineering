# POA&M Remediation Tracking

An automated security remediation workflow that converts assessment findings into accountable remediation records and exports the resulting risk state as structured OSCAL Plan of Action and Milestones (POA&M) data.

## Overview

Security assessments are useful only when their findings become owned, measurable remediation work.

This implementation connects assessment output with an operational remediation lifecycle:

    Security Assessment Findings
              |
              v
       Structured JSON Input
              |
              v
        Redmine REST API
              |
              v
       Remediation Tickets
              |
        +-----+------+---------+
        |            |         |
        v            v         v
      Owner       Milestone   SLA
                              |
                              v
                         Target Date
                              |
              +---------------+---------------+
              |                               |
              v                               v
          Remediate                     Risk Decision
                                              |
                                              v
                                        Residual Risk
                                              |
                                              v
                                      OSCAL POA&M Export

The workflow demonstrates how security findings can move from assessment through remediation planning, ownership, risk disposition, residual-risk documentation, and machine-readable reporting.

## Key Capabilities

- Converts SAR-style security findings into Redmine issues through the REST API
- Prevents duplicate finding imports
- Discovers Redmine priority identifiers dynamically instead of relying on hard-coded database IDs
- Maps finding severity to remediation priority
- Assigns remediation ownership programmatically
- Implements severity-based target close dates
- Associates findings with remediation milestones
- Records formal risk treatment decisions
- Tracks residual risk after mitigation or acceptance
- Preserves risk-acceptance rationale as operational evidence
- Retrieves current remediation state through the Redmine API
- Converts tracked findings into OSCAL POA&M JSON
- Associates POA&M items with structured risk objects
- Produces human-readable POA&M reporting
- Generates SHA-256 integrity evidence for exported artifacts

## Remediation SLA Model

| Severity | Target Close | Milestone Strategy |
|---|---:|---|
| High | 30 days | Q1-Remediation |
| Medium | 60 days | Q1-Remediation |
| Low | 90 days | Q2-Remediation |

These values demonstrate a severity-driven remediation model. Production SLA requirements should be derived from organizational risk policy, contractual requirements, regulatory obligations, and system impact.

## Risk Treatment Model

Findings support three dispositions:

| Decision | Meaning |
|---|---|
| Remediate | Reduce the risk by implementing corrective action |
| Risk Accepted | Formally retain the identified residual risk |
| Transferred | Shift responsibility or financial impact through an appropriate risk-transfer mechanism |

Risk acceptance is treated as an accountable decision rather than as remediation.

The workflow records:

- finding identifier
- security control
- original severity
- remediation owner
- target milestone
- target close date
- risk decision
- residual risk
- decision rationale and review conditions

## Example Risk Acceptance

The Low-severity `F-003` finding demonstrates the risk-acceptance path.

Recorded state:

    Finding: F-003
    Control: AU-6
    Decision: Risk Accepted
    Residual Risk: Low
    Decision Authority: ISSO (simulated)
    Review Period: 12 months

The finding remains visible in the risk record even though remediation is not currently required. This preserves traceability between the identified weakness and the accountable risk decision.

## Automation

### Finding Import

`automation/import_findings.py`

Loads structured SAR findings, discovers available Redmine priorities, maps severity to the appropriate priority, detects existing findings, and creates remediation tickets through the Redmine REST API.

### Remediation Assignment

`automation/assign_remediation.py`

Applies ownership, milestones, and severity-based target close dates to existing findings through API-driven bulk updates.

### OSCAL Export

`automation/export_oscal_poam.py`

Retrieves the current remediation state from Redmine and transforms findings into a structured OSCAL POA&M representation containing POA&M items, related risks, remediation information, target dates, dispositions, and residual-risk metadata.

## Repository Structure

    poam-remediation-tracking/
    ├── automation/
    │   ├── assign_remediation.py
    │   ├── export_oscal_poam.py
    │   └── import_findings.py
    ├── evidence/
    │   ├── assignment_results.json
    │   ├── poam_export.json
    │   ├── poam_export.sha256
    │   └── risk_acceptance_evidence.json
    ├── input/
    │   └── sar_findings.json
    ├── reports/
    │   └── poam_summary.md
    ├── .gitignore
    └── README.md

## Data Flow

1. Assessment findings are represented as structured JSON.
2. The import automation validates each finding.
3. Redmine priorities are discovered through the REST API.
4. Each finding becomes a trackable remediation issue.
5. Ownership and target dates are assigned according to remediation policy.
6. Findings are associated with remediation milestones.
7. Risk treatment and residual-risk information are recorded.
8. Current ticket state is retrieved through the API.
9. The state is transformed into OSCAL POA&M JSON.
10. Human-readable reporting and integrity evidence are generated.

## Example Finding Input

    {
      "id": "F-001",
      "title": "Unpatched OpenSSL vulnerability",
      "severity": "High",
      "control": "SI-2"
    }

The same finding becomes a remediation record containing ownership, priority, milestone, target date, status, and associated risk information.

## OSCAL POA&M

The exported POA&M models the relationship between operational remediation tickets and structured security risk information.

Each exported item includes relevant tracking properties such as:

- finding ID
- control ID
- severity
- ticket status
- remediation owner
- milestone
- target close date
- risk decision
- residual risk
- related risk UUID

Risk objects capture additional disposition and remediation information.

The export workflow is designed around the NIST OSCAL POA&M model rather than treating arbitrary JSON as OSCAL simply because it is syntactically valid.

## Validation

The workflow performs multiple validation layers:

    jq empty poam_export.json

verifies JSON syntax.

The generated document is additionally checked against the applicable NIST OSCAL POA&M JSON schema during execution.

Artifact integrity is recorded with:

    sha256sum poam_export.json poam_summary.md

This separates three different concerns:

- syntactic JSON validity
- OSCAL structural validation
- artifact integrity

## Security Considerations

Authentication material is intentionally excluded from the repository.

Local API configuration such as:

    .redmine.env

must never be committed because it contains the Redmine API credential.

The repository also excludes:

- SQLite databases
- runtime logs
- environment files
- virtual environments
- credentials
- temporary application data

A production deployment should additionally use TLS, dedicated service identities, centralized secret management, least-privilege API access, database backups, hardened authentication, and auditable risk-approval workflows.

## Technologies

- Ubuntu Linux
- Redmine
- Ruby / Rails
- SQLite
- Python
- Requests
- REST APIs
- JSON
- jq
- OSCAL
- SHA-256
- NIST RMF concepts

## Governance and Security Engineering Value

This implementation demonstrates the operational bridge between security assessment and continuous remediation.

Rather than stopping at vulnerability identification, the workflow provides evidence of:

- finding normalization
- remediation accountability
- SLA-driven tracking
- milestone management
- risk treatment
- residual-risk documentation
- risk acceptance
- machine-readable compliance reporting
- evidence integrity

These capabilities are applicable to security engineering, GRC engineering, security operations, continuous monitoring, authorization support, and remediation governance workflows.

## Production Extensions

A production implementation could extend this design with:

- authenticated TLS termination
- PostgreSQL
- enterprise identity integration
- role-based approval workflows
- automated scanner ingestion
- vulnerability-management integrations
- SIEM integration
- notification and escalation workflows
- SLA breach detection
- dashboards and remediation metrics
- formal POA&M approval gates
- continuous OSCAL generation
- CI-based OSCAL schema validation
- automated evidence retention

## Disclaimer

The users, findings, risk authority, milestones, and system context represented here are simulated for engineering demonstration purposes. They should not be interpreted as evidence of an authorization decision or production risk acceptance.
