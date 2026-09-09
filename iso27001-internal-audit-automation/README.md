# ISO 27001 Internal Audit Automation

## Overview

This implementation provides a structured internal ISMS audit workflow aligned with ISO/IEC 27001:2022 concepts.

It combines:

- audit planning
- Annex A control sampling
- evidence collection
- interview documentation
- technical walkthroughs
- nonconformity logging
- corrective action tracking
- automated report generation
- PDF export

The workflow demonstrates how a lightweight audit evidence pipeline can be built using Linux, Python, CSV, Markdown, and Pandoc.

## Architecture

    Audit Scope and Criteria
            |
            v
    ┌─────────────────────────────┐
    │        Audit Plan           │
    │                             │
    │ • Objectives                │
    │ • Scope                     │
    │ • Criteria                  │
    │ • Roles                     │
    │ • Schedule                  │
    └──────────────┬──────────────┘
                   |
                   v
    ┌─────────────────────────────┐
    │      Annex A Checklist      │
    │                             │
    │ • Control status            │
    │ • Category                  │
    │ • Evidence reference        │
    └──────────────┬──────────────┘
                   |
          ┌────────┴─────────┐
          |                  |
          v                  v
      Interviews       Technical Walkthroughs
          |                  |
          └────────┬─────────┘
                   |
                   v
    ┌─────────────────────────────┐
    │      Findings Register      │
    │                             │
    │ • Major                     │
    │ • Minor                     │
    │ • Observation               │
    └──────────────┬──────────────┘
                   |
                   v
    ┌─────────────────────────────┐
    │ Corrective Action Plan      │
    │                             │
    │ • Owner                     │
    │ • Target date               │
    │ • Status                    │
    │ • Closure evidence          │
    └──────────────┬──────────────┘
                   |
                   v
       Internal Audit Report
          Markdown + PDF

## Audit Scenario

The audit models a fictitious organization:

    Meridian FinTech Services Ltd.

The sampled ISMS scope includes:

- cloud infrastructure
- privileged access
- secure authentication
- configuration management
- monitoring
- HR onboarding
- security awareness
- termination responsibilities
- cloud governance
- incident readiness
- ICT continuity
- physical security monitoring

## Audit Criteria

The audit plan references:

- ISO/IEC 27001:2022 Clauses 4–10
- selected Annex A controls
- internal configuration expectations
- simulated organizational policies

The detailed audit criteria are maintained in:

    plan/audit_plan.md

## Selected Annex A Controls

The sample checklist contains 15 controls across the four Annex A categories:

- Organizational
- People
- Physical
- Technological

The checklist is stored in:

    plan/annex_a_checklist.csv

Example controls include:

- A.5.1 — Policies for information security
- A.5.7 — Threat intelligence
- A.5.15 — Access control
- A.5.23 — Information security for use of cloud services
- A.6.3 — Information security awareness, education and training
- A.7.4 — Physical security monitoring
- A.8.2 — Privileged access rights
- A.8.5 — Secure authentication
- A.8.9 — Configuration management
- A.8.16 — Monitoring activities
- A.8.23 — Web filtering

## Checklist Automation

The checklist helper is implemented in:

    scripts/checklist_summary.py

It loads the Annex A sample using pandas and summarizes:

- total controls
- status distribution
- category distribution

Statuses include:

- Not Tested
- Conforms
- Nonconformity
- Observation
- Partially Tested

## Evidence Collection

Evidence is stored under:

    evidence/

The evidence set includes:

- interview template
- cloud infrastructure interview
- HR awareness interview
- Linux password-policy output
- technical walkthrough notes

## Interview Evidence

### Configuration Management

The technical interview focused on:

    A.8.9 — Configuration management

Topics included:

- configuration baselines
- change approval
- configuration review
- drift detection
- compliance monitoring

### Awareness

The HR interview focused on:

    A.6.3 — Information security awareness, education and training

Topics included:

- onboarding awareness
- annual refreshers
- completion evidence
- policy-change communication

## Technical Walkthrough

A local Linux configuration was inspected using:

    /etc/login.defs

The walkthrough captured:

    PASS_MAX_DAYS
    PASS_MIN_DAYS
    PASS_WARN_AGE

The sampled environment showed:

    PASS_MAX_DAYS = 99999

The simulated organizational requirement used for the audit was:

    Maximum password age <= 90 days

This resulted in a Minor Nonconformity for the sampled configuration.

## Evidence Limitation

The `/etc/login.defs` file provides default password-aging settings.

It does not, by itself, prove the effective configuration of every existing account.

A real audit should supplement this with:

- account-level password aging
- identity-provider configuration
- PAM configuration
- authentication architecture
- approved configuration baselines

## Checklist Update Automation

Checklist updates are handled by:

    scripts/update_checklist.py

The script validates:

- control identity
- status value
- evidence reference

and updates the CSV without manually editing rows.

## Findings Register

The finding register is stored in:

    findings/nonconformity_register.csv

A reusable logger is implemented in:

    scripts/log_finding.py

It automatically:

- generates sequential finding IDs
- validates severity
- appends finding details
- includes the current date
- records evidence and recommendations

Example IDs:

    F001
    F002

## Finding Classification

### Major

Used where there is evidence of:

- systemic breakdown
- absence of a required process
- widespread failure
- inability of the ISMS to achieve intended outcomes

### Minor

Used for:

- isolated implementation failure
- partial control breakdown
- limited deviation from an established process

### Observation

Used where:

- no formal nonconformity is established
- an improvement opportunity exists
- assurance maturity can be strengthened

## Findings

### F001 — Minor Nonconformity

Control:

    A.8.9 — Configuration management

Condition:

The sampled Linux password-aging value exceeded the simulated internal limit.

Evidence:

    evidence/A8_9_password_policy_evidence.txt

Recommendation:

Review applicable local accounts and align the configuration with the approved password-aging requirement.

### F002 — Observation

Control:

    A.6.3 — Information security awareness, education and training

Condition:

The awareness process was described during interview, but independent sample evidence of annual refresher completion was not retrieved.

Recommendation:

Introduce periodic evidence sampling and maintain auditable completion records.

## Corrective Action Plan

The CAP is stored in:

    reports/corrective_action_plan.csv

It tracks:

- Finding ID
- Severity
- Corrective Action
- Owner
- Target Date
- Status

The generated report also explains that corrective actions should not be considered closed solely because implementation has been reported.

Closure should include:

- implementation evidence
- responsible owner confirmation
- audit or ISMS review
- effectiveness verification
- retained closure evidence

## Audit Report

The report generator is implemented in:

    scripts/generate_audit_report.py

It produces:

    reports/internal_audit_report.md
    reports/internal_audit_report.pdf

The report includes:

- Executive Summary
- Audit Information
- Audit Objective
- Audit Criteria
- Methodology
- Evidence Reviewed
- Checklist Summary
- Findings Summary
- Corrective Action Plan
- Overall Audit Conclusion
- Risk and Governance Implications
- Follow-Up Requirements
- Audit Limitations
- Auditor Statement

## PDF Generation

The final PDF is generated with:

    pandoc internal_audit_report.md \
        -o internal_audit_report.pdf \
        --pdf-engine=pdflatex

This creates a portable audit deliverable suitable for management review.

## Repository Structure

    iso27001-internal-audit-automation/
    ├── README.md
    ├── plan/
    │   ├── annex_a_checklist.csv
    │   └── audit_plan.md
    ├── evidence/
    │   ├── interview_log_template.md
    │   ├── interview_01.md
    │   ├── interview_02.md
    │   ├── A8_9_password_policy_evidence.txt
    │   └── A8_9_walkthrough_notes.md
    ├── findings/
    │   └── nonconformity_register.csv
    ├── scripts/
    │   ├── checklist_summary.py
    │   ├── update_checklist.py
    │   ├── log_finding.py
    │   └── generate_audit_report.py
    └── reports/
        ├── corrective_action_plan.csv
        ├── internal_audit_report.md
        └── internal_audit_report.pdf

## Tools Used

- Ubuntu Linux
- Python 3
- pandas
- tabulate
- Bash
- Markdown
- Pandoc
- LaTeX
- CSV
- ISO/IEC 27001:2022 audit concepts

## Key Skills Demonstrated

- ISMS internal audit planning
- scope and criteria definition
- ISO 27001 evidence evaluation
- Annex A control sampling
- interview documentation
- technical walkthroughs
- configuration evidence review
- nonconformity classification
- evidence traceability
- audit register automation
- Python CSV automation
- corrective action governance
- audit reporting
- PDF report generation
- CGRC-aligned assurance workflows

## Real-World Use Case

Internal ISMS audits often involve information scattered across:

- spreadsheets
- interview notes
- screenshots
- configuration outputs
- corrective action trackers
- audit reports

This implementation centralizes those artifacts into a structured workflow.

It supports questions such as:

- Which controls were sampled?
- Which controls have evidence?
- Which findings remain open?
- What evidence supports each finding?
- Who owns corrective action?
- When is remediation due?
- Has effectiveness been verified?
- Which controls have not yet been tested?

## Audit Design Principles

### Evidence Before Conclusion

A control should not be marked conforming solely because an auditee states that a process exists.

Where appropriate, interview evidence should be supplemented with:

- records
- configuration evidence
- system output
- document evidence
- sampling

### Findings Must Be Traceable

Every finding should reference supporting evidence.

This improves:

- repeatability
- management review
- remediation quality
- follow-up verification

### Severity Must Be Defensible

Severity should reflect:

- scope of failure
- systemic impact
- process maturity
- risk implications

A single isolated configuration weakness should not automatically be classified as a major nonconformity.

### Corrective Action Requires Effectiveness Testing

Closing an action is different from proving that the underlying problem has been resolved.

Effectiveness verification should confirm that:

- the change is implemented
- the issue no longer exists
- the control operates consistently
- evidence is retained

## Limitations

This implementation uses a simulated audit environment.

It does not constitute:

- ISO certification
- certification-body assessment
- legal advice
- a complete Annex A evaluation
- a complete Statement of Applicability review
- a production ISMS conformity determination

The sample is intentionally limited so the focus remains on audit engineering, evidence handling, finding management, and report automation.

## Engineering Decisions

### Automated Status Management

Control statuses are updated programmatically rather than manually editing the checklist.

This reduces accidental CSV inconsistencies.

### Programmatic Finding IDs

Finding IDs are generated sequentially to avoid duplication and make findings easier to trace.

### Separate Evidence Repository

Evidence files remain separate from findings and reports.

This preserves traceability and allows multiple findings or controls to reference the same source when appropriate.

### Report Generation from Source Data

The final report reads directly from:

    annex_a_checklist.csv
    nonconformity_register.csv

This reduces the risk that findings in the report diverge from the underlying registers.

### Markdown as Source Format

Markdown provides a portable, version-control-friendly audit format that can be converted into PDF for executive consumption.
