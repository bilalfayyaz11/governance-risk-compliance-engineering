# Internal ISMS Audit Plan

## Audit Objective

The objective of this internal audit is to evaluate whether the organization's Information Security Management System is:

- aligned with ISO/IEC 27001:2022 requirements
- operating as intended
- supported by appropriate evidence
- effectively implemented across selected business and technical processes
- capable of identifying and addressing information security weaknesses

The audit also aims to identify nonconformities, observations, and opportunities for improvement that can strengthen the ISMS.

## Organization

Fictitious Organization:

    Meridian FinTech Services Ltd.

Business Context:

Meridian FinTech Services Ltd. provides digital financial services and cloud-hosted customer platforms. The organization relies on centralized identity services, cloud infrastructure, internal HR processes, and third-party technology providers.

## Scope

The internal audit includes the following areas:

### Cloud Infrastructure

- cloud infrastructure administration
- privileged access
- secure authentication
- configuration management
- security monitoring
- web filtering
- incident readiness

### Human Resources

- employee onboarding
- information security awareness
- role changes
- termination responsibilities
- access revocation

### Governance

- information security policies
- threat intelligence
- access-control governance
- cloud-service security governance
- incident-management preparation
- ICT continuity readiness

### Physical Security

- physical security monitoring controls applicable to administrative locations

The audit excludes:

- financial accounting controls
- software product quality assurance
- unrelated operational processes outside the ISMS scope
- external supplier environments not directly controlled by the organization

## Audit Criteria

The audit criteria include:

### ISO/IEC 27001:2022 Clauses

- Clause 4 — Context of the organization
- Clause 5 — Leadership
- Clause 6 — Planning
- Clause 7 — Support
- Clause 8 — Operation
- Clause 9 — Performance evaluation
- Clause 10 — Improvement

### Selected Annex A Controls

The detailed control sample is maintained in:

    plan/annex_a_checklist.csv

Selected controls include:

- A.5.1 — Policies for information security
- A.5.7 — Threat intelligence
- A.5.15 — Access control
- A.5.18 — Access rights
- A.5.23 — Information security for use of cloud services
- A.5.24 — Information security incident management planning and preparation
- A.5.30 — ICT readiness for business continuity
- A.6.3 — Information security awareness, education and training
- A.6.5 — Responsibilities after termination or change of employment
- A.7.4 — Physical security monitoring
- A.8.2 — Privileged access rights
- A.8.5 — Secure authentication
- A.8.9 — Configuration management
- A.8.16 — Monitoring activities
- A.8.23 — Web filtering

## Audit Approach

The audit will use a risk-based evidence approach combining:

- document review
- interviews
- technical walkthroughs
- configuration inspection
- evidence sampling
- checklist evaluation
- finding classification

Audit conclusions will be based on sufficient and relevant evidence collected during the defined scope.

## Audit Team and Roles

| Role | Name | Responsibility |
|---|---|---|
| Lead Auditor | Sara Ahmed | Audit planning, interviews, evidence review, finding classification, final report |
| Technical Auditor | Omar Khan | Technical walkthroughs, configuration checks, cloud and access-control review |
| ISMS Coordinator | Nadia Ali | Provides ISMS documentation and coordinates evidence requests |
| Cloud Infrastructure Lead | Hamza Siddiqui | Auditee for cloud infrastructure and technical security controls |
| HR Manager | Ayesha Malik | Auditee for onboarding, awareness, role-change, and termination controls |

## Auditor Independence

The audit team is assumed to be independent from the activities being directly audited.

Auditors will avoid evaluating controls for which they have direct operational ownership.

## Audit Schedule

| Date | Session | Auditee / Area | Location |
|---|---|---|---|
| 2026-09-10 | Opening Meeting | ISMS Coordinator and Management | Virtual |
| 2026-09-10 | Policy and Governance Review | ISMS Coordinator | Virtual |
| 2026-09-10 | Cloud Infrastructure Interview | Cloud Infrastructure Lead | Virtual |
| 2026-09-10 | Configuration Walkthrough | Technical Operations | Linux Environment |
| 2026-09-11 | HR Process Interview | HR Manager | Virtual |
| 2026-09-11 | Access and Authentication Review | Cloud Infrastructure Lead | Virtual |
| 2026-09-11 | Evidence Consolidation | Audit Team | Internal Workspace |
| 2026-09-12 | Finding Review | ISMS Coordinator | Virtual |
| 2026-09-12 | Closing Meeting | Management and Auditees | Virtual |

## Evidence Sources

Potential evidence includes:

- information security policies
- access-control procedures
- system configuration files
- authentication settings
- awareness records
- onboarding and termination procedures
- monitoring records
- incident-management documentation
- cloud governance documentation
- interview records
- walkthrough notes

## Audit Evidence Repository

Evidence collected during the audit is stored in:

    ~/isms_audit/evidence/

Findings are recorded in:

    ~/isms_audit/findings/

Reports are generated in:

    ~/isms_audit/reports/

## Resources

The audit uses:

- Annex A checklist:
      plan/annex_a_checklist.csv

- Interview templates:
      evidence/

- Technical evidence:
      evidence/

- Finding register:
      findings/nonconformity_register.csv

- Audit automation scripts:
      scripts/

- Final report repository:
      reports/

## Finding Classification

### Major Nonconformity

A significant failure of the ISMS, including:

- absence of a required process
- systemic control failure
- widespread breakdown in implementation
- failure that materially affects the ability of the ISMS to achieve intended outcomes

### Minor Nonconformity

A limited or isolated failure where:

- the process exists but is not fully implemented
- a specific control requirement is not consistently achieved
- the issue does not indicate systemic ISMS breakdown

### Observation

A condition that does not currently represent a formal nonconformity but may:

- reduce efficiency
- increase future risk
- indicate an opportunity for improvement

## Audit Deliverables

The audit will produce:

- internal audit plan
- Annex A checklist
- interview records
- technical walkthrough evidence
- nonconformity register
- corrective action plan
- final internal audit report
- PDF report

## Confidentiality

Audit evidence and findings may contain sensitive operational information.

Evidence should be handled according to organizational information-classification and access-control requirements.

## Audit Conclusion Method

The overall audit conclusion will consider:

- number and severity of findings
- evidence supporting selected controls
- degree of implementation
- consistency of ISMS processes
- corrective-action requirements

The audit conclusion will not be based solely on the number of checklist items marked as conforming.

## Follow-Up

Corrective actions identified during the audit must:

- have an accountable owner
- include a target completion date
- have a defined status
- be supported by closure evidence
- be reviewed for effectiveness before formal closure
