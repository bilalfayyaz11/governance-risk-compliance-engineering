# Cross-Border Data Transfer Addendum

## 1. Purpose

This Addendum governs international transfers of personal data processed by ACME Vendor and its approved sub-processors where personal data is transferred, remotely accessed, stored, or otherwise processed outside the originating jurisdiction.

The Addendum supplements the Data Processing Agreement and applies to transfer scenarios identified through vendor due diligence.

## 2. Disclosed Processing Locations

Based on the current vendor questionnaire:

| Provider | Location | Processing Context | Current Assessment |
|---|---|---|---|
| AWS | Ireland | Hosting / infrastructure | Disclosed |
| SubProcessor-X | India | Support or processing services | Requires documented transfer safeguards |

The vendor must maintain an accurate and current list of all jurisdictions in which Controller personal data is stored, accessed, transmitted, or otherwise processed.

No undisclosed international processing location may be introduced without following the sub-processor and transfer-change requirements in the DPA.

## 3. Transfer Mechanisms

The Processor shall not conduct an international transfer unless a legally valid transfer basis is identified for the relevant jurisdiction.

Depending on the originating jurisdiction and destination, the applicable mechanism may include:

- an adequacy decision or formally recognized adequate jurisdiction,
- approved standard contractual clauses,
- another legally recognized contractual transfer mechanism,
- approved binding organizational safeguards where applicable,
- a specific transfer mechanism permitted by applicable UAE requirements,
- a transfer mechanism permitted under Saudi PDPL and its implementing transfer requirements.

The selected mechanism must be documented before the transfer begins.

## 4. GDPR / EEA Transfer Requirements

Where GDPR Chapter V applies and personal data is transferred outside the EEA to a jurisdiction not covered by an applicable adequacy decision, the Processor shall implement an appropriate transfer mechanism.

Where Standard Contractual Clauses are used:

- the appropriate SCC module shall be selected,
- Annexes describing processing and security measures shall be completed,
- relevant sub-processors and destinations shall be identified,
- a transfer risk assessment shall be completed where required,
- supplementary safeguards shall be implemented where necessary.

The Processor shall not rely solely on contractual wording where the transfer assessment identifies material technical, legal, or governmental-access risks that require additional controls.

## 5. KSA PDPL Transfer Requirements

Where Saudi personal data is transferred outside the Kingdom, the transfer must comply with applicable Saudi PDPL cross-border transfer requirements and related implementing rules.

Before transfer, the Controller and Processor shall determine whether:

- the destination satisfies applicable protection requirements,
- an approved or otherwise lawful transfer basis is available,
- a transfer risk assessment is required,
- contractual safeguards are necessary,
- additional technical or organizational measures are required,
- regulatory approval or other procedural steps apply.

Where a transfer impact or risk assessment is required, it should address at minimum:

- categories and sensitivity of personal data,
- volume and frequency of transfer,
- destination jurisdiction,
- recipient and sub-processor identities,
- purpose of processing,
- onward-transfer risks,
- security controls,
- legal and governmental access risks,
- mitigation measures,
- residual risk.

The assessment and supporting evidence must be retained as part of the vendor governance record.

## 6. UAE PDPL Transfer Requirements

Where the UAE Federal Decree-Law No. 45 of 2021 applies, international transfers shall be evaluated against the applicable cross-border transfer provisions.

The parties shall determine whether the destination benefits from an applicable recognized level of protection or whether another legally permitted safeguard is required.

Where contractual safeguards are used, they should address:

- processing limitations,
- confidentiality,
- information security,
- onward transfers,
- sub-processing,
- breach notification,
- deletion and return,
- cooperation with the Controller,
- data subject rights support,
- regulatory cooperation.

No transfer shall proceed solely because a vendor has disclosed a destination. Disclosure and lawful transfer authorization are separate requirements.

## 7. Transfer Assessment for AWS — Ireland

The vendor disclosed AWS infrastructure in Ireland.

For transfers governed by EU/EEA data protection rules, Ireland is within the EEA and therefore does not itself constitute a transfer outside the EEA when processing remains within Ireland.

However, the vendor must still document:

- the actual AWS legal entity,
- selected AWS region,
- support-access locations,
- disaster-recovery locations,
- subprocessors with access to the environment,
- any onward transfers outside the EEA.

If support, telemetry, administrative access, or other operations involve additional jurisdictions, those transfers require separate evaluation.

## 8. Transfer Assessment for SubProcessor-X — India

The vendor disclosed SubProcessor-X in India.

Before approval, the vendor must provide:

- full legal name of SubProcessor-X,
- registered address,
- processing purpose,
- categories of personal data processed,
- categories of data subjects,
- system access model,
- storage location,
- remote-access locations,
- onward sub-processors,
- security controls,
- deletion controls,
- transfer mechanism.

The India-based processing relationship shall remain **conditionally approved / remediation required** until the appropriate transfer mechanism and safeguards are documented.

## 9. Supplementary Safeguards

Where a destination or processing arrangement creates elevated transfer risk, the parties shall consider additional safeguards including:

### Technical Measures

- encryption in transit using current secure protocols,
- encryption at rest,
- customer-controlled or segregated encryption keys where practical,
- pseudonymization or tokenization,
- access restrictions,
- least-privilege administration,
- strong authentication,
- data minimization,
- regional storage restrictions,
- detailed security logging.

### Organizational Measures

- restricted personnel access,
- confidentiality obligations,
- documented government-request handling,
- incident escalation,
- periodic access review,
- sub-processor governance,
- staff security training,
- transfer-specific procedures.

### Contractual Measures

- purpose restrictions,
- onward-transfer restrictions,
- audit rights,
- security obligations,
- breach notification commitments,
- deletion obligations,
- transparency requirements,
- cooperation with regulatory authorities,
- termination rights for unresolved transfer risk.

## 10. Onward Transfers

The Processor and each approved sub-processor shall not transfer personal data to another recipient or jurisdiction unless:

1. the Controller is informed where required,
2. any required authorization is obtained,
3. a lawful transfer mechanism applies,
4. equivalent contractual and security obligations flow down,
5. the transfer is recorded in the sub-processor register.

## 11. Transfer Change Notification

The Processor shall notify the Controller before materially changing:

- processing country,
- hosting region,
- support location,
- sub-processor location,
- onward-transfer arrangement,
- transfer mechanism.

Where the change involves a new sub-processor, the notice and objection provisions of the DPA also apply.

## 12. Evidence Requirements

For every international transfer, the vendor should be able to produce, where applicable:

- sub-processor register,
- processing-location inventory,
- applicable transfer agreement,
- SCCs or equivalent contractual safeguards,
- transfer impact or risk assessment,
- security-control documentation,
- relevant certifications or assurance reports,
- approval records,
- remediation evidence.

## 13. Current Transfer Remediation Status

### C4 — Critical

The vendor's sub-processor disclosure remains incomplete for approval purposes.

Although AWS in Ireland and SubProcessor-X in India have been identified, the vendor has not yet provided sufficient contractual, security, transfer-mechanism, and onward-processing information.

**Status:** Open  
**Severity:** Critical

Required action:

- provide complete sub-processor details,
- identify all processing locations,
- document transfer mechanisms,
- provide evidence of supplementary safeguards where necessary,
- confirm onward-transfer arrangements.

## 14. Transfer Approval Decision

International processing may proceed only after the relevant transfer mechanism, recipient information, locations, and safeguards have been reviewed and accepted in accordance with applicable law and the Controller's third-party risk process.

Until C4 remediation is completed, international sub-processing involving SubProcessor-X shall be treated as requiring further review before final vendor approval.
