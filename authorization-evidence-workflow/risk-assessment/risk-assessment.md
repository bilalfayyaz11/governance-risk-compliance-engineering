# Risk Assessment

## System

Customer Records Processing Platform

## Purpose

This assessment evaluates threats, likelihood, impact, control effectiveness, and residual risk relevant to the authorization decision.

## Risk Method

Risk is evaluated using qualitative likelihood and impact ratings.

### Likelihood Scale

| Rating | Definition |
|---|---|
| Low | Unlikely to occur given current conditions and protections |
| Moderate | Credible threat path exists and occurrence is plausible |
| High | Threat activity or weakness makes exploitation likely |

### Impact Scale

| Rating | Definition |
|---|---|
| Low | Limited operational or information impact |
| Moderate | Significant operational, confidentiality, integrity, or recovery impact |
| High | Severe business, mission, legal, or security consequences |

## Risk Matrix

| Likelihood | Low Impact | Moderate Impact | High Impact |
|---|---|---|---|
| Low | Low | Low | Moderate |
| Moderate | Low | Moderate | High |
| High | Moderate | High | High |

## Threat Analysis

### T-001 — Exploitation of Vulnerable Software

Threat Source:

External attacker or malicious actor exploiting a known software vulnerability.

Related Weakness:

Outstanding OpenSSL security remediation.

Likelihood:

Moderate

Impact:

High

Inherent Risk:

High

Existing Protections:

- network access controls
- encrypted communications
- limited administrative access
- security logging
- change-management process

Residual Risk:

High until the identified software remediation is completed.

### T-002 — Credential Compromise

Threat Source:

External attacker using weak, reused, or compromised credentials.

Related Weakness:

Password policy enforcement gap.

Likelihood:

Moderate

Impact:

Moderate

Inherent Risk:

Moderate

Existing Protections:

- authenticated access
- unique user accounts
- restricted administrative privileges
- activity logging

Residual Risk:

Moderate pending authentication-control hardening.

### T-003 — Delayed Detection of Suspicious Activity

Threat Source:

External or internal malicious activity that is logged but not reviewed promptly.

Related Weakness:

Incomplete recurring audit-review evidence.

Likelihood:

Low

Impact:

Moderate

Inherent Risk:

Low

Existing Protections:

- centralized audit logging
- retained security records
- administrative access restrictions

Residual Risk:

Low.

This risk is considered acceptable for the current authorization period provided the condition is reviewed during the next annual risk review or sooner if the threat environment changes.

### T-004 — Failed Recovery During Service Disruption

Threat Source:

Operational failure, destructive incident, system corruption, or administrative error.

Related Weakness:

Backup restoration testing evidence incomplete.

Likelihood:

Low

Impact:

High

Inherent Risk:

Moderate

Existing Protections:

- scheduled backups
- protected backup storage
- operational recovery procedures

Residual Risk:

Moderate until successful restoration testing is formally evidenced.

## Residual Risk Summary

| Risk | Residual Rating | Disposition |
|---|---|---|
| Vulnerable software exploitation | High | Remediate |
| Credential compromise | Moderate | Remediate |
| Delayed security-event detection | Low | Risk Accepted |
| Recovery failure | Moderate | Remediate |

## Overall Risk Determination

Overall residual risk is assessed as Moderate-to-High.

The principal driver is the outstanding High-risk software remediation item.

The system may be considered for conditional authorization if the Authorizing Official determines that:

- current compensating protections are sufficient for temporary operation
- the High-risk weakness has an accountable owner
- remediation occurs within the approved target period
- Medium-risk weaknesses remain actively tracked
- the accepted Low risk is formally documented and periodically reviewed

## Recommended Authorization Posture

Authorize with Conditions

The recommendation is based on the existence of a functioning security-control baseline combined with clearly identified, owned, and time-bound remediation requirements.
