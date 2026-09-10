# Incident Response After-Action Report

## Executive Summary

A simulated personal-data breach was generated against a sensitive customer export workflow and detected by custom Wazuh rules.

The event involved repeated bulk access to an export endpoint containing email addresses and government-issued national identifiers. The detection triggered a structured breach-response workflow covering evidence preservation, impact analysis, regulatory classification, notification drafting, and post-incident review.

Exercise risk score: **9/10**

Risk classification: **HIGH**

Observed affected subjects: **4**

Maximum records reported in a bulk export event: **650**

Supervisory Authority notification required: **YES**

Data Subject notification required: **YES**

## Incident Timeline

| Phase | Timestamp | Activity |
|---|---|---|
| First observed malicious activity | 2026-09-10T21:17:43.961000+00:00 | Initial suspicious bulk PII export activity observed |
| Last observed malicious activity | 2026-09-10T21:17:47.961000+00:00 | Last qualifying event in the observed exposure window |
| Detection / T0 | 2026-09-10T21:17:43.961+0000 | Wazuh rule 100100 generated a qualifying breach indicator |
| Risk classification completed | 2026-09-10T21:18:56.985345+00:00 | Alert evidence analyzed and regulatory risk determination produced |
| Authority notification drafted | 2026-09-10T21:19:47.746931+00:00 | Supervisory authority notification prepared |
| Data Subject notification drafted | 2026-09-10T21:19:47.747051+00:00 | Plain-language affected-individual notification prepared |
| 72-hour authority deadline | 2026-09-13T21:17:43.961000+00:00 | Calculated regulatory notification deadline |
| After-action review completed | 2026-09-10T21:20:55.398030+00:00 | Tabletop review and remediation plan documented |

## Detection and Response Flow

~~text
Mock Export Activity
        |
        v
Application Log
        |
        v
Wazuh Log Collector
        |
        v
Custom Decoder
        |
        v
Rule 100100
Bulk PII Exposure
        |
        +------------------+
        |                  |
        v                  v
Rule 100101           Detection T0
Correlation               |
                           v
                  Breach Impact Analysis
                           |
                           v
                  Regulatory Decision
                       /       \
                      /         \
                     v           v
             Authority Notice  Subject Notice
                      \         /
                       \       /
                        v     v
                    After-Action
                       Review
~~

## What Worked

### 1. Deterministic Detection

The custom Wazuh decoder successfully extracted structured fields including source IP, export endpoint, record count, email address, national identifier, and session information.

Rule 100100 reliably identified bulk PII-export activity and established a reproducible breach-detection signal.

### 2. Severity Escalation

The detection model assigned a high rule severity to bulk exposure involving both personal contact information and government identifiers.

Repeated activity from the same source could additionally be correlated through rule 100101, providing escalation beyond a single isolated request.

### 3. Evidence-Based T0

The breach-notification clock was based on the actual Wazuh alert timestamp rather than a manually entered simulation time.

This creates a more defensible incident timeline because the notification deadline can be traced directly to security-monitoring evidence.

### 4. Automated Impact Analysis

The breach-analysis script automatically:

- Deduplicated observed Data Subjects
- Identified exposed data categories
- Identified first-seen and last-seen times
- Calculated exposure duration
- Classified the breach using a documented risk rubric
- Determined supervisory-authority notification requirements
- Determined Data Subject notification requirements

### 5. Notification Generation

Both supervisory-authority and Data Subject notifications were generated from the same structured incident evidence.

This reduced the risk of inconsistent timestamps, affected-person counts, risk classifications, or breach descriptions appearing across separate response documents.

## What Failed or Required Correction

### 1. Infrastructure Sizing Did Not Support the Original Architecture

The initial specification proposed a complete Docker-based Wazuh deployment with manager, indexer, and dashboard components.

The available machine had only two CPU cores, approximately 8 GB RAM, and significantly less disk capacity than recommended for the full stack.

The deployment was therefore redesigned around a native Wazuh Manager with CLI-based alert validation.

### 2. Wazuh Service Model Was Inconsistent

The original instructions mixed Docker-manager administration with host-level systemd commands.

A Docker-based manager would require container administration, while a native manager uses systemd and direct `/var/ossec` paths.

The exercise was standardized on the native manager architecture.

### 3. Shell Error Handling Terminated SSH Sessions

Some command blocks initially used global:

~~bash
set -e
~~

while running diagnostic Wazuh status commands.

`wazuh-control status` can return non-zero when optional components are not running, even when the core manager is healthy.

The global shell-exit behavior caused the SSH login shell to terminate unexpectedly.

The remediation was to handle expected non-zero diagnostic commands explicitly rather than applying global fail-fast behavior to the entire session.

## Detection and Process Gaps

### Gap 1 — Limited Sensitive Endpoint Coverage

The detection logic currently focuses on a small set of export endpoint patterns.

An attacker using a different export path, API version, GraphQL operation, asynchronous job, or internal service endpoint may bypass this detection.

**Remediation:**

- Maintain an inventory of sensitive data-export functions.
- Build rules from data classification rather than endpoint names alone.
- Add API gateway, application, and database telemetry.
- Review rule coverage after application releases.

### Gap 2 — PII Detection Depends on Log Visibility

The rule detects personal information only when identifiers appear directly in the monitored log event.

Production systems should generally avoid logging complete sensitive identifiers, so relying on plaintext PII patterns creates a detection blind spot.

**Remediation:**

- Generate structured security metadata such as `contains_pii=true`.
- Tag sensitive datasets and export operations.
- Send classification labels rather than full identifiers into SIEM.
- Integrate DLP or data-access monitoring where appropriate.

### Gap 3 — Static Record Threshold

The current detection uses a fixed bulk-export threshold of approximately 500 records.

A slow attacker could intentionally remain below the threshold while extracting significant data across a longer time window.

**Remediation:**

- Add rolling per-user and per-source aggregation.
- Correlate activity across longer windows.
- Detect unusual export behavior relative to historical baselines.
- Track cumulative records exported per identity/session.

### Gap 4 — Limited Identity Context

The simulated log captures source IP and session information but lacks authenticated user identity, role, device, MFA status, and authorization outcome.

This limits attribution and makes insider misuse harder to distinguish from external compromise.

**Remediation:**

- Include user and service identity in structured logs.
- Integrate identity-provider authentication events.
- Include authorization decisions and assigned roles.
- Correlate suspicious export activity with login anomalies.

### Gap 5 — Manual Regulatory Decision Boundary

The risk score improves consistency but remains an internally defined exercise rubric rather than a statutory formula.

Different jurisdictions, data categories, vulnerable Data Subjects, or contextual harms may require legal/privacy review beyond automated scoring.

**Remediation:**

- Treat automated scoring as decision support.
- Define escalation thresholds for DPO/legal review.
- Maintain jurisdiction-specific breach decision matrices.
- Record human approval and rationale for notification decisions.

## Remediation Plan

| Priority | Remediation | Owner | Target |
|---|---|---|---|
| Critical | Expand monitoring across all sensitive export mechanisms | Security Engineering | Immediate |
| Critical | Add authenticated user and authorization context to security logs | Application / IAM Engineering | Immediate |
| High | Implement cumulative export-volume correlation | Detection Engineering | 30 days |
| High | Introduce structured data-classification metadata | Data Governance / Engineering | 30 days |
| High | Integrate DLP or sensitive-data access telemetry | Security Engineering | 60 days |
| Medium | Develop jurisdiction-specific notification decision matrices | Privacy / Legal | 60 days |
| Medium | Automate incident evidence preservation | Incident Response | 60 days |
| Medium | Add immutable reidentification and privileged-access audit trails | Security / Platform | 90 days |

## Updated Playbook Recommendations

The breach-response process should follow this sequence:

1. Detect suspicious access through SIEM and application telemetry.
2. Preserve raw alerts and supporting source logs immediately.
3. Establish T0 using documented organizational awareness criteria.
4. Identify affected systems, Data Subjects, and categories of information.
5. Determine whether special-category or otherwise highly sensitive information is involved.
6. Assess likely harm to individuals.
7. Determine notification obligations for each applicable jurisdiction.
8. Calculate regulatory deadlines automatically.
9. Escalate notification decisions to the appropriate privacy/legal authority.
10. Draft notifications from a common structured incident record.
11. Record notification submission timestamps and evidence.
12. Continue investigation and issue supplemental notifications if material facts change.
13. Conduct a formal after-action review.
14. Track remediation actions through closure.

## Regulatory Timing Assessment

Detection T0:

**2026-09-10T21:17:43.961+0000**

Supervisory-authority notification deadline:

**2026-09-13T21:17:43.961000+00:00**

The exercise generated the required regulatory-notification artifacts during the simulated response window.

The 72-hour calculation applies to the GDPR Article 33 supervisory-authority notification requirement.

Where the high-risk threshold is met, communication to Data Subjects should occur without undue delay under GDPR Article 34.

## Lessons Learned

- Detection engineering and privacy incident response should operate from the same structured evidence.
- Regulatory deadlines should be calculated automatically from an evidence-backed awareness timestamp.
- Infrastructure constraints should be assessed before selecting a SIEM deployment architecture.
- Detection rules should rely increasingly on structured security and data-classification metadata rather than plaintext PII appearing in logs.
- Volume thresholds alone are insufficient for identifying slow or distributed data exfiltration.
- Fail-fast shell behavior should not be applied blindly to diagnostic commands that can legitimately return non-zero results.
- Automated risk scoring improves consistency but does not replace qualified privacy or legal review.
- Notification documents should be generated from a common incident record to reduce factual inconsistencies.

## Final Outcome

The exercise demonstrated an end-to-end breach-response workflow:

- Sensitive export activity was simulated.
- Custom Wazuh detection logic identified the activity.
- SIEM evidence established the breach-detection timestamp.
- A 72-hour notification deadline was calculated.
- Impact and affected Data Subjects were analyzed.
- Regulatory notification thresholds were assessed.
- Authority and Data Subject notifications were generated.
- Process gaps were identified.
- Corrective actions were documented through an after-action review.

The resulting workflow provides a reproducible foundation for combining security monitoring, privacy incident response, and regulatory breach-notification operations.
