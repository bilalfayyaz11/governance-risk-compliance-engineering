# STIG Security Control Assessment

A hands-on security control assessment workflow for evaluating Ubuntu 24.04 systems against a Security Technical Implementation Guide baseline using OpenSCAP and ComplianceAsCode content.

This repository demonstrates the full assessment lifecycle: planning, baseline selection, automated evaluation, findings triage, controlled remediation, reassessment, evidence preservation, and formal Security Assessment Report generation.

## What This Demonstrates

- Security Assessment Plan development
- Assessor independence documentation
- OpenSCAP-based technical control assessment
- Ubuntu 24.04 STIG baseline evaluation
- XCCDF result analysis
- Security finding classification and triage
- Risk-based remediation prioritization
- Controlled configuration remediation
- Before-and-after compliance validation
- Evidence integrity using SHA-256
- Security Assessment Report development
- POA&M-oriented handling of unresolved findings

## Assessment Workflow

The implementation follows this sequence:

    Security Assessment Plan
            |
            v
    STIG Baseline Selection
            |
            v
    OpenSCAP Assessment
            |
            v
    XCCDF Evidence
            |
            v
    Findings Extraction
            |
            v
    Risk Triage
            |
            v
    Controlled Remediation
            |
            v
    OpenSCAP Reassessment
            |
            v
    Verification Evidence
            |
            v
    Security Assessment Report

## Technology Stack

- Ubuntu 24.04 LTS
- OpenSCAP
- ComplianceAsCode Security Content
- XCCDF
- SCAP datastreams
- Python
- Bash
- CSV
- SHA-256
- Markdown

## Repository Structure

    stig-security-control-assessment/
    ├── plans/
    │   └── assessment_plan.md
    │
    ├── findings/
    │   ├── all-failed-findings.csv
    │   ├── findings_triage.csv
    │   ├── remediation-record.txt
    │   └── remediation-verification.txt
    │
    ├── evidence/
    │   ├── assessment-metadata.txt
    │   ├── initial-counts.txt
    │   ├── scan-results.xml
    │   ├── rescan-results.xml
    │   ├── initial-evidence.sha256
    │   └── remediation-evidence.sha256
    │
    ├── reports/
    │   ├── scan-report.html
    │   ├── rescan-report.html
    │   ├── security_assessment_report.md
    │   └── security_assessment_report.sha256
    │
    ├── .gitignore
    └── README.md

## Security Assessment Plan

The assessment plan defines:

- assessment scope
- technical objectives
- methodology
- assessor responsibilities
- system owner responsibilities
- assessor independence
- assessment evidence
- schedule
- operational constraints
- authorization assumptions

The plan establishes the assessment context before technical scanning begins.

## STIG Assessment

The target system is evaluated using OpenSCAP against the Ubuntu 24.04 STIG profile:

    xccdf_org.ssgproject.content_profile_stig

The assessment uses an Ubuntu 24.04 SCAP datastream:

    ssg-ubuntu2404-ds.xml

A typical assessment command is:

    sudo oscap xccdf eval \
      --profile xccdf_org.ssgproject.content_profile_stig \
      --results results/scan-results.xml \
      --report results/scan-report.html \
      ssg-ubuntu2404-ds.xml

The XCCDF results preserve machine-readable evidence while the HTML report provides a human-readable assessment view.

## Findings Analysis

Assessment results are parsed to identify failed technical rules.

Each finding is enriched with:

- rule identifier
- control title
- SCAP severity
- STIG category
- risk rating
- remediation owner
- remediation target date
- remediation status

The complete failure inventory is stored in:

    findings/all-failed-findings.csv

Prioritized findings are maintained in:

    findings/findings_triage.csv

## Risk-Based Remediation

Remediation is intentionally constrained to changes that can be implemented without creating unnecessary operational risk.

Controls affecting areas such as:

- remote access
- authentication
- PAM
- firewall policy
- boot configuration
- kernel configuration
- storage layout
- cryptographic enforcement

should undergo explicit operational-impact review before modification.

This prevents compliance automation from becoming a source of availability or access failures.

## Verification

After selected controls are remediated, the system is assessed again using the same STIG profile.

The reassessment produces:

    evidence/rescan-results.xml

and:

    reports/rescan-report.html

Selected control results are compared between the initial assessment and the reassessment.

Example verification logic:

    fail -> pass

A remediation is considered verified only when the reassessment evidence confirms the expected control-state transition.

Verification records are maintained in:

    findings/remediation-verification.txt

## Evidence Integrity

Assessment artifacts are hashed using SHA-256.

Initial assessment evidence:

    evidence/initial-evidence.sha256

Post-remediation evidence:

    evidence/remediation-evidence.sha256

This provides a simple integrity mechanism for detecting unintended modification of assessment artifacts.

## Security Assessment Report

The final Security Assessment Report is available at:

    reports/security_assessment_report.md

The report includes:

1. Executive Summary
2. Assessment Scope and Methodology
3. Results Summary
4. Detailed Findings
5. Remediation Status
6. Assessor Conclusion
7. Assessment Limitations
8. Evidence and Appendices

The report deliberately distinguishes automated technical assessment results from broader organizational compliance or authorization conclusions.

## Important Assessment Principle

A passing OpenSCAP rule does not automatically prove that an organization is fully compliant.

Automated SCAP assessments primarily validate machine-testable technical configurations.

Areas such as:

- governance
- policy
- personnel controls
- physical controls
- procedural controls
- risk acceptance
- compensating controls
- authorization decisions

require separate assessment evidence.

Likewise, a simple pass percentage should not be interpreted as an official STIG compliance score or authorization decision.

## Handling Unresolved Findings

Remaining findings should be:

- validated for applicability
- reviewed for operational impact
- assigned to accountable owners
- prioritized according to risk
- tracked through remediation
- documented in a POA&M where appropriate
- supported by compensating controls or approved exceptions when remediation is not feasible

This mirrors real security assessment and authorization workflows more closely than simply forcing every automated check into a passing state.

## Key Engineering Outcomes

This implementation demonstrates the ability to:

- translate compliance requirements into technical assessment workflows
- operate OpenSCAP and SCAP security content
- interpret XCCDF assessment evidence
- distinguish invalid assessments from valid evidence
- design risk-aware remediation processes
- verify control effectiveness through reassessment
- preserve assessment evidence integrity
- communicate findings in an assessor-oriented report
- avoid overstating automated compliance results

## Relevant Roles

This work is directly relevant to:

- GRC Engineer
- Security Compliance Engineer
- Security Engineer
- DevSecOps Engineer
- Cloud Security Engineer
- Security Assurance Analyst
- Security Control Assessor
- Platform Security Engineer
