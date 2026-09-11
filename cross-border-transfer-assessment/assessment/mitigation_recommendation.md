# Technical Mitigation Recommendation

## Executive Decision

**Recommended architecture: Option A — Data Localization + Data Minimization**

Use localization and selective onward transfer as the primary risk-reduction strategy.

Client-side / field-level encryption remains a supporting control for selected fields, but it should not be relied upon as the sole mitigation where the Riyadh Sub-processor requires plaintext access to perform payroll support.

---

## Options Evaluated

### Option A — Data Localization

Keep higher-risk HR fields in the UAE and/or Frankfurt-controlled environment.

Transfer to Riyadh only the minimum information necessary for payroll support.

Routine Riyadh access should exclude:

- Health accommodation information
- Performance reviews
- Full HR case history
- Unnecessary direct identifiers
- Any field not required for the support activity

Where possible, replace direct identifiers with pseudonymous employee references.

Example:

~~text
UAE / Frankfurt HR Record
        |
        | Remove unnecessary HR fields
        | Exclude Article 9 health data
        | Tokenize direct identifiers
        v
Minimal Payroll Support Record
        |
        v
Riyadh Support Environment
~~

### Option B — Client-Side / Field-Level Encryption

Encrypt selected fields before they leave the controlled environment.

Potential protected fields include:

- Emirates ID
- Bank IBAN
- Other direct identifiers

Keys would remain controlled by the UAE Controller or Frankfurt Processor where operationally possible.

Example:

~~text
Sensitive Field
      |
      v
Client-Side Encryption
      |
      +----> Key retained outside Riyadh
      |
      v
Ciphertext
      |
      v
Riyadh Environment
~~

---

## Trade-Off Comparison

| Dimension | Option A — Localization / Minimization | Option B — Client-Side Encryption |
|---|---|---|
| Residual privacy risk | Low-Medium | Medium where plaintext is required |
| Government-access exposure | Reduced because less intelligible data exists in destination | Strong only where importer lacks decryption capability |
| Article 9 exposure | Can be eliminated from routine transfer | Remains relevant if data must be decrypted in Riyadh |
| Direct identifier exposure | Can be replaced with tokens | Can be encrypted |
| Operational complexity | Medium | High |
| Application changes | Medium | High |
| Key-management overhead | Low-Medium | High |
| Support-team usability | High if support workflow is redesigned around minimal data | Can be reduced if important fields remain encrypted |
| Latency impact | Low | Low-Medium depending on cryptographic workflow |
| Compliance operating cost | Medium | Medium-High to High |
| Auditability | High | High if key operations are logged |
| Data minimization benefit | High | Low by itself |
| Breach impact reduction | High | High for inaccessible ciphertext |
| Resilience to key compromise | Not primarily key-dependent | Dependent on key separation and access controls |
| Long-term maintainability | High | Medium |
| Fit for payroll support | Strong | Conditional |
| Overall recommendation | **Preferred** | Supporting measure |

---

## Latency Analysis

### Option A

Localization and minimization introduce little additional runtime latency.

The primary impact occurs during workflow preparation:

1. Select approved fields.
2. Remove unnecessary attributes.
3. Tokenize identifiers.
4. Transfer the minimized record.

Expected operational effect:

**Low latency impact**

The architecture may add a small transformation step before transfer, but the Riyadh support environment can work normally with the approved fields it receives.

### Option B

Client-side or field-level encryption introduces:

- Encryption processing
- Key lookup
- Decryption authorization
- Key-management network calls
- Potential application logic changes

For normal payroll volumes, raw cryptographic processing overhead is likely small compared with network and application latency.

However, workflow latency may increase materially if support personnel require controlled decryption approvals.

Expected operational effect:

**Low-Medium latency impact**

---

## Compliance Cost Analysis

### Option A

Primary costs include:

- Field mapping
- Data-flow redesign
- Pseudonymization/tokenization
- Access-policy changes
- Transfer validation
- Updated processor instructions

Expected compliance cost:

**Medium**

Once implemented, the architecture is comparatively simple to operate because sensitive information is not routinely sent to the destination environment.

### Option B

Primary costs include:

- Client-side encryption implementation
- Key-management infrastructure
- Key rotation
- Access-policy engineering
- Cryptographic audit logging
- Recovery procedures
- Separation-of-duty controls
- Application integration
- Key compromise response

Expected compliance cost:

**Medium-High to High**

The design becomes substantially more complex if the importer requires access to some protected fields but not others.

---

## Residual Risk Reduction

### Option A

Starting risk:

**High**

After:

- Removing health accommodation data
- Removing performance reviews
- Minimizing payroll fields
- Tokenizing direct identifiers
- Restricting onward transfer

Expected residual risk:

**Low-Medium**

The main advantage is architectural:

Data that is never transferred cannot be accessed, exposed, compelled, or breached in the destination environment.

### Option B

Starting risk:

**High**

If encryption keys remain exclusively outside Saudi Arabia and the importer never needs plaintext:

Expected residual risk:

**Low**

However, if Riyadh personnel require plaintext for operational support and can obtain decryption capability:

Expected residual risk:

**Medium**

The effectiveness of encryption therefore depends heavily on whether the importer genuinely needs access to plaintext.

---

## Recommended Architecture

Use a hybrid architecture led by **Option A**.

~~text
                    UAE HR System
                         |
                         v
                Full Employee Record
                         |
               Data Minimization
                         |
          +--------------+---------------+
          |                              |
          v                              v
Restricted HR Data                Payroll Support Data
Remain UAE / Frankfurt                   |
                                         |
                               Pseudonymization
                                         |
                               Field Encryption
                               where feasible
                                         |
                                         v
                              Riyadh Sub-processor
~~

### Keep Outside Routine Riyadh Access

- Health accommodation data
- Performance reviews
- Unnecessary HR narrative
- Reidentification mappings
- Cryptographic master keys
- Fields unrelated to payroll support

### Permit Only Where Necessary

- Pseudonymous employee reference
- Work email where operationally necessary
- Payroll amount
- Limited payroll exception information
- Masked or protected bank information where possible

---

## Why Option A Is Preferred

Option A provides stronger structural risk reduction.

The most effective way to reduce cross-border transfer risk is to avoid transferring data that the recipient does not need.

This approach directly supports:

- Data minimization
- Purpose limitation
- Lower breach impact
- Reduced public-authority-access exposure
- Lower insider risk
- Smaller audit scope
- Simpler key-management requirements

By contrast, encryption is strongest only when the recipient cannot decrypt the data.

If the operational model requires Riyadh personnel to decrypt the same information they receive, encryption mainly protects:

- Network transit
- Storage media
- Certain unauthorized technical access

It does not eliminate exposure to authorized recipient access or legally compelled recipient disclosure.

---

## Final Recommendation

### Primary Control

**Option A — Data Localization + Data Minimization**

### Supporting Controls

Add:

- Pseudonymization
- TLS 1.3
- Encryption at rest
- Field-level encryption where plaintext is unnecessary
- Customer/exporter-controlled keys
- Least privilege
- MFA
- Access logging
- Privileged activity monitoring
- Strict onward-transfer controls

### Final Residual Risk

**Low-Medium**, provided all required conditions in the TIA are implemented.

If the Riyadh Sub-processor requires unrestricted access to full employee records, health data, or reidentification information, the risk should be reassessed and the transfer may no longer be acceptable.

---

## Decision Summary

| Item | Decision |
|---|---|
| Primary strategy | Data Localization / Minimization |
| Encryption role | Supporting technical measure |
| Special-category data to Riyadh | No, except exceptional documented necessity |
| Reidentification mapping in Riyadh | No |
| Full Emirates ID in Riyadh | Avoid where feasible |
| Minimum-data principle | Mandatory |
| Overall residual risk | Low-Medium |
| Transfer recommendation | Proceed with Conditions |
