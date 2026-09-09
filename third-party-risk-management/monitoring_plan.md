# Third-Party Risk Monitoring Plan

## Purpose

This monitoring plan defines the reassessment cadence and Key Risk Indicators (KRIs) used to oversee third-party vendors after initial due diligence. Monitoring intensity increases with vendor risk so that higher-risk suppliers receive more frequent review and stronger evidence requirements.

## Monitoring Model

| Tier | Reassessment Cadence | Oversight Level |
|---|---|---|
| Critical | Quarterly | Continuous attention to major findings, incidents, and contractual risk |
| High | Semi-annual | Frequent control and evidence review |
| Medium | Annual | Standard yearly reassessment |
| Low | Biennial | Lightweight periodic validation |

## Critical Tier

### Reassessment Cadence
Quarterly

### KRIs

1. **Open Critical Security Findings**
   - Definition: Number of unresolved critical-severity security findings associated with the vendor.
   - Threshold: Greater than 0 requires escalation.
   - Data Source: Vendor remediation reports, penetration test reports, and the exception register.

2. **Security Incident Count**
   - Definition: Number of confirmed security incidents involving the vendor during the monitoring period.
   - Threshold: Any material incident triggers immediate review.
   - Data Source: Vendor incident notifications, internal security operations records, and incident response reports.

3. **Security Notification SLA Breaches**
   - Definition: Number of incidents where the vendor failed to notify the organization within the contractually required timeframe.
   - Threshold: Greater than 0 requires risk-owner review.
   - Data Source: Contract SLA records and incident notification timestamps.

4. **Expired Critical Risk Exceptions**
   - Definition: Number of critical-risk exceptions that remain unresolved after their approved expiry date.
   - Threshold: Greater than 0 requires escalation.
   - Data Source: TPRM exception register.

## High Tier

### Reassessment Cadence
Semi-annual

### KRIs

1. **Days Since Last Penetration Test**
   - Definition: Number of days since the vendor's most recent independent penetration test.
   - Threshold: More than 365 days triggers evidence request.
   - Data Source: Vendor penetration test report.

2. **Unresolved High-Risk Findings**
   - Definition: Number of high-risk security findings that remain open beyond the agreed remediation deadline.
   - Threshold: Greater than 0 requires follow-up.
   - Data Source: Vendor remediation tracker and exception register.

3. **Contract Renewal Risk Flags**
   - Definition: Number of unresolved security or compliance issues approaching contract renewal.
   - Threshold: Any unresolved material issue requires review before renewal.
   - Data Source: Contract management records and TPRM exception register.

## Medium Tier

### Reassessment Cadence
Annual

### KRIs

1. **Security Certification Expiry**
   - Definition: Remaining days until a relevant security certification expires.
   - Threshold: Less than 90 days triggers evidence renewal request.
   - Data Source: Vendor ISO 27001 certificate, SOC 2 report, or equivalent assurance documentation.

2. **Overdue Questionnaire Renewal**
   - Definition: Number of days past the required annual reassessment date.
   - Threshold: Any overdue assessment triggers follow-up.
   - Data Source: Vendor assessment register and LimeSurvey response history.

3. **Open Medium-Risk Exceptions**
   - Definition: Number of unresolved medium-risk control gaps.
   - Threshold: Increase in open exceptions between review periods requires investigation.
   - Data Source: TPRM exception register.

## Low Tier

### Reassessment Cadence
Biennial

### KRIs

1. **Self-Attestation Completion Rate**
   - Definition: Percentage of required vendor attestations completed by the due date.
   - Threshold: Below 100% requires follow-up.
   - Data Source: Vendor questionnaire records.

2. **Material Service Change**
   - Definition: Whether the vendor has materially changed its service scope, hosting model, data handling, or subcontractor relationships.
   - Threshold: Any material change triggers reassessment.
   - Data Source: Vendor change notifications and contract management records.

3. **Expired Assurance Evidence**
   - Definition: Number of required security documents that are no longer current.
   - Threshold: Greater than 0 requires evidence refresh.
   - Data Source: Vendor document repository and assessment records.

## Escalation Rules

A vendor may be reassessed before its normal cadence when any of the following occurs:

- Material security incident
- Significant breach of contractual security obligations
- Critical or repeated high-risk findings
- Major change in service architecture or data processing
- Introduction of new critical subcontractors
- Expiry of a major risk exception without remediation
- Acquisition, merger, or significant financial instability affecting service delivery

## Monitoring Data Sources

The monitoring process uses evidence from:

- Vendor due diligence questionnaires
- SOC 2 reports
- ISO 27001 certificates
- Penetration test reports
- Incident notifications
- Contract and SLA records
- Risk exception register
- Vendor remediation plans
- Internal security operations records
- Vendor change notifications

## Risk Governance Principle

Monitoring frequency is risk-based. Critical and High vendors require stronger evidence and more frequent review because failure of these vendors may create greater operational, security, compliance, or data exposure.
