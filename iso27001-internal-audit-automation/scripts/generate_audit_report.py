#!/usr/bin/env python3

from pathlib import Path
from datetime import date

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent

CHECKLIST = ROOT / "plan" / "annex_a_checklist.csv"
FINDINGS = ROOT / "findings" / "nonconformity_register.csv"
REPORT = ROOT / "reports" / "internal_audit_report.md"


def status_summary(df: pd.DataFrame) -> dict:
    return (
        df["Status"]
        .value_counts()
        .to_dict()
    )


def severity_summary(df: pd.DataFrame) -> dict:
    return (
        df["Severity"]
        .value_counts()
        .to_dict()
    )


def markdown_table(df: pd.DataFrame) -> str:
    return df.to_markdown(
        index=False
    )


def main() -> None:
    if not CHECKLIST.exists():
        raise FileNotFoundError(
            f"Missing checklist: {CHECKLIST}"
        )

    if not FINDINGS.exists():
        raise FileNotFoundError(
            f"Missing findings register: {FINDINGS}"
        )

    checklist = pd.read_csv(
        CHECKLIST,
        keep_default_na=False,
    )

    findings = pd.read_csv(
        FINDINGS,
        keep_default_na=False,
    )

    status_counts = status_summary(
        checklist
    )

    severity_counts = severity_summary(
        findings
    )

    total_controls = len(
        checklist
    )

    tested_controls = int(
        (
            checklist["Status"]
            != "Not Tested"
        ).sum()
    )

    nonconformities = int(
        (
            findings["Severity"]
            .isin(
                [
                    "Major",
                    "Minor",
                ]
            )
        ).sum()
    )

    observations = int(
        (
            findings["Severity"]
            == "Observation"
        ).sum()
    )

    findings_table = markdown_table(
        findings[
            [
                "Finding_ID",
                "Control_ID",
                "Description",
                "Severity",
                "Evidence_Ref",
                "Recommendation",
            ]
        ]
    )

    cap_rows = []

    for _, row in findings.iterrows():
        finding_id = row["Finding_ID"]
        severity = row["Severity"]

        if finding_id == "F001":
            owner = "Cloud Infrastructure Lead"
            target_date = "2026-09-30"
            action = (
                "Review applicable local accounts, update the "
                "approved Linux password-aging baseline, and "
                "remediate PASS_MAX_DAYS where local password "
                "authentication remains in use."
            )

        elif finding_id == "F002":
            owner = "HR Manager"
            target_date = "2026-10-15"
            action = (
                "Establish periodic sampling of security-awareness "
                "completion records and maintain auditable evidence "
                "of refresher completion and overdue follow-up."
            )

        else:
            owner = "ISMS Coordinator"
            target_date = "TBD"
            action = row["Recommendation"]

        cap_rows.append(
            {
                "Finding_ID":
                    finding_id,

                "Severity":
                    severity,

                "Corrective Action":
                    action,

                "Owner":
                    owner,

                "Target Date":
                    target_date,

                "Status":
                    "Open",
            }
        )

    cap = pd.DataFrame(
        cap_rows
    )

    cap_table = markdown_table(
        cap
    )

    checklist_results = markdown_table(
        checklist[
            [
                "Control_ID",
                "Control_Name",
                "Category",
                "Status",
                "Evidence_Ref",
            ]
        ]
    )

    report = f"""# Internal ISMS Audit Report

## Executive Summary

An internal audit of selected Information Security Management System controls was conducted for Meridian FinTech Services Ltd. against ISO/IEC 27001:2022 requirements and a selected Annex A control sample.

The audit identified {nonconformities} nonconformity and {observations} improvement observation across {tested_controls} controls for which audit activity was performed. The sampled evidence indicates that elements of the ISMS are implemented, but corrective action is required for the identified configuration-management weakness and additional evidence maturity is recommended for awareness assurance.

No major nonconformity was identified in the simulated audit sample.

## Audit Information

**Organization:** Meridian FinTech Services Ltd.

**Audit Type:** Internal ISMS Audit

**Audit Standard:** ISO/IEC 27001:2022

**Report Date:** {date.today().isoformat()}

**Audit Scope:** Selected governance, HR, cloud infrastructure, access-control, configuration-management, monitoring, and physical-security processes within the defined ISMS scope.

## Audit Objective

The audit objective was to evaluate whether selected ISMS processes:

- align with defined ISO/IEC 27001:2022 audit criteria
- are implemented as described
- are supported by relevant evidence
- operate sufficiently to support intended information security outcomes
- contain weaknesses requiring corrective action or improvement

## Audit Criteria

The audit criteria included:

- ISO/IEC 27001:2022 Clauses 4 through 10
- selected Annex A controls documented in `plan/annex_a_checklist.csv`
- fictitious organizational policies used for simulated evidence evaluation
- applicable internal configuration and awareness expectations

The complete audit scope and criteria are documented in:

    plan/audit_plan.md

## Methodology

The audit used a risk-based sampling approach combining:

- document review
- checklist evaluation
- auditee interviews
- technical walkthroughs
- configuration inspection
- evidence review
- finding classification
- corrective action planning

Evidence was evaluated for relevance and sufficiency within the limits of the simulated environment.

## Evidence Reviewed

The audit considered evidence including:

- configuration-management interview
- security-awareness interview
- `/etc/login.defs` technical configuration output
- technical walkthrough notes
- selected Annex A checklist status
- documented auditor assessments

Key evidence records include:

    evidence/interview_01.md
    evidence/interview_02.md
    evidence/A8_9_password_policy_evidence.txt
    evidence/A8_9_walkthrough_notes.md

## Checklist Summary

Total selected controls:

    {total_controls}

Controls with audit activity:

    {tested_controls}

Status distribution:

    {status_counts}

## Checklist Results

{checklist_results}

## Findings Summary

Severity distribution:

    {severity_counts}

{findings_table}

## Finding F001 — Minor Nonconformity

### Related Control

A.8.9 — Configuration management

### Condition

The sampled Linux configuration showed a `PASS_MAX_DAYS` value of 99999.

The fictitious organizational requirement used during the audit specifies a maximum password age of 90 days for applicable locally managed password accounts.

### Evidence

    evidence/A8_9_password_policy_evidence.txt

### Classification

    Minor Nonconformity

### Rationale

Configuration-management activities exist, but the sampled setting does not align with the stated internal requirement.

The issue is classified as minor because the available evidence indicates an isolated implementation gap rather than complete absence or systemic failure of configuration management.

### Required Action

Review applicable locally authenticated accounts and align the approved configuration baseline with the organizational password-aging requirement.

Account-level effective settings should also be verified because `/etc/login.defs` alone does not prove the current aging configuration of every existing account.

## Finding F002 — Improvement Observation

### Related Control

A.6.3 — Information security awareness, education and training

### Condition

The awareness process was described during interview and completion was said to be tracked through HR processes.

However, independent sample evidence of annual refresher completion was not retrieved during this simulated audit.

### Evidence

    evidence/interview_02.md

### Classification

    Observation

### Recommendation

Establish periodic evidence sampling and maintain an auditable completion dashboard or equivalent record that demonstrates:

- completion rates
- overdue activities
- escalation actions
- refresher participation
- evidence retention

## Corrective Action Plan

{cap_table}

## Corrective Action Governance

Corrective actions should not be considered closed solely because an implementation change was reported.

Closure should require:

1. implementation evidence
2. responsible-owner confirmation
3. auditor or ISMS review
4. effectiveness verification
5. retained closure evidence

For F001, effectiveness testing should include inspection of applicable account-level password-aging values or the actual identity mechanism in use.

For F002, follow-up should include sampling awareness completion evidence rather than relying solely on interview statements.

## Overall Audit Conclusion

The selected ISMS processes demonstrate evidence of implementation, but the audit identified one minor nonconformity and one opportunity for improvement.

Based on the limited sample:

- no major systemic breakdown was identified
- configuration-management practices require corrective action
- awareness governance would benefit from stronger auditable evidence
- additional controls remain untested and should not be inferred to conform

The organization should implement the corrective action plan and perform follow-up verification before formally closing the identified nonconformity.

## Risk and Governance Implications

The configuration-management finding may increase the risk associated with weak or long-lived local credentials where local password authentication remains relevant.

The awareness observation relates primarily to assurance maturity: a process may exist operationally, but insufficient retained evidence can weaken the organization's ability to demonstrate effective implementation.

Management should ensure that corrective actions are proportionate to:

- business risk
- control applicability
- authentication architecture
- regulatory obligations
- organizational risk appetite

## Follow-Up Requirements

The audit team recommends:

- corrective-action owner assignment
- target-date tracking
- evidence submission
- verification of implementation
- validation of control effectiveness
- formal closure approval

Open actions should remain visible in the ISMS corrective-action process until closure evidence has been reviewed.

## Audit Limitations

This audit was performed in a simulated local environment.

Limitations include:

- selected control sampling rather than complete Annex A assessment
- no access to production cloud systems
- no access to live HR records
- no independent policy repository
- no historical internal-audit records
- no management-review records
- no supplier evidence
- no production identity-provider evidence

The audit conclusion therefore applies only to the defined simulated scope and sampled evidence.

## Auditor Statement

Audit findings are based on the evidence available during the assessment and should not be interpreted as certification, legal advice, or a complete ISO/IEC 27001 conformity determination.

The purpose of the internal audit is to support management oversight, corrective action, and continual improvement of the ISMS.
"""

    REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT.write_text(
        report,
        encoding="utf-8",
    )

    cap.to_csv(
        ROOT
        / "reports"
        / "corrective_action_plan.csv",
        index=False,
    )

    print(
        f"PASS | Generated {REPORT}"
    )

    print(
        "PASS | Generated reports/corrective_action_plan.csv"
    )


if __name__ == "__main__":
    main()
