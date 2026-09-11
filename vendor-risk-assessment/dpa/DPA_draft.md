# Data Processing Agreement

## 1. Subject Matter and Duration

This Data Processing Agreement governs the processing of personal data by ACME Vendor on behalf of the Controller in connection with hosted application, infrastructure, support, security, and related technology services.

Processing shall continue only for the duration of the underlying services agreement or for such shorter or longer period as documented by the Controller where legally permitted.

Upon termination or expiry of the services, the Processor shall return or securely delete personal data in accordance with documented Controller instructions and applicable legal retention requirements.

## 2. Nature and Purpose of Processing

The Processor may process personal data only to provide the contracted services and perform activities explicitly documented by the Controller.

### Categories of Data Subjects

Processing may include personal data relating to:

- Customers and end users
- Employees and authorized users
- Contractors and business representatives
- Support contacts
- Other individuals whose personal data is submitted through the services

### Categories of Personal Data

Depending on the services used, processing may include:

- Names and identifiers
- Email addresses and contact information
- Account and authentication information
- Customer application data
- Device and network information
- Support communications
- Usage and audit records
- Other personal data intentionally submitted by the Controller

The Processor shall not independently determine new processing purposes inconsistent with the Controller's documented instructions.

## 3. Processor Obligations

The Processor shall:

1. Process personal data only on documented instructions from the Controller, including instructions relating to transfers of personal data.

2. Ensure that personnel authorized to process personal data are subject to appropriate confidentiality obligations.

3. Implement and maintain appropriate technical and organizational measures proportionate to the nature, scope, context, and risks of processing.

4. Assist the Controller, where reasonably required, with:
   - data subject rights requests,
   - security assessments,
   - personal data breach investigations,
   - regulatory inquiries,
   - data protection impact assessments,
   - deletion and return obligations.

5. Maintain appropriate records demonstrating processing activities performed on behalf of the Controller.

6. Promptly notify the Controller if an instruction appears to conflict with applicable data protection requirements.

### GDPR

Where the GDPR applies, the Processor shall comply with the requirements applicable to processors under Article 28, including the contractual requirements of Article 28(3).

### UAE PDPL

Where UAE Federal Decree-Law No. 45 of 2021 applies, the Processor shall comply with the Processor obligations established under Article 8, including:

- processing in accordance with Controller instructions and contractual scope,
- appropriate technical and organizational protection,
- processing only for the defined purpose and duration,
- deletion or return after the processing period,
- protection against unauthorized disclosure,
- maintenance of processing records where required,
- demonstration of compliance when requested.

### KSA PDPL

Where the Saudi Personal Data Protection Law and its Implementing Regulations apply, the Processor shall:

- process personal data within the Controller's documented instructions,
- provide sufficient guarantees for protecting personal data,
- support the Controller's compliance obligations,
- identify subcontractors involved in processing,
- notify the Controller of material non-compliance without undue delay.

Processor and sub-processor arrangements shall comply with the applicable Saudi PDPL and Implementing Regulations, including the requirements governing Processor selection and subsequent sub-processing arrangements.

## 4. Sub-Processor Flow-Down

### 4.1 Authorization

The Controller grants general written authorization for the Processor to engage sub-processors subject to the requirements of this section.

The Processor shall maintain and provide an up-to-date list of approved sub-processors, including:

- legal entity name,
- processing purpose,
- categories of personal data processed,
- processing location,
- hosting or infrastructure location where applicable.

### 4.2 Prior Notice

The Processor shall provide the Controller with at least **30 calendar days' prior written notice** before appointing a new sub-processor or materially replacing an existing sub-processor.

The notice shall include sufficient information to allow the Controller to assess potential data protection and security risks.

### 4.3 Right to Object

The Controller may object on reasonable data protection or security grounds during the notice period.

Where an objection is raised, the parties shall work in good faith to:

1. address the identified risk,
2. implement additional safeguards,
3. use an alternative sub-processor where reasonably possible,
4. modify the affected processing activity where necessary.

If no reasonable resolution can be achieved, the Controller may exercise contractual remedies available under the underlying services agreement.

### 4.4 Flow-Down Obligations

Before allowing a sub-processor to process personal data, the Processor shall enter into a binding written agreement imposing data protection obligations that are no less protective than those imposed on the Processor under this DPA where applicable to the sub-processor's services.

The sub-processor agreement shall address, as applicable:

- confidentiality,
- security measures,
- processing limitations,
- breach notification,
- assistance obligations,
- deletion and return,
- audit cooperation,
- international transfers,
- further sub-processing.

### 4.5 Processor Responsibility

The Processor remains responsible to the Controller for the performance of its sub-processors to the extent required by applicable law and the parties' agreement.

### 4.6 Current Disclosed Sub-Processors

Based on the vendor due-diligence response currently provided:

| Provider | Location | Processing Role | Status |
|---|---|---|---|
| AWS | Ireland | Hosting / infrastructure | Disclosed |
| SubProcessor-X | India | Support or processing services | Disclosed; further review required |

The vendor must provide complete processing-purpose, entity, security, and transfer-mechanism details before final approval.

## 5. Cross-Border Transfers

The Processor shall not transfer personal data outside an approved jurisdiction or permit remote access constituting an international transfer unless:

1. the Controller has been informed of the destination and processing circumstances,
2. an appropriate transfer mechanism is available,
3. required contractual and technical safeguards are implemented,
4. any required transfer assessment has been completed,
5. sub-processors are contractually bound to equivalent obligations.

Detailed transfer controls are addressed in the separate Cross-Border Data Transfer Addendum.

## 6. Security, Audit and Assistance

### Security Measures

The Processor shall maintain safeguards appropriate to the risks associated with processing, including where applicable:

- multi-factor authentication for privileged access,
- encryption at rest,
- encryption in transit,
- access controls and least privilege,
- vulnerability management,
- security logging and monitoring,
- incident response controls,
- backup and recovery protections.

The vendor questionnaire indicates:

- MFA is enforced for privileged administrator access.
- Production storage uses AES-256 encryption.
- TLS 1.2 or TLS 1.3 is used for data in transit.

These controls remain subject to evidence validation.

### Breach Notification

The vendor has stated an initial breach-notification target of **24 hours following confirmation of an incident**.

Accordingly, the Processor shall notify the Controller without undue delay and, contractually, no later than 24 hours after becoming aware of a confirmed personal data breach affecting Controller data.

Initial notification should include available information regarding:

- incident date and time,
- affected systems,
- categories of personal data,
- estimated affected individuals or records,
- known or suspected cause,
- containment measures,
- likely consequences,
- investigation status.

The Processor shall provide supplemental information as the investigation progresses.

### Audit Rights

The Processor shall provide information reasonably necessary to demonstrate compliance with this DPA.

Independent assurance reports, certifications, security documentation, and related evidence may be used to support audit requirements.

Where such evidence is insufficient or a material compliance concern exists, the Controller may conduct or commission a reasonable audit subject to appropriate confidentiality, security, and operational safeguards.

## 7. Data Deletion and Return

Control C7 of the vendor assessment remains unresolved because the vendor did not confirm its ability to certify deletion within 30 days following contract termination.

This item is therefore a **High-severity remediation requirement**.

Before production approval, the Processor must provide a documented deletion and return procedure specifying:

- deletion timeline,
- deletion method,
- backup handling,
- legal retention exceptions,
- sub-processor deletion requirements,
- evidence or certification of deletion.

The contractual target shall be deletion or return of Controller personal data within **30 calendar days** after termination or receipt of a valid deletion instruction, except where applicable law requires continued retention.

Where retention is legally required, retained personal data shall:

- remain protected,
- be isolated from ordinary processing,
- be used only for the legally required retention purpose,
- be deleted when the retention obligation expires.

## 8. Compliance Evidence

The Processor shall retain evidence reasonably necessary to demonstrate compliance with its obligations, including where applicable:

- security policies,
- access-control records,
- encryption standards,
- incident response procedures,
- sub-processor registers,
- audit reports,
- deletion records,
- transfer assessments,
- remediation evidence.

## 9. Outstanding Vendor Due-Diligence Actions

The following matters must be resolved before final vendor approval:

1. **C4 — Critical:** complete sub-processor disclosure and location information.
2. **C7 — High:** documented and certifiable deletion within the agreed contractual period.

These issues shall be tracked through the remediation register maintained as part of the vendor governance process.
