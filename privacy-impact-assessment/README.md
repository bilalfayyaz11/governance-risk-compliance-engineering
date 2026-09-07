# Privacy Impact Assessment Engineering

A reproducible privacy engineering workflow for assessing regulated health and neural-signal processing workloads.

The implementation models a Brain-Computer Interface analytics platform processing patient identifiers, EEG signals, device metadata, session records, consent information, and clinician notes. It combines structured data inventory, automated privacy classification, DPIA risk analysis, NIST SP 800-53 control traceability, evidence hashing, and cryptographic report signing.

## What This Demonstrates

- Privacy engineering for sensitive healthcare and neural-signal workloads
- Structured PII and processing-activity inventories
- GDPR Article 6 and Article 9 processing analysis
- Saudi PDPL-aware privacy assessment
- Automated identification of high-risk and special-category information
- Data Protection Impact Assessment risk modeling
- Inherent versus residual privacy risk analysis
- Privacy risk treatment and accountability
- NIST SP 800-53 Rev. 5 control traceability
- Third-party processor risk assessment
- Cross-border data-transfer risk analysis
- Automated DPIA report generation
- SHA-256 evidence integrity
- Detached GPG report signing and verification

## Architecture

The workflow follows a simple evidence pipeline:

    PII Inventory
         |
         v
    Automated Classification
         |
         v
    DPIA Risk Register
         |
         v
    Mitigation and Control Mapping
         |
         v
    Automated DPIA Report
         |
         v
    SHA-256 Evidence + GPG Signature

Structured YAML is used as the source of truth rather than embedding privacy decisions directly into report prose.

Python consumes those structured records, performs classification and validation, and generates a consolidated assessment that can be reviewed by privacy, security, risk, and governance stakeholders.

## Regulated Workload

The modeled system is a Patient Neural Signal Analytics Platform supporting clinical Brain-Computer Interface processing.

The privacy inventory includes:

| Data Element | Classification | Sensitivity |
|---|---|---|
| Patient identifier | Direct identifier | High |
| EEG signal data | Special-category health / biometric-related information | High |
| Device IP address | Indirect identifier | Medium |
| Session timestamp | Indirect identifier | Medium |
| Consent record | Direct identifier | High |
| Clinician notes | Special-category health information | High |

Neural-signal and clinical information are automatically elevated to the highest privacy classification used by the workflow.

## Legal Basis Modeling

The assessment deliberately separates different regulatory concepts rather than presenting them as interchangeable.

For GDPR processing, the inventory records:

- Article 6 lawful basis
- Article 9 condition where special-category information is involved
- purpose of processing
- applicable safeguards

Saudi PDPL processing considerations are documented separately.

This prevents a common privacy-assessment error: assuming that a GDPR legal basis has a direct one-to-one equivalent under another privacy regime.

## Automated PII Classification

The classification engine reads the YAML inventory and assigns privacy risk tiers.

Classification logic includes:

    Special-category information -> Critical
    High-sensitivity identifiers -> High
    Medium-sensitivity identifiable information -> Medium
    Lower-sensitivity information -> Low

The workflow additionally records whether enhanced safeguards are required and preserves the results as machine-readable JSON evidence.

## DPIA Risk Model

A qualitative 3x3 risk matrix evaluates likelihood and impact.

The modeled risks include:

### R1 — Unauthorized Neural Data Access

Unauthorized access to raw EEG, biometric-related, or clinical information.

Primary mitigations include:

- encryption at rest and in transit
- least privilege
- strong authentication
- access logging
- environment segregation

Inherent risk: High  
Residual risk: Medium

### R2 — Re-identification

Re-identification through device metadata, timestamps, or correlation with auxiliary datasets.

Primary mitigations include:

- data minimization
- pseudonymization
- separation of identity mappings
- restricted linkage keys
- retention limits

Inherent risk: Medium  
Residual risk: Low

### R3 — Third-Party Processor Exposure

Excessive access or uncontrolled processing by an external cloud analytics provider.

Primary mitigations include:

- processor due diligence
- contractual processing restrictions
- minimum-necessary disclosure
- pseudonymization
- processor access controls
- subprocessor oversight

Inherent risk: High  
Residual risk: Medium

### R4 — Cross-Border Processing

Transfer of sensitive BCI or health information to jurisdictions without equivalent protections.

Primary mitigations include:

- transfer necessity assessment
- applicable legal safeguards
- transfer-risk analysis
- encryption
- data minimization
- documented privacy and legal approval

Inherent risk: High  
Residual risk: Medium

The validation logic confirms that residual risk is lower than inherent risk for every modeled scenario.

## NIST SP 800-53 Traceability

Privacy risks are mapped to controls according to the actual purpose of each mitigation.

Examples include:

| Risk | Primary Control | Supporting Controls |
|---|---|---|
| R1 | PT-2 Authority to Process PII | PT-7, AC-6, SC-13 |
| R2 | PT-3 PII Processing Purposes | SI-12(1), PT-7 |
| R3 | PM-30 Supply Chain Risk Management Strategy | PT-2, PT-3, SR-6 |
| R4 | PT-2 Authority to Process PII | PT-3, PM-27, SC-13 |

Technical protections are mapped to applicable security families rather than artificially assigning every mitigation to PT or PM.

This distinction is important in real control-engineering work because privacy governance controls and technical enforcement controls solve different parts of the risk.

## Automated DPIA Report

The report generator consolidates:

- workload overview
- PII inventory
- automated risk classifications
- GDPR and PDPL processing analysis
- DPIA risk register
- treatment detail
- NIST control mappings
- residual risk
- DPO recommendation

The resulting report is stored at:

    reports/DPIA_Report.md

The simulated recommendation is:

    PROCEED WITH CONDITIONS

The recommendation requires the documented safeguards to be implemented and monitored, particularly for neural information, external processors, and international transfers.

## Evidence Integrity

Critical assessment artifacts are protected with SHA-256 hashes.

Evidence includes:

    evidence/pii-inventory.sha256
    evidence/pii-classification.sha256
    evidence/dpia-risk-register.sha256
    evidence/control-mapping.sha256
    evidence/dpia-report.sha256

This provides a basic chain for detecting unintended modification of assessment evidence.

## Cryptographic Report Signing

The final DPIA report is signed using a detached GPG signature:

    reports/DPIA_Report.md.sig

A public verification key is included at:

    evidence/privacy-officer-public-key.asc

The private signing key is deliberately excluded from the repository.

To verify the report independently:

    gpg --import evidence/privacy-officer-public-key.asc

    gpg --verify \
      reports/DPIA_Report.md.sig \
      reports/DPIA_Report.md

A successful verification should report a good signature for the simulated Privacy Officer identity.

The key is generated specifically for this demonstration workflow and does not represent a production organizational identity.

## Repository Structure

    privacy-impact-assessment/
    |
    |-- automation/
    |   |-- classify_pii.py
    |   `-- generate_report.py
    |
    |-- data/
    |   |-- pii_inventory.yaml
    |   |-- dpia_risk_register.yaml
    |   `-- control_mapping.yaml
    |
    |-- evidence/
    |   |-- pii-classification-results.json
    |   |-- pii-inventory.sha256
    |   |-- pii-classification.sha256
    |   |-- dpia-risk-register.sha256
    |   |-- control-mapping.sha256
    |   |-- dpia-report.sha256
    |   `-- privacy-officer-public-key.asc
    |
    |-- reports/
    |   |-- DPIA_Report.md
    |   `-- DPIA_Report.md.sig
    |
    `-- README.md

## Engineering Decisions

### Structured Data Before Documents

Privacy decisions are maintained in YAML and JSON first.

The report is an output of the evidence model rather than the primary source of truth.

This makes the assessment easier to validate, automate, review, and integrate into broader governance workflows.

### Regulatory Grounds Are Separated

GDPR Article 6, GDPR Article 9, and Saudi PDPL considerations are represented independently.

This reduces the risk of creating misleading cross-framework equivalences.

### Privacy Controls and Security Controls Are Distinguished

Privacy governance requirements are mapped to PT and PM controls where appropriate.

Technical mitigations such as encryption and least privilege remain mapped to the security controls that actually implement them.

### Residual Risk Is Explicit

The workflow does not stop at identifying threats.

Every risk records:

- inherent likelihood
- inherent impact
- inherent risk
- mitigation
- residual likelihood
- residual impact
- residual risk
- accountable owner
- treatment decision

This creates a decision-oriented DPIA rather than a compliance checklist.

### Signing Keys Are Not Committed

Only the public verification key is included.

Private GPG key material remains outside the repository.

## Technologies

- Python 3
- PyYAML
- JSON
- YAML
- Markdown
- GnuPG
- SHA-256
- Git
- NIST SP 800-53 Rev. 5
- GDPR privacy concepts
- Saudi PDPL privacy concepts

## Governance Outcomes

This implementation demonstrates how privacy assessment can be treated as an engineering workflow rather than a static document exercise.

It provides traceability from:

    personal data
        ->
    processing purpose
        ->
    privacy classification
        ->
    privacy risk
        ->
    mitigation
        ->
    control
        ->
    residual risk
        ->
    approval recommendation
        ->
    signed evidence

That traceability supports privacy engineering, GRC, security assurance, regulated AI governance, and data-protection review processes.

## Disclaimer

This repository demonstrates privacy engineering and control-traceability techniques. It is not legal advice and does not independently establish compliance with GDPR, Saudi PDPL, or any other law.

Actual lawful bases, special-category processing conditions, healthcare requirements, international-transfer mechanisms, and regulator obligations must be evaluated for the specific organization, processing purpose, jurisdiction, and deployment context.
