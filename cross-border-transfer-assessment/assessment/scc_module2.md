# SCC Module 2 — Controller to Processor

## Purpose of This Document

This document satisfies the exercise requirement to populate an SCC Module 2-style record for the relationship between the Dubai HR Controller and the Frankfurt Payroll Processor.

However, this document is **not treated as the GDPR Chapter V transfer mechanism for the Dubai-to-Frankfurt leg**, because Frankfurt is located within the EEA.

The actual onward transfer from the Frankfurt Processor to the Riyadh Sub-processor is assessed separately under SCC Module 3.

## Parties

### Data Exporter / Controller

**Entity:** Dubai HR Controller  
**Location:** Dubai, United Arab Emirates  
**Role:** Controller

Responsibilities include:

- Determining the purpose of employee payroll processing
- Determining the categories of HR data collected
- Approving processors and sub-processors
- Defining retention and access requirements
- Maintaining employee privacy governance

### Data Importer / Processor

**Entity:** Frankfurt Payroll Processor  
**Location:** Frankfurt, Germany  
**Role:** Processor

Responsibilities include:

- Processing employee data only on documented instructions
- Applying appropriate technical and organizational measures
- Restricting personnel access
- Maintaining processing records
- Supporting security and privacy obligations
- Controlling onward transfers to approved sub-processors

## Processing Purpose

The processing purpose is payroll administration, including:

- Salary calculation
- Payroll reconciliation
- Salary payment preparation
- Statutory payroll reporting
- Payroll correction handling

Processing must not be expanded to unrelated purposes without documented authorization.

## Data Subjects

The covered data subjects are:

- Current employees
- Former employees whose payroll records remain subject to valid retention obligations

## Categories of Personal Data

The processing may include:

| Data Field | Classification |
|---|---|
| Full legal name | Confidential |
| Work email | Internal |
| Emirates ID | Confidential |
| Salary | Confidential |
| Bank IBAN | Confidential |
| Performance review | Confidential |
| Health accommodation information | Special Category |

Health accommodation data may reveal health status and therefore requires heightened protection.

## Processing Frequency

Processing is recurring and normally occurs during the monthly payroll cycle.

Ad-hoc transfers may occur where payroll corrections or legally required adjustments are necessary.

## Processing Duration

Processing is limited to the duration necessary for:

- Payroll execution
- Contractual processor obligations
- Statutory retention
- Approved incident investigation
- Authorized audit requirements

Data must be deleted or returned when no longer necessary, subject to valid legal retention requirements.

## Processor Instructions

The Frankfurt Processor must:

- Process data only on documented controller instructions
- Restrict access to authorized personnel
- Apply confidentiality obligations
- Prevent unauthorized secondary use
- Maintain appropriate technical and organizational security controls
- Support requests relating to affected data subjects where required
- Notify the controller of security incidents without undue delay
- Maintain evidence of compliance

## Sub-processor Authorization

**Authorization model: General authorization with prior notice and objection rights**

The Frankfurt Processor may engage approved sub-processors where:

1. The Controller receives advance notice.
2. The Controller is given a reasonable opportunity to object.
3. Equivalent data-protection obligations are imposed on the sub-processor.
4. The Processor remains accountable for the performance of the sub-processor's obligations.

The current hypothetical sub-processor is:

**Riyadh Payroll Support Services — Riyadh, Saudi Arabia**

Purpose:

Regional payroll support and exception handling.

## Security Obligations

Minimum controls include:

- TLS 1.3 for data in transit
- Encryption at rest
- Strong role-based access control
- Least privilege
- Access logging
- Administrative activity logging
- Data minimization
- Segregation of duties
- Regular access reviews
- Incident detection and response
- Secure key management
- Controlled backup access

## Special-Category Data

Health accommodation information must receive additional protection.

Where possible, this information should not be transferred to a payroll processor unless strictly necessary for the payroll purpose.

If transfer is necessary, access must be narrowly restricted and technical protection strengthened.

## Audit Rights

The Controller must be able to obtain information necessary to demonstrate processor compliance.

Audit rights include:

- Security-control evidence review
- Access-control review
- Sub-processor register review
- Incident-response evidence
- Relevant independent assurance reports
- Targeted audits where materially justified

Audits should be proportionate and should avoid compromising the security or confidentiality of other customers.

## Incident Notification

The Processor must notify the Controller without undue delay after becoming aware of a personal-data breach affecting the covered processing.

The notice should include, where available:

- Nature of the incident
- Systems affected
- Categories of data involved
- Approximate number of affected data subjects
- Likely consequences
- Containment actions
- Remediation measures
- Sub-processors affected
- Relevant timestamps

## Liability and Accountability

Each party remains responsible for obligations applicable to its role.

The Processor remains responsible for ensuring that authorized sub-processors comply with equivalent contractual data-protection obligations.

Commercial liability allocation must not be interpreted to reduce mandatory rights or obligations imposed by applicable data-protection law.

## Return and Deletion

At the end of processing, personal data must be returned or securely deleted according to Controller instructions unless retention is required by applicable law.

Deletion should include:

- Primary records
- Temporary processing copies
- Export files
- Staging data
- Cached data

Backup deletion may follow documented lifecycle schedules where immediate deletion is technically impracticable, provided the data remains protected and inaccessible for operational use.

## Legal Architecture Note

This Module 2-style document records Controller-to-Processor obligations for the Dubai-to-Frankfurt relationship.

It is **not relied upon as the Chapter V safeguard for that leg**, because the destination is Germany.

The onward Frankfurt-to-Riyadh transfer is evaluated separately under SCC Module 3.
