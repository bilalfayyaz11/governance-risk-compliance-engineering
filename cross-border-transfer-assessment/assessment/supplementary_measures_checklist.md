# Supplementary Measures Checklist

## Scope

This checklist evaluates supplementary technical, contractual, and organizational measures for the Frankfurt-to-Riyadh onward transfer.

The assessment follows the logic of EDPB Recommendations 01/2020: identify the transfer, identify the transfer tool, assess destination-country law and practice, identify effective supplementary measures where necessary, complete procedural steps, and periodically reassess.

| Measure Category | Applied? | Residual Risk | Justification |
|---|---|---|---|
| Encryption in transit (TLS 1.3) | Yes | Medium | Protects confidentiality against network interception, but data must normally be decrypted by the recipient for payroll support processing. It therefore does not eliminate lawful or compelled access risk at the destination. |
| Encryption at rest (customer-managed keys) | Yes | Medium | Strong protection for stored data when keys are segregated. Risk remains if the importer or its administrators can obtain decryption capability during processing. |
| Client-side / field-level encryption | Partial | Low-Medium | Highly effective for fields the Riyadh support function does not need in plaintext. Effectiveness falls where the importer must possess the decryption capability to perform its task. |
| Pseudonymization before transfer | Yes | Low | Emirates ID and direct identifiers can be replaced with controlled tokens where full identity is unnecessary. Residual risk remains if data can be reidentified using information available to the importer. |
| Reidentification mapping retained separately | Yes | Low | Token mapping remains under exporter/controller control and is not routinely available to the Riyadh importer. This materially limits reidentification capability. |
| Data minimization | Yes | Low | Only fields required for the specific support case should be transferred. Health accommodation and performance review data are excluded from routine Riyadh processing. |
| Access logging & monitoring | Yes | Medium | Improves accountability, detection, and investigation. It does not technically prevent authorized or compelled access by itself. |
| Least-privilege RBAC | Yes | Low-Medium | Limits routine employee access and reduces insider risk. Privileged administrator access remains a residual concern. |
| MFA for privileged access | Yes | Low | Reduces account-compromise risk but does not address lawful government-access powers. |
| Customer-controlled cryptographic keys | Partial | Medium | Effective where keys remain outside the importer environment. Operational payroll support may require selected fields in plaintext, leaving some residual exposure. |
| Split-key / dual-control design | Feasible | Low-Medium | Can prevent a single administrator or organization from independently decrypting protected data, but increases operational complexity and may not work for fields requiring real-time support access. |
| Government access assessment (Saudi Arabia) | Yes | Medium-High | Destination-law and practice must be evaluated against the essential-equivalence standard. Contractual promises alone cannot neutralize binding legal authority. Technical measures therefore remain important. |
| Government request challenge commitment | Yes | Medium | Improves procedural safeguards where challenges are legally available, but cannot guarantee prevention of access under mandatory local law. |
| Transparency reporting | Yes | Medium | Provides governance visibility into requests where disclosure is legally permitted but is not a preventative technical control. |
| Contractual audit clauses | Yes | Medium | Supports verification and accountability but cannot override destination-country law. |
| Onward transfer restrictions | Yes | Low-Medium | Contractually prevents uncontrolled onward disclosure, subject to enforceability and mandatory legal obligations. |
| Sub-processor approval controls | Yes | Low | Requires authorization and reassessment before additional recipients are introduced. |
| Short retention period | Yes | Low | Reduces the duration during which data remains exposed to compromise, misuse, or compelled access. |
| Secure deletion verification | Yes | Low | Reduces post-processing exposure when deletion can be verified. Backup lifecycle constraints remain a residual factor. |
| Incident notification obligation | Yes | Low-Medium | Enables rapid response but does not prevent the initial incident. |
| Periodic TIA reassessment | Yes | Low-Medium | Helps identify legal, operational, or technical changes over time. Protection depends on timely and substantive reassessment. |

## Overall Assessment

### Strongest Measures

The strongest measures are:

1. Pseudonymization before transfer
2. Separate control of reidentification information
3. Data minimization
4. Client-side or field-level encryption where the importer does not require plaintext
5. Strong limitations on onward transfers

These controls reduce the quantity and intelligibility of personal data available in the destination environment.

## Key Limitation

Transport encryption alone does not solve destination-country access risk because TLS protects data during transmission but not after the recipient receives and decrypts it.

Similarly, contractual measures cannot override binding national law.

## Residual Risk

**Overall residual risk: Medium**

The risk is materially reduced where:

- Direct identifiers are pseudonymized
- Special-category information is excluded
- Decryption keys remain outside the importer environment
- Only minimum payroll support information is transferred
- Strong access controls and monitoring are enforced

Risk rises toward **Medium-High** if the Riyadh importer receives full identifiers, special-category data, or unrestricted decryption capability.

## Required Conditions Before Transfer

The onward transfer should proceed only if:

- Special-category health information is excluded unless strictly necessary.
- Emirates ID is pseudonymized where operationally feasible.
- Reidentification mapping remains under exporter/controller control.
- Data fields are minimized to the support purpose.
- Key-management responsibilities are documented.
- Government-access handling obligations are contractually defined.
- Additional onward transfers require approval.
- Security logging and privileged-access monitoring remain active.
- The TIA is periodically reassessed.
