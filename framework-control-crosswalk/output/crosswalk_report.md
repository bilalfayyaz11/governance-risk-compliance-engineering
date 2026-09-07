# Security Control Framework Crosswalk Report

## Executive Summary

This report presents a normalized security-control crosswalk across ISO/IEC 27001 Annex A, NIST Cybersecurity Framework 2.0, and the SAMA Cyber Security Framework. It identifies aligned control themes, framework coverage gaps, and the evidence expected to support assessment activities.

**Generated:** 2026-09-07 13:06 UTC

## Crosswalk Metrics

| Metric | Result |
|---|---:|
| Total control themes assessed | 8 |
| Equivalent mappings | 6 |
| Framework coverage gaps | 2 |
| Equivalent coverage | 75.0% |
| Gap rate | 25.0% |
| Evidence requirements defined | 8 |
| Missing evidence definitions | 0 |

## Framework Coverage

| Framework | Themes with mapped control |
|---|---:|
| ISO/IEC 27001 | 7/8 |
| NIST CSF 2.0 | 8/8 |
| SAMA CSF | 6/8 |

## Coverage Gap Analysis

| Theme | ISO 27001 | NIST CSF 2.0 | SAMA CSF | Rationale |
|---|---|---|---|---|
| Configuration Management | A.8.9 | PR.PS-01 | — | ISO and NIST have explicit configuration-management references in this catalog extract, while no directly mapped SAMA control was selected. |
| Recovery Planning | — | RC.RP-01 | — | A recovery-specific NIST outcome is present in the sample catalog, but equivalent ISO and SAMA controls were not included in this simplified extract. |

## Evidence Requirements

| Control Theme | Mapping Status | Validation | Required Evidence |
|---|---|---|---|
| Policy | Equivalent | PASS | Approved cybersecurity policy with owner approval and documented review date |
| Vulnerability Management | Equivalent | PASS | Vulnerability scan reports remediation tickets and remediation tracking records |
| Monitoring | Equivalent | PASS | SIEM logs monitoring dashboards alert records and monitoring procedures |
| Incident Management | Equivalent | PASS | Incident response plan incident tickets investigation records and post-incident reports |
| Identity and Access Management | Equivalent | PASS | Access review records user provisioning records role assignments and approval evidence |
| Configuration Management | Gap | PASS | Approved configuration baseline change records and configuration review evidence |
| Logging | Equivalent | PASS | Audit logs log-retention configuration and centralized logging evidence |
| Recovery Planning | Gap | PASS | Recovery plan backup records recovery test results and restoration evidence |

## Full Framework Crosswalk

| Control Theme | Status | ISO 27001 | NIST CSF 2.0 | SAMA CSF |
|---|---|---|---|---|
| Policy | Equivalent | A.5.1 — Policies for information security | GV.PO-01 — Cybersecurity risk management policy is established communicated and enforced | 3.1.3 — Cyber Security Policy |
| Vulnerability Management | Equivalent | A.8.8 — Management of technical vulnerabilities | ID.RA-01 — Vulnerabilities in assets are identified validated and recorded | 3.3.17 — Vulnerability Management |
| Monitoring | Equivalent | A.8.16 — Monitoring activities | DE.CM-01 — Networks and network services are monitored | 3.3.14 — Cyber Security Event Management |
| Incident Management | Equivalent | A.5.24 — Information security incident management planning and preparation | RS.MA-01 — The incident response plan is executed in coordination with relevant parties | 3.3.15 — Cyber Security Incident Management |
| Identity and Access Management | Equivalent | A.5.15 — Access control | PR.AA-01 — Identities and credentials are managed for authorized users services and hardware | 3.3.5 — Identity and Access Management |
| Configuration Management | Gap | A.8.9 — Configuration management | PR.PS-01 — Configuration management practices are established and applied | — |
| Logging | Equivalent | A.8.15 — Logging | DE.CM-01 — Networks and network services are monitored | 3.3.14 — Cyber Security Event Management |
| Recovery Planning | Gap | — | RC.RP-01 — The recovery portion of the incident response plan is executed | — |

## Assessment Notes

- Equivalent mappings represent thematic alignment within the simplified control scope and should not be interpreted as proof that the frameworks are legally or technically interchangeable.
- Gap status identifies where the sampled catalog does not contain a mapped control; it does not necessarily prove that the complete source framework lacks a related requirement.
- Evidence requirements define expected assessment artifacts but do not establish that those artifacts have actually been collected or validated.
- Production compliance assessments should validate mappings against the complete authoritative framework publications and organizational implementation context.
