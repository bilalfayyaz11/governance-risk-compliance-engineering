# Transfer Impact Assessment

## Assessment Metadata

**Assessment date:** 12 September 2026

**Primary Controller:** Dubai HR Controller

**Primary Processor:** Frankfurt Payroll Processor

**Onward Sub-processor:** Riyadh Payroll Support Services

**Relevant Chapter V transfer:** Frankfurt, Germany → Riyadh, Saudi Arabia

**Selected transfer mechanism:** SCC Module 3 — Processor to Processor

**Overall recommendation:** **Proceed with Conditions**

**Residual risk:** **Medium**

---

# 1. Executive Summary

This Transfer Impact Assessment evaluates the handling of employee HR and payroll information across a three-party processing chain:

~~text
Dubai HR Controller
        |
        v
Frankfurt Payroll Processor
        |
        v
Riyadh Payroll Support Services
~~

The original data originates with a Controller in Dubai and is sent to a Processor in Frankfurt for payroll processing.

Because Frankfurt is located within the EEA, the Dubai-to-Frankfurt leg is not treated as a GDPR Chapter V export merely because the United Arab Emirates does not have an EU adequacy decision.

The relevant GDPR Chapter V transfer occurs when the Frankfurt Processor makes an onward transfer to the Riyadh Sub-processor in Saudi Arabia.

Saudi Arabia does not have an European Commission adequacy decision as of the assessment date.

The selected Article 46 safeguard for the Frankfurt-to-Riyadh transfer is therefore the European Commission Standard Contractual Clauses, Module 3, for Processor-to-Processor transfers.

The data set contains highly sensitive HR information, including Emirates ID numbers, salary information, bank IBANs, performance information, and health accommodation information.

Health accommodation information may reveal health status and therefore represents GDPR Article 9 special-category data.

The strongest risk reduction is achieved not by contractual terms alone but by minimizing the data transferred to Riyadh, pseudonymizing direct identifiers, retaining reidentification mappings outside the Saudi processing environment, excluding health information from routine onward transfers, and applying field-level encryption where the recipient does not require plaintext.

The assessment concludes that the transfer should **proceed only with conditions**.

---

# 2. Transfer Description

## 2.1 Source System

The source environment is a UAE-hosted Human Resources Information System operated by the Dubai HR Controller.

The system contains employee information used for employment administration and payroll.

## 2.2 First Processing Leg

~~text
Dubai HR Controller
        |
        | HR and payroll information
        | TLS 1.3
        v
Frankfurt Payroll Processor
~~

Purpose:

- Payroll calculation
- Payroll reconciliation
- Salary-payment administration
- Statutory payroll reporting
- Payroll correction processing

The destination is Frankfurt, Germany.

Because Germany is within the EEA, this leg is not itself the third-country transfer evaluated under GDPR Chapter V.

## 2.3 Onward Processing Leg

~~text
Frankfurt Payroll Processor
        |
        | Minimum payroll support data
        | TLS 1.3
        v
Riyadh Payroll Support Services
~~

The Riyadh Sub-processor performs regional payroll support and exception handling.

This transfer leaves the EEA and therefore requires a valid GDPR Chapter V transfer mechanism.

## 2.4 Data Flow Diagram

The visual data-flow diagram is maintained at:

`../diagrams/dataflow.png`

The Graphviz source is maintained at:

`../diagrams/dataflow.dot`

## 2.5 Data Subjects

Data subjects include:

- Current employees
- Former employees whose information remains subject to valid payroll retention obligations

## 2.6 Data Categories

The overall source data set contains:

| Data | Classification |
|---|---|
| Full legal name | Confidential |
| Work email | Internal |
| Emirates ID | Confidential |
| Salary | Confidential |
| Bank IBAN | Confidential |
| Performance review | Confidential |
| Health accommodation information | Special Category |

## 2.7 Transfer Frequency

The primary payroll transfer is recurring and normally occurs monthly.

Ad-hoc processing may occur for:

- Payroll corrections
- Support escalations
- Payroll discrepancies
- Authorized exception handling

---

# 3. EDPB Six-Step Transfer Assessment

## Step 1 — Know Your Transfers

The first EDPB step requires the organization to understand and document transfers of personal data.

This assessment identified two material processing legs:

1. Dubai → Frankfurt
2. Frankfurt → Riyadh

Only the second leg constitutes the relevant EEA-to-third-country transfer for this assessment.

The transfer inventory records:

- Exporter and importer
- Processing roles
- Data categories
- Data subjects
- Processing purpose
- Frequency
- Storage locations
- Sub-processors
- Technical transport mechanism

### Step 1 Conclusion

The Frankfurt-to-Riyadh onward transfer is the transfer requiring GDPR Chapter V analysis.

The organization must maintain the transfer inventory and update it when:

- New sub-processors are added
- New data categories are transferred
- Processing purposes change
- Storage locations change
- Transfer routes change

---

## Step 2 — Identify the Transfer Tool

Saudi Arabia does not benefit from an EU adequacy decision in this assessment.

The Frankfurt Processor therefore cannot rely on Article 45 adequacy for the onward transfer.

The processing roles are:

**Exporter:** Processor

**Importer:** Sub-processor / Processor

The selected transfer tool is therefore:

**European Commission Standard Contractual Clauses — Module 3: Processor to Processor**

The SCC documentation is maintained at:

`assessment/scc_module3.md`

### Step 2 Conclusion

The selected Article 46 safeguard is:

**SCC Module 3 + Transfer Impact Assessment + supplementary measures**

The SCCs are not treated as sufficient merely because they have been executed.

Their effectiveness must be assessed against the circumstances of the transfer and the legal environment applicable to the importer.

---

## Step 3 — Assess Third-Country Law and Practice

The third step evaluates whether law or practice applicable in the destination country may interfere with the effectiveness of the selected transfer tool.

The destination for the Chapter V transfer is Saudi Arabia.

The assessment must consider whether public authorities may obtain access to transferred personal data and whether such access could undermine the protections required by EU law and the SCCs.

### 3.1 Assessment Standard

The assessment uses the EDPB essential-equivalence approach.

Relevant questions include whether public-authority access:

- Has a clear and accessible legal basis
- Pursues legitimate objectives
- Is necessary
- Is proportionate
- Is subject to meaningful limits
- Includes independent oversight
- Provides effective remedies to affected individuals

### 3.2 Destination-Country Risk

Saudi Arabia does not have an EU adequacy decision.

The absence of an adequacy decision does not itself prove that every transfer is unlawful.

It does mean that the exporter cannot rely on an Article 45 finding that the destination provides an essentially equivalent level of protection.

The parties therefore must independently assess whether destination-country law and practice may interfere with the SCC commitments.

### 3.3 Government and Law-Enforcement Access

The following risk is considered material:

A processor located in the destination jurisdiction may become subject to binding legal demands for access to information in its possession or control.

Contractual commitments between private parties cannot override mandatory national law.

Accordingly, clauses requiring the importer to resist excessive requests, minimize disclosures, document requests, or notify the exporter are valuable procedural protections but cannot by themselves eliminate public-authority-access risk.

### 3.4 Legal Verification Limitation

This technical TIA does not make a definitive legal opinion on the complete body of Saudi national-security, criminal-procedure, telecommunications, or intelligence law.

Before production deployment, qualified privacy counsel should verify:

- Current applicable surveillance and disclosure authorities
- Scope of government access powers
- Available judicial or independent oversight
- Challenge mechanisms available to the importer
- Transparency restrictions
- Remedies available to affected individuals
- Any sector-specific requirements

### 3.5 UAE Legal Context

The UAE is relevant as the location of the original Controller and source system.

However, the Dubai-to-Frankfurt leg is not the EEA-to-third-country transfer being assessed under Chapter V.

The UAE legal environment may still affect:

- Original collection
- Controller obligations
- Employee privacy rights
- Data localization
- Security obligations
- Access to the source system

Those questions should be evaluated under applicable UAE privacy requirements separately from this Chapter V determination.

### Step 3 Risk Rating

**Pre-supplementary-measures risk: Medium-High**

Reasons:

- Destination lacks EU adequacy
- Direct identifiers may be transferred
- Financial information may be transferred
- Data relates to employees
- Processing is recurring
- Recipient may require some plaintext processing
- Contractual measures cannot override mandatory public-law requirements

### Step 3 Conclusion

The SCCs should not be relied upon without supplementary measures.

---

## Step 4 — Identify and Adopt Supplementary Measures

The following supplementary measures are required.

### 4.1 Data Minimization

The Riyadh Sub-processor should receive only fields required for the specific support activity.

Routine onward transfer should exclude:

- Health accommodation information
- Performance reviews
- Other HR information unrelated to payroll support

### 4.2 Pseudonymization

Emirates ID should be tokenized before the onward transfer wherever the recipient does not require the actual identifier.

Example:

~~text
Actual Emirates ID
        |
        v
Controlled Tokenization
        |
        +----> Mapping retained outside Riyadh
        |
        v
Opaque Employee Token
        |
        v
Riyadh Support Environment
~~

The reidentification mapping must remain under the control of the exporter or Controller.

### 4.3 Field-Level Encryption

Fields not required in plaintext should be encrypted before transfer.

Suitable targets may include:

- Emirates ID
- Bank IBAN
- Other direct identifiers

Encryption is most effective where the importer does not possess the key needed to recover plaintext.

### 4.4 TLS 1.3

TLS 1.3 must protect data in transit.

Residual limitation:

TLS protects the communication channel but does not protect information after the importer decrypts it.

TLS alone therefore does not address destination-country access risk.

### 4.5 Encryption at Rest

Personal information must remain encrypted in storage.

Where technically possible:

- Customer-managed keys should be used
- Key access should be restricted
- Key access should be logged
- Key rotation should be defined

### 4.6 Key Jurisdiction

Where field-level encryption is intended to reduce destination-access risk, decryption keys should not be placed under routine control of the Riyadh importer.

Giving both ciphertext and unrestricted decryption keys to the same recipient substantially reduces the value of encryption as a supplementary transfer measure.

### 4.7 Access Control

The importer must implement:

- Named user accounts
- MFA
- Least privilege
- Role-based access control
- Periodic entitlement reviews
- Privileged-access restrictions

### 4.8 Logging and Monitoring

Logging must cover:

- Successful access
- Failed access
- Administrative operations
- Data exports
- Privileged activity
- Authentication events
- Permission changes

Logs should be protected from unauthorized modification.

### 4.9 Contractual Controls

The importer must contractually commit to:

- Process only documented instructions
- Restrict onward transfers
- Challenge disproportionate government requests where legally permitted
- Minimize legally compelled disclosure
- Notify the exporter where legally permitted
- Maintain records of government requests where permitted
- Support audits
- Report security incidents without undue delay
- Delete or return data at the end of processing

### 4.10 Organizational Controls

Required organizational measures include:

- Security awareness training
- Privacy training
- Incident response procedures
- Personnel confidentiality obligations
- Sub-processor governance
- Access certification
- Periodic transfer review

### Step 4 Conclusion

The combination of minimization, pseudonymization, key separation, encryption, access control, monitoring, and contractual restrictions materially reduces transfer risk.

The strongest controls are those that reduce the amount of intelligible personal information accessible in Riyadh.

---

## Step 5 — Complete Formal Procedural Steps

The organization must complete the formal steps necessary to implement the selected safeguard.

Required actions include:

1. Execute the correct SCC Module 3 configuration.
2. Complete the SCC annexes accurately.
3. Document technical and organizational measures.
4. Record approved sub-processors.
5. Maintain this TIA with the SCC package.
6. Obtain appropriate Controller authorization for the sub-processor.
7. Record internal privacy/legal approval.
8. Document the supplementary measures as binding requirements.
9. Update internal records of processing and transfer inventories where applicable.

### Step 5 Conclusion

The transfer must not move into unrestricted production merely because the technical connection is available.

Contractual and governance prerequisites must be completed first.

---

## Step 6 — Re-evaluate at Appropriate Intervals

Transfer assessments are not one-time documents.

Reassessment should occur:

- At least annually
- When relevant laws change
- When regulatory guidance changes
- When the importer changes its processing architecture
- When new sub-processors are introduced
- When additional data categories are transferred
- After material security incidents
- When government-access practices materially change
- When encryption or key-management architecture changes

### Step 6 Conclusion

A material change that undermines the effectiveness of the SCCs or supplementary measures must trigger escalation.

Possible responses include:

- Additional controls
- Suspension of transfers
- Data localization
- Replacement of the sub-processor
- Termination of the transfer

---

# 4. Legal Basis and Transfer Mechanism

## Dubai → Frankfurt

GDPR Chapter V mechanism:

**Not required solely for this transfer direction because the destination is within the EEA.**

This does not remove other privacy, processor-contract, security, transparency, or UAE-law requirements.

## Frankfurt → Riyadh

Adequacy:

**No adequacy decision identified**

Transfer safeguard:

**SCC Module 3**

Additional requirement:

**Transfer Impact Assessment**

Supplementary measures:

**Required**

---

# 5. Government Access Risk Analysis

Government-access risk cannot be reduced simply by inserting contractual language.

The TIA therefore separates controls into three categories.

## Technical

Technical controls can reduce the amount of intelligible information accessible at the destination.

Examples:

- Strong pseudonymization
- Field-level encryption
- Key separation
- Data minimization

These measures provide the strongest reduction where the recipient does not need access to the protected plaintext.

## Contractual

Contractual controls can:

- Require request review
- Require challenges where legally available
- Require minimum disclosure
- Restrict voluntary disclosure
- Require documentation
- Require transparency where permitted

Their limitation is that private contracts cannot override mandatory law.

## Organizational

Organizational controls can:

- Limit employee access
- Establish escalation channels
- Ensure privacy review
- Monitor privileged use
- Maintain evidence
- Periodically reassess destination risk

These measures support accountability but do not independently eliminate public-authority access risk.

---

# 6. Special-Category Data

The source data contains health accommodation information.

Health information may constitute special-category data under GDPR Article 9.

Its presence materially increases the sensitivity of the processing.

The preferred design is:

**Do not routinely transfer health accommodation information to Riyadh.**

Where a payroll calculation genuinely requires a consequence of the accommodation, transfer only the minimum payroll-relevant result rather than the underlying health information where feasible.

Example:

Prefer:

~~text
payroll_adjustment_code = A17
~~

over:

~~text
medical_condition = [specific diagnosis]
~~

This follows the principle of data minimization.

---

# 7. Residual Risk Scoring

The following assessment uses an internal risk methodology and is not a statutory scoring formula.

| Risk Factor | Inherent Risk | Mitigation | Residual Risk |
|---|---|---|---|
| Direct employee identifiers | High | Pseudonymization | Low-Medium |
| Bank details | High | Minimization + encryption | Medium |
| Emirates ID | High | Tokenization + key separation | Low-Medium |
| Special-category health data | High | Exclude from routine onward transfer | Low |
| Network interception | Medium | TLS 1.3 | Low |
| Unauthorized employee access | High | RBAC + MFA + logging | Low-Medium |
| Privileged administrator access | High | PAM-like controls + monitoring | Medium |
| Public-authority access | High | Technical minimization + encryption + contractual safeguards | Medium |
| Uncontrolled onward transfer | High | SCC restrictions + approval controls | Low-Medium |
| Excessive retention | Medium | Retention limits + deletion | Low |

## Overall Inherent Risk

**High**

## Overall Residual Risk

**Medium**

The residual risk is considered tolerable only under the conditions documented below.

---

# 8. Required Conditions

The transfer may proceed only if all of the following conditions are satisfied:

1. SCC Module 3 is executed for Frankfurt → Riyadh.
2. SCC annexes accurately describe the actual processing.
3. Health accommodation data is excluded from routine Riyadh access.
4. Performance-review information is excluded.
5. Emirates ID is pseudonymized wherever operationally feasible.
6. Reidentification mappings remain outside routine Riyadh control.
7. Only minimum payroll support fields are transferred.
8. TLS 1.3 is required.
9. Stored personal data is encrypted.
10. Field-level encryption is applied where plaintext is unnecessary.
11. Cryptographic key access is separated from routine importer access where feasible.
12. MFA is required for privileged access.
13. Access is governed by least privilege.
14. Administrative access is logged.
15. Additional onward transfers require approval.
16. Government-access handling commitments are documented.
17. Incident notification obligations are contractually defined.
18. Retention periods are minimized.
19. Secure deletion is verified.
20. The TIA is periodically reassessed.

---

# 9. Conditions That Would Change the Recommendation

The recommendation should be changed to:

**DO NOT TRANSFER**

if any of the following occurs and cannot be remediated:

- Special-category data must routinely be provided in plaintext without an operational need.
- The recipient requires unrestricted access to all source HR records.
- Effective access control cannot be implemented.
- Required audit rights are refused.
- Unauthorized onward transfers cannot be prevented.
- The selected SCC obligations cannot be complied with in practice.
- Destination legal requirements prevent an acceptable level of protection.
- Effective technical supplementary measures cannot be implemented where necessary.
- Material changes invalidate the assumptions underlying this assessment.

---

# 10. Final Recommendation

## Decision

**PROCEED WITH CONDITIONS**

## Rationale

The Frankfurt-to-Riyadh transfer presents meaningful inherent risk because it involves recurring employee-data processing, financial information, government identifiers, and a non-adequate third-country destination.

However, the onward processing purpose does not require unrestricted access to the entire HR record.

The architecture can therefore materially reduce exposure through:

- Data minimization
- Exclusion of health information
- Exclusion of performance information
- Pseudonymization
- Field-level encryption
- Separate key control
- Strong identity controls
- Access monitoring
- Contractual restrictions
- Periodic reassessment

The transfer should proceed only when the importer receives the minimum intelligible information necessary to perform the approved payroll support function.

Where the importer does not require plaintext, effective pseudonymization or encryption should be preferred over reliance on contractual safeguards alone.

---

# 11. Evidence and Supporting Artifacts

This assessment is supported by:

- `data/dataflow.yaml`
- `diagrams/dataflow.dot`
- `diagrams/dataflow.png`
- `assessment/adequacy_report.json`
- `assessment/scc_module2.md`
- `assessment/scc_module3.md`
- `assessment/supplementary_measures_checklist.md`

---

# 12. Review Record

**Current decision:** Proceed with Conditions

**Current residual risk:** Medium

**Next review:** Annual review or earlier upon material change

Triggers for immediate review include:

- New destination country
- New sub-processor
- New sensitive data category
- Material legal change
- Security breach
- Major platform redesign
- Change in encryption or key-control architecture
- Change in public-authority-access risk
