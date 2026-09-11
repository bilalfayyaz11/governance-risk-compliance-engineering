# SCC Module 3 — Processor to Processor

## Transfer Context

**Exporter:** Frankfurt Payroll Processor  
**Location:** Frankfurt, Germany  
**Role:** Processor

**Importer:** Riyadh Payroll Support Services  
**Location:** Riyadh, Saudi Arabia  
**Role:** Sub-processor / Processor

This document describes the processor-to-processor onward transfer that requires GDPR Chapter V analysis.

## Transfer Purpose

The transfer supports:

- Regional payroll exception handling
- Payroll support operations
- Investigation of payroll discrepancies
- Authorized support activities

The Riyadh importer must not use the data for independent purposes.

## Data Subjects

- Current employees
- Former employees subject to valid payroll retention requirements

## Personal Data Categories

Potentially transferred data includes:

- Full legal name
- Work email
- Emirates ID
- Salary
- Bank IBAN

Health accommodation data should be excluded from the Riyadh transfer unless strictly necessary and separately approved.

## Transfer Frequency

Transfers may occur:

- During monthly payroll cycles
- When support escalation requires access
- During approved exception handling

## Transfer Mechanism

Saudi Arabia does not have an EU adequacy decision in this assessment.

The selected transfer mechanism is:

**SCC Module 3 — Processor to Processor**

The SCC mechanism is supplemented by:

- Transfer Impact Assessment
- Technical controls
- Contractual controls
- Organizational controls
- Periodic reassessment

## Documented Instructions

The Riyadh importer may process personal data only on documented instructions received through the Frankfurt Processor acting within the instructions of the Dubai Controller.

The importer must not:

- Determine independent processing purposes
- Reuse data for unrelated analytics
- Combine the data with unrelated datasets
- Retain data beyond approved support periods
- Conduct onward transfers without authorization

## Confidentiality

Personnel with access to transferred data must:

- Be bound by confidentiality obligations
- Receive privacy and security training
- Have access limited according to job responsibilities
- Use named individual accounts
- Be subject to access logging

## Security Measures

Required measures include:

- TLS 1.3 in transit
- Encryption at rest
- Strong identity authentication
- Least-privilege access
- Administrative access monitoring
- Centralized security logging
- Session monitoring for privileged activity
- Data minimization
- Restricted export functionality

## Pseudonymization

Where operationally feasible:

- Emirates ID should be replaced with a token before transfer.
- Payroll support should use an internal employee reference.
- Reidentification information should remain outside the importer environment.
- Token mapping should be controlled by the exporter or Controller.

Effective pseudonymization materially reduces the usefulness of transferred data to an unauthorized party.

## Cryptographic Key Control

Where client-side or field-level encryption is used:

- Encryption should occur before the data leaves the controlled EEA processing environment.
- Keys required to decrypt protected fields should not be available to the Riyadh importer unless strictly required.
- Key access should be logged.
- Key rotation procedures should be documented.
- Administrative access to key-management systems should be tightly restricted.

## Government Access Requests

The importer must:

- Review government-access requests for legality.
- Challenge requests where there are reasonable grounds and applicable law permits.
- Disclose only the minimum data legally required.
- Maintain records of requests where legally permitted.
- Notify the exporter where legally permitted.
- Provide transparency information regarding request handling.

A contractual commitment does not override mandatory local law and therefore cannot be treated as sufficient by itself.

## Onward Transfers

The Riyadh importer must not make additional onward transfers unless:

1. The onward recipient is authorized.
2. A valid Chapter V mechanism applies where required.
3. Equivalent protections are contractually imposed.
4. The exporter is informed.
5. Transfer-risk implications are reassessed.

## Audit Rights

The Frankfurt Processor must have access to information necessary to verify compliance.

Evidence may include:

- Independent audit reports
- Technical-control evidence
- Access-control records
- Security certifications
- Logging samples
- Sub-processor information
- Incident records

Targeted audit rights should remain available where material risk justifies deeper review.

## Breach Notification

The Riyadh importer must notify the Frankfurt Processor without undue delay after becoming aware of a personal-data breach.

The notice should include available information concerning:

- Nature of the breach
- Categories of affected data
- Number of affected records
- Number of affected individuals
- Likely consequences
- Containment
- Remediation
- Timeline

## Clause 14 Transfer Impact Considerations

The parties must assess whether the laws and practices applicable in the destination country could prevent the importer from complying with the SCCs.

The assessment must consider:

- Specific circumstances of the transfer
- Nature of the data
- Transfer frequency
- Storage duration
- Processing purpose
- Technical architecture
- Relevant local legal requirements
- Potential public-authority access
- Practical safeguards

The parties must not rely merely on the existence of SCCs if the required level of protection cannot be achieved in practice.

## Suspension and Termination

Where adequate protection cannot be maintained, the exporter must be able to:

- Suspend transfers
- Require corrective measures
- Terminate the processing relationship
- Require return or deletion of transferred data

## Review Cycle

The transfer arrangement should be reviewed:

- At least annually
- After material legal changes
- After significant security incidents
- After major architectural changes
- When new data categories are added
- When new onward recipients are introduced
