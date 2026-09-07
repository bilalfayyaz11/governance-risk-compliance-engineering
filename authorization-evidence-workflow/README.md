# Authorization Evidence Workflow

A Linux-based security authorization workflow that assembles a structured ATO package, validates authorization artifacts, creates a cryptographically verifiable evidence snapshot, generates an executive authorization briefing, and records the final authorization decision in a tamper-evident hash-chained ledger.

## Overview

This implementation models the final authorization stage of a security governance lifecycle.

The workflow connects:

    System Security Plan
            |
            v
    Security Assessment Report
            |
            v
           POA&M
            |
            v
      Risk Assessment
            |
            v
    Executive Risk Summary
            |
            v
      AO Decision Briefing
            |
            v
      Signed Evidence Index
            |
            v
    Authorization Decision
            |
            v
    Hash-Chained Decision Ledger

The system used in the demonstration is a fictitious mid-tier customer records platform processing sensitive information.

## Core Authorization Artifacts

The package contains:

- System Security Plan
- Security Assessment Report
- Plan of Action and Milestones
- Risk Assessment
- Executive Risk Summary
- Authorizing Official briefing
- Authorization Decision Memorandum
- Cryptographic evidence index
- Detached GPG signature
- Authorization decision ledger

## Security Control Coverage

The System Security Plan documents implementation status across selected NIST SP 800-53 controls including:

- Account Management
- Least Privilege
- Event Logging
- Audit Review
- Identification and Authentication
- Authenticator Management
- Transmission Protection
- Data-at-Rest Protection
- Flaw Remediation
- System Backup

The authorization workflow demonstrates how control implementation, assessment results, remediation status, and residual risk combine into an executive risk decision.

## Assessment Findings

The simulated assessment identified:

| Finding | Risk | Outcome |
|---|---|---|
| Outstanding software security remediation | High | Remediate |
| Password policy enforcement gap | Medium | Remediate |
| Audit review evidence gap | Low | Risk Accepted |
| Backup restoration testing gap | Medium | Remediate |

These findings feed directly into the POA&M and authorization recommendation.

## Authorization Recommendation

The assessed posture supports:

    Authorize with Conditions

Recommended authorization mechanism:

    Interim ATO

The recommendation requires:

- closure of the elevated software weakness within 30 days
- authentication hardening within 60 days
- documented recovery testing within 60 days
- continued POA&M monitoring
- periodic reassessment of accepted residual risk

The simulated recommendation does not represent a real authorization decision.

## Artifact Validation

`automation/validate_artifacts.py` validates the required authorization artifacts.

It verifies:

- SSP exists and is non-empty
- SAR exists and is non-empty
- risk assessment exists and is non-empty
- POA&M exists
- POA&M contains required columns
- POA&M records contain required values

Required POA&M columns:

    id
    weakness
    control
    severity
    status
    milestone
    due_date

## Evidence Integrity

`automation/build_evidence_index.py` recursively inventories package artifacts and calculates SHA-256 hashes.

Each evidence entry records:

- relative path
- SHA-256 digest
- size in bytes
- UTC indexing timestamp

The evidence index itself is excluded from its own hash set.

`automation/verify_evidence_index.py` independently recalculates each artifact hash and detects:

- missing files
- size changes
- content changes
- hash mismatches

## Cryptographic Signature

The evidence index is protected with a detached GPG signature.

This provides cryptographic integrity and authenticity for the indexed authorization snapshot.

The demonstration signing identity is intentionally simulated and does not represent an organizational PKI identity or real Authorizing Official.

No private GPG key material is stored in this repository.

## Chain of Custody

The authorization process links the final decision to the exact evidence snapshot reviewed during authorization.

The decision record contains the SHA-256 digest of:

    evidence/evidence-index.json

This provides traceability between:

- reviewed authorization evidence
- signed evidence snapshot
- executive decision
- authorization ledger entry

## Hash-Chained Authorization Ledger

`automation/record_ato_decision.py` records authorization decisions in JSON Lines format.

Each decision contains:

- UTC timestamp
- authorization decision
- authorization type
- Authorizing Official identity or role
- justification
- evidence-index SHA-256
- previous record hash
- current record hash

The first entry references:

    previous_record_hash = GENESIS

Every subsequent record references the SHA-256 hash of the immediately preceding record.

This creates a tamper-evident sequence.

## Ledger Verification

`automation/verify_ato_decision_log.py` verifies:

- valid JSON records
- valid authorization decisions
- evidence hash format
- previous-record linkage
- record-level SHA-256 hashes
- complete chain continuity

Modification of an earlier entry causes downstream chain verification to fail.

## Why JSONL

JSON Lines was selected because it supports append-oriented authorization history without rewriting previous records.

Benefits include:

- machine-readable audit records
- simple chronological append operations
- independent record parsing
- integration with automation pipelines
- version-control compatibility
- downstream SIEM or governance ingestion

A local JSONL file is not inherently immutable.

Production implementations should combine this design with digitally signed decisions, protected storage, centralized logging, controlled write access, trusted timestamps, and immutable archival systems.

## AO Briefing

The executive briefing translates technical findings into business-oriented risk language.

It covers:

- overall residual risk posture
- top residual risks
- remediation timelines
- accepted risk
- evidence integrity
- recommended authorization decision

The briefing is generated as Reveal.js HTML using Pandoc.

## Repository Structure

    authorization-evidence-workflow/
    ├── automation/
    │   ├── build_evidence_index.py
    │   ├── record_ato_decision.py
    │   ├── validate_artifacts.py
    │   ├── verify_ato_decision_log.py
    │   └── verify_evidence_index.py
    ├── briefing/
    │   ├── ao-briefing.html
    │   ├── ao-briefing.md
    │   └── executive-risk-summary.md
    ├── decision/
    │   ├── ato-decision-log.jsonl
    │   ├── decision-memo.md
    │   └── rationale.md
    ├── evidence/
    │   ├── chain-of-custody.txt
    │   ├── evidence-index.json
    │   └── evidence-index.json.sig
    ├── poam/
    │   └── poam.csv
    ├── risk-assessment/
    │   └── risk-assessment.md
    ├── sar/
    │   └── security-assessment-report.md
    ├── ssp/
    │   └── system-security-plan.md
    ├── .gitignore
    └── README.md

## Technologies

- Ubuntu Linux
- Python
- Bash
- Markdown
- CSV
- JSON / JSONL
- Pandoc
- Reveal.js
- GnuPG
- SHA-256
- jq
- NIST RMF concepts
- NIST SP 800-53 concepts

## Security Engineering Value

This workflow demonstrates the transition from security-control implementation and assessment into formal authorization decision support.

It combines:

- governance documentation
- risk analysis
- remediation management
- artifact validation
- evidence integrity
- cryptographic signing
- executive communication
- authorization traceability
- tamper-evident audit records

These capabilities are directly relevant to GRC engineering, security authorization, continuous monitoring, cloud security governance, security engineering, and information assurance workflows.

## Production Extensions

A production implementation could add:

- OSCAL-native SSP and assessment artifacts
- enterprise PKI signing
- identity-backed AO approvals
- immutable evidence storage
- WORM retention
- trusted timestamping
- automated POA&M ingestion
- scanner integrations
- continuous authorization pipelines
- cloud control evidence collection
- ticketing integrations
- authorization-expiration monitoring
- automated reassessment triggers
- SIEM integration
- policy-as-code authorization gates

## Disclaimer

All system details, findings, users, authorization authorities, risks, and decisions in this repository are simulated for engineering demonstration purposes.

The repository does not represent a real Authority to Operate, production authorization decision, or formal organizational risk acceptance.
