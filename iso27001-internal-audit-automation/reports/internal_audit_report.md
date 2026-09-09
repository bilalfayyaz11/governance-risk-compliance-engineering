# Internal ISMS Audit Report

## Executive Summary

An internal audit of selected Information Security Management System controls was conducted for Meridian FinTech Services Ltd. against ISO/IEC 27001:2022 requirements and a selected Annex A control sample.

The audit identified 1 nonconformity and 1 improvement observation across 2 controls for which audit activity was performed. The sampled evidence indicates that elements of the ISMS are implemented, but corrective action is required for the identified configuration-management weakness and additional evidence maturity is recommended for awareness assurance.

No major nonconformity was identified in the simulated audit sample.

## Audit Information

**Organization:** Meridian FinTech Services Ltd.

**Audit Type:** Internal ISMS Audit

**Audit Standard:** ISO/IEC 27001:2022

**Report Date:** 2026-09-09

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

    15

Controls with audit activity:

    2

Status distribution:

    {'Not Tested': 13, 'Partially Tested': 1, 'Nonconformity': 1}

## Checklist Results

| Control_ID   | Control_Name                                                      | Category       | Status           | Evidence_Ref                               |
|:-------------|:------------------------------------------------------------------|:---------------|:-----------------|:-------------------------------------------|
| A.5.1        | Policies for information security                                 | Organizational | Not Tested       |                                            |
| A.5.7        | Threat intelligence                                               | Organizational | Not Tested       |                                            |
| A.5.15       | Access control                                                    | Organizational | Not Tested       |                                            |
| A.5.18       | Access rights                                                     | Organizational | Not Tested       |                                            |
| A.5.23       | Information security for use of cloud services                    | Organizational | Not Tested       |                                            |
| A.5.24       | Information security incident management planning and preparation | Organizational | Not Tested       |                                            |
| A.5.30       | ICT readiness for business continuity                             | Organizational | Not Tested       |                                            |
| A.6.3        | Information security awareness education and training             | People         | Partially Tested | evidence/interview_02.md                   |
| A.6.5        | Responsibilities after termination or change of employment        | People         | Not Tested       |                                            |
| A.7.4        | Physical security monitoring                                      | Physical       | Not Tested       |                                            |
| A.8.2        | Privileged access rights                                          | Technological  | Not Tested       |                                            |
| A.8.5        | Secure authentication                                             | Technological  | Not Tested       |                                            |
| A.8.9        | Configuration management                                          | Technological  | Nonconformity    | evidence/A8_9_password_policy_evidence.txt |
| A.8.16       | Monitoring activities                                             | Technological  | Not Tested       |                                            |
| A.8.23       | Web filtering                                                     | Technological  | Not Tested       |                                            |

## Findings Summary

Severity distribution:

    {'Minor': 1, 'Observation': 1}

| Finding_ID   | Control_ID   | Description                                                                                                                                                                        | Severity    | Evidence_Ref                                  | Recommendation                                                                                                                                                              |
|:-------------|:-------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------|:----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| F001         | A.8.9        | Password maximum age exceeds the organizational policy limit of 90 days.                                                                                                           | Minor       | ../evidence/A8_9_password_policy_evidence.txt | Review applicable local accounts and update the approved password-aging configuration so PASS_MAX_DAYS does not exceed 90 days where local password authentication is used. |
| F002         | A.6.3        | Awareness activities are described and tracked through HR processes, but independent sample evidence of annual refresher completion was not available during this simulated audit. | Observation | evidence/interview_02.md                      | Introduce periodic evidence sampling and an auditable completion dashboard for information security awareness activities.                                                   |

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

| Finding_ID   | Severity    | Corrective Action                                                                                                                                                    | Owner                     | Target Date   | Status   |
|:-------------|:------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------|:--------------|:---------|
| F001         | Minor       | Review applicable local accounts, update the approved Linux password-aging baseline, and remediate PASS_MAX_DAYS where local password authentication remains in use. | Cloud Infrastructure Lead | 2026-09-30    | Open     |
| F002         | Observation | Establish periodic sampling of security-awareness completion records and maintain auditable evidence of refresher completion and overdue follow-up.                  | HR Manager                | 2026-10-15    | Open     |

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
