# Security Assessment Plan

## 1. Scope

- Target system: ip-172-31-10-5 (172.31.10.5)
- Operating system: Ubuntu 24.04.3 LTS
- Assessment baseline: xccdf_org.ssgproject.content_profile_stig
- SCAP datastream: ssg-ubuntu2404-ds.xml
- Assessment type: Automated technical security control assessment
- Assessment engine: OpenSCAP

## 2. Objectives

The purpose of this assessment is to evaluate the target Linux workload against the selected STIG-aligned security baseline and determine whether applicable technical security requirements are implemented correctly.

The assessment will identify configuration deficiencies, document their security significance, establish remediation actions, and provide repeatable evidence supporting security control assessment activities.

## 3. Methodology

The assessment uses OpenSCAP to perform an automated XCCDF compliance evaluation against the selected SCAP Security Guide profile.

The assessment process consists of:

1. Establishing the authorized assessment scope and baseline.
2. Executing an initial OpenSCAP XCCDF evaluation.
3. Preserving machine-readable XML and human-readable HTML results.
4. Identifying and triaging failed security rules.
5. Assigning risk and remediation actions to selected findings.
6. Implementing low-risk corrective actions where appropriate.
7. Performing a follow-up assessment to verify remediation effectiveness.
8. Consolidating assessment evidence and conclusions into a Security Assessment Report.

Assessment artifacts will be retained under the scap-assessment workspace to provide reproducible evidence of the assessment process.

## 4. Roles and Responsibilities

### Assessor

Bilal Fayyaz

Responsibilities:

- Define assessment scope and methodology.
- Execute automated technical control tests.
- Analyze assessment results.
- Document findings and remediation recommendations.
- Validate selected corrective actions.
- Produce the Security Assessment Report.

### System Owner

Linux Workload Operations Team

Responsibilities:

- Maintain operational responsibility for the assessed workload.
- Review identified security deficiencies.
- Approve or coordinate remediation activities.
- Track unresolved deficiencies through appropriate risk-management processes.

## 5. Assessor Independence Statement

The assessor performing this security control assessment has no operational ownership or administrative responsibility for the target system being evaluated within the assessment scenario. Assessment conclusions will be based on reproducible technical evidence generated through the defined methodology, without responsibility for the implementation or ongoing operation of the assessed controls.

No conflict of interest has been identified that would prevent an objective evaluation of the selected security baseline.

## 6. Assessment Evidence

The assessment is expected to produce the following evidence:

- Initial OpenSCAP XCCDF results
- Initial human-readable assessment report
- Finding triage records
- Documented remediation actions
- Follow-up OpenSCAP results
- Follow-up human-readable report
- Security Assessment Report

## 7. Schedule

- Planned assessment start: 2026-09-07 14:36:28 UTC
- Planned assessment end: 2026-09-07 16:36:28 UTC

## 8. Assessment Constraints

Automated SCAP testing evaluates machine-verifiable configuration requirements and does not independently establish the effectiveness of organizational, procedural, or non-automatable controls.

Remediation will be limited to findings that can be safely modified within the assessment environment without creating unnecessary availability or remote-access risk.

## 9. Authorization to Proceed

This assessment plan establishes the scope, baseline, methodology, responsibilities, evidence requirements, and independence conditions that govern the technical security assessment.

The automated assessment may proceed after verification that the selected datastream and profile are available on the target system.
