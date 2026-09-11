# IDVerify Privacy Remediation Backlog

## Executive Summary

IDVerify currently presents a **High privacy risk posture** because the identity-verification pipeline handles highly identifying document data, biometric face-matching inputs, persistent verification records, and an external OCR/face-match dependency across trust boundaries.

The three most systemic issues are:

1. **Third-party biometric processing** — full identity documents and selfies may leave the primary trust boundary, creating linkability, disclosure, processor-governance, cross-border, and special-category-data risk.
2. **Excessive identity correlation and retention** — persistent identifiers, centralized extracted PII, audit history, and verification metadata can enable unnecessary linking and long-term profiling.
3. **Privacy controls are not consistently enforced by architecture** — retention, minimization, unlinkability, transparency, and audit minimization need technical controls rather than policy-only assurances.

The recommended remediation strategy prioritizes reducing data before trust-boundary crossings, limiting persistent identifiers, constraining third-party processing, and enforcing privacy defaults through architecture and automated controls.

---

## Severity Method

This backlog uses:

**Risk Score = Impact × Likelihood**

Each dimension is scored from 1 to 5.

### Impact

| Score | Meaning |
|---|---|
| 1 | Negligible privacy impact |
| 2 | Limited individual impact |
| 3 | Material privacy impact |
| 4 | Serious privacy or regulatory impact |
| 5 | Severe impact involving identity, biometric, financial, or systemic exposure |

### Likelihood

| Score | Meaning |
|---|---|
| 1 | Unlikely |
| 2 | Possible but uncommon |
| 3 | Plausible |
| 4 | Likely under realistic misuse/failure |
| 5 | Expected or inherent in current architecture |

### Severity Bands

| Score | Severity |
|---|---|
| 20–25 | Critical |
| 12–19 | High |
| 6–11 | Med |
| 1–5 | Low |

---

## Prioritized Backlog

| ID | LINDDUN Category | Severity | Score | GDPR/PDPL Ref | Mitigation Summary | Owner (role) | Target Sprint |
|---|---|---:|---:|---|---|---|---|
| DSC-02 | Data Disclosure | Critical | 25 | GDPR Arts. 5, 9, 25, 32, 35; UAE PDPL 5,20,22-23; KSA PDPL 11,13,19,29 | Minimize document regions before external OCR; prefer confidential-computing/secure-enclave processing; prohibit unrelated third-party retention/use. | Privacy Architect + ML Platform Lead | Sprint 1 |
| IDN-01 | Identifying | Critical | 25 | GDPR Arts. 5,9,25,32,35; UAE PDPL 5,20,22-23; KSA PDPL 11,13,19,29 | Move face matching on-device or into a controlled enclave and return only derived match results where feasible. | Mobile Engineering Lead + Security Architect | Sprint 1 |
| NCM-01 | Non-compliance | Critical | 20 | GDPR Arts. 5,9,25,28,32,35; UAE PDPL 5,20,22-23; KSA PDPL 11,13,19,29 | Enforce third-party deletion SLA, disable model training on customer data, require deletion attestations, and define onward-processing restrictions. | Vendor Risk + Privacy Counsel | Sprint 1 |
| LNK-02 | Linking | High | 20 | GDPR Arts. 5,9,25,35; UAE PDPL 5,22-23; KSA PDPL 11,13,29 | Replace persistent provider-facing identifiers with per-request pseudonymous tokens and prevent cross-customer biometric correlation. | Privacy Engineering + ML Integration | Sprint 1 |
| DSC-03 | Data Disclosure | High | 16 | GDPR Arts. 5,25,32; UAE PDPL 5,20; KSA PDPL 11,19 | Tokenize document identifiers, encrypt high-risk columns, and enforce automated field-level retention. | Data Platform Lead | Sprint 2 |
| LNK-03 | Linking | High | 16 | GDPR Arts. 5,25; UAE PDPL 5; KSA PDPL 11 | Separate identity attributes from verification-event history using tokenized subject keys and schema segmentation. | Data Architect | Sprint 2 |
| NCM-02 | Non-compliance | High | 16 | GDPR Arts. 5,25,32,35; UAE PDPL 5,20; KSA PDPL 11,19 | Implement privacy-policy-as-code for retention, access review, deletion, and purpose-bound fields with CI checks. | Platform Engineering + Privacy Engineering | Sprint 2 |
| DSC-01 | Data Disclosure | High | 16 | GDPR Arts. 5,9,25,32,35; UAE PDPL 5,20; KSA PDPL 11,19 | Redact/crop identity documents client-side and avoid raw-image persistence in gateway infrastructure. | Mobile Engineering Lead | Sprint 2 |
| IDN-02 | Identifying | High | 15 | GDPR Arts. 5,25,32; UAE PDPL 5,20; KSA PDPL 11,19 | Tokenize direct identifiers before storage and isolate token mapping in a separately controlled service. | Backend Lead + Security Engineering | Sprint 2 |
| DSC-04 | Data Disclosure | High | 15 | GDPR Arts. 5,25,32; UAE PDPL 5,20; KSA PDPL 11,19 | Remove raw identifiers/match scores from logs; tokenize subject references; apply differential privacy to aggregate analytics. | Observability Lead | Sprint 2 |
| UNA-01 | Unawareness/Unintervenability | High | 15 | GDPR Arts. 5,9,25,35; UAE PDPL 5-6,22-23; KSA PDPL 12-13,29 | Add just-in-time notice before capture explaining third-party biometric processing, destination, retention, and rights. | Product + Privacy Counsel | Sprint 2 |
| DET-01 | Detecting | High | 12 | GDPR Arts. 5,25,32; UAE PDPL 5,20; KSA PDPL 11,19 | Normalize timing, status codes, response sizes, and error messages; add rate limiting and request shaping. | API Platform Lead | Sprint 3 |
| NRP-01 | Non-repudiation | Med | 10 | GDPR Arts. 5,25; UAE PDPL 5; KSA PDPL 11-13 | Replace raw identity data in logs with pseudonymous references and cryptographically integrity-chain audit events. | Security Engineering | Sprint 3 |
| NRP-02 | Non-repudiation | Med | 9 | GDPR Arts. 5,25; UAE PDPL 5; KSA PDPL 11 | Use role-scoped or rotating reviewer pseudonyms with restricted re-identification capability. | Compliance Systems Lead | Sprint 3 |
| UNA-02 | Unawareness/Unintervenability | Med | 9 | GDPR Arts. 5,25,35; UAE PDPL 5; KSA PDPL 12-13 | Add explainable review notice plus correction/appeal workflow for automated or human-assisted decisions. | Product + Compliance Operations | Sprint 3 |
| DET-02 | Detecting | Med | 8 | GDPR Arts. 5,25,32; UAE PDPL 5,20; KSA PDPL 11,19 | Return coarse-grained onboarding status instead of exposing exact biometric/fraud/manual-review causes. | Backend Engineering | Sprint 3 |
| LNK-01 | Linking | Med | 8 | GDPR Arts. 5,25; UAE PDPL 5; KSA PDPL 11 | Use unlinkable per-verification session identifiers with short TTLs instead of persistent device/account context. | API Platform Lead | Sprint 3 |

---

## Immediate Priorities

The first implementation wave should focus on:

1. Reducing third-party biometric exposure.
2. Moving face matching closer to the data source or into a controlled enclave.
3. Preventing third-party retention and secondary use.
4. Replacing persistent cross-system identifiers with unlinkable or tokenized identifiers.
5. Enforcing retention and minimization technically rather than through documentation alone.

---

## Architectural Recommendation

Preferred direction:

~~text
Mobile Client
     |
     | client-side crop/redaction
     | on-device preprocessing
     v
API Gateway
     |
     | unlinkable session token
     v
IDVerify Service
     |
     +----> Token Vault
     |
     +----> Minimal PII -> PostgreSQL
     |
     +----> Privacy-minimized Audit Events
     |
     +----> Minimal Required Input
              |
              v
       Confidential OCR /
       Face-Match Processing
              |
              v
        Derived Result Only
~~

The system should avoid transmitting raw identity or biometric data where a transformed, minimized, or derived representation is sufficient.

---

## Definition of Done for High-Risk Items

Critical and High issues should not be considered resolved until:

- The mitigation exists in production code or infrastructure.
- Relevant data flows have been re-modeled.
- Threat register residual risk has been reassessed.
- Logging confirms the control operates as designed.
- Privacy/security tests are automated where feasible.
- Processor and transfer obligations match the technical design.
- Data-retention behavior has been tested.
- Product notices reflect the actual processing.
- Evidence is retained for privacy review.

---

## Residual Risk Position

After implementation of Critical and High items, the expected residual posture is:

**Medium**

The principal remaining risks would be:

- Necessary identity processing itself
- Mandatory retention
- Limited third-party dependency
- Insider privilege
- Public-authority access where applicable
- False matches and human review errors

These risks require continuous governance rather than one-time remediation.

