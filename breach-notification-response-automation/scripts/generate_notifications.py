#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ANALYSIS_PATH = BASE_DIR / "breach_analysis_output.json"
T0_PATH = BASE_DIR / "evidence" / "detection_t0.txt"
DEADLINE_PATH = BASE_DIR / "evidence" / "notification_deadline.txt"

AUTHORITY_OUTPUT = (
    BASE_DIR
    / "notifications"
    / "supervisory_authority_notification.md"
)

SUBJECT_OUTPUT = (
    BASE_DIR
    / "notifications"
    / "data_subject_notification.md"
)

COMPLIANCE_OUTPUT = (
    BASE_DIR
    / "notifications"
    / "deadline_compliance_statement.md"
)


def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(
        value.strip().replace("Z", "+00:00")
    )


def yes_no(value: bool) -> str:
    return "YES" if value else "NO"


analysis = json.loads(
    ANALYSIS_PATH.read_text(encoding="utf-8")
)

t0_raw = T0_PATH.read_text(
    encoding="utf-8"
).strip()

deadline_raw = DEADLINE_PATH.read_text(
    encoding="utf-8"
).strip()

t0 = parse_datetime(t0_raw)
deadline = parse_datetime(deadline_raw)

draft_time = datetime.now(timezone.utc)

deadline_met = draft_time <= deadline

affected_subjects = analysis[
    "affected_subjects_count"
]

max_records = analysis[
    "maximum_reported_records_per_export"
]

risk_score = analysis["risk_score"]
risk_level = analysis["risk_level"]

first_seen = analysis["first_seen"]
last_seen = analysis["last_seen"]

categories = analysis["data_categories"]

source_ips = analysis["source_ips"]
endpoints = analysis["sensitive_endpoints"]

authority_required = analysis[
    "supervisory_authority_notification_required"
]

subject_required = analysis[
    "data_subject_notification_required"
]

categories_md = "\n".join(
    f"- {item}"
    for item in categories
)

source_ips_md = "\n".join(
    f"- {item}"
    for item in source_ips
)

endpoints_md = "\n".join(
    f"- {item}"
    for item in endpoints
)

status = "MET" if deadline_met else "MISSED"

authority_document = f"""# Supervisory Authority Breach Notification

## Notification Status

Notification required: **{yes_no(authority_required)}**

Detection timestamp (T0): **{t0.isoformat()}**

72-hour notification deadline: **{deadline.isoformat()}**

Draft prepared: **{draft_time.isoformat()}**

Simulated deadline status: **{status}**

## 1. Nature of the Personal Data Breach

A security monitoring rule detected repeated unauthorized bulk access to a customer export endpoint.

Observed sensitive endpoint(s):

{endpoints_md}

Observed source IP address(es):

{source_ips_md}

The activity was detected through custom Wazuh rules designed to identify high-volume exports containing personal identifiers.

The evidence indicates repeated retrieval of customer information containing email addresses and government-issued national identifiers.

Observed activity window:

- First seen: {first_seen}
- Last seen: {last_seen}

## 2. Categories and Approximate Number of Data Subjects and Records

Unique affected data subjects directly observed in the alert evidence:

**{affected_subjects}**

Maximum records reported in an individual bulk export event:

**{max_records}**

Exposed data categories:

{categories_md}

No GDPR Article 9 special-category data was identified in the simulated evidence.

The record count represents the quantity reported by the bulk-export event, while the affected-subject count represents unique identifiers directly observable in the available SIEM evidence.

## 3. Contact Point

Data Protection / Incident Response Contact:

**Privacy and Security Response Team**

Contact channel:

**privacy-response@example.com**

This address is a placeholder for the simulation and must be replaced by the organization's actual Data Protection Officer or designated privacy contact in production.

## 4. Likely Consequences

Potential consequences include:

- Identity fraud or attempted impersonation
- Targeted phishing and social-engineering attacks
- Misuse of government-issued identifiers
- Correlation of identity and contact information
- Unauthorized profiling or secondary use of exposed data
- Increased risk of account takeover attempts

The combination of government identifiers and contact information increases the potential impact on affected individuals.

## 5. Measures Taken or Proposed

Immediate and proposed measures include:

- Detection and validation of the suspicious export activity through Wazuh
- Preservation of relevant SIEM alerts and source logs
- Identification of the source address and targeted endpoint
- Classification of exposed data categories
- Establishment of a formal detection timestamp and notification deadline
- Restriction and review of access to sensitive export functionality
- Review of authentication and authorization controls
- Expansion of monitoring coverage for sensitive export operations
- Investigation of potentially affected accounts and systems
- Review of audit logging and data-classification coverage

## 6. Risk Assessment

Exercise risk score: **{risk_score}/10**

Risk classification: **{risk_level}**

The incident was classified as reportable because unauthorized disclosure of government identifiers and contact information creates a credible risk to the rights and freedoms of affected individuals.

## 7. Regulatory Basis

Under GDPR Article 33, notification to the competent supervisory authority is required unless the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons.

The simulated incident does not meet that exception because sensitive identity information was exposed through repeated unauthorized bulk export activity.

The exercise also treats the event as notifiable under the Saudi PDPL breach-notification framework because the incident may cause harm to personal data or prejudice the rights or interests of Data Subjects.

## 8. Notification Timing

Detection T0:

**{t0.isoformat()}**

72-hour deadline:

**{deadline.isoformat()}**

Draft completion:

**{draft_time.isoformat()}**

Deadline status:

**{status}**

This exercise therefore records the notification preparation as **{status}** relative to the calculated 72-hour deadline.
"""

subject_document = f"""# Data Subject Breach Notification

## Important Notice About Your Personal Information

We identified unauthorized activity involving a system used to export customer information.

Our monitoring detected the activity at:

**{t0.isoformat()}**

## What Happened

Our security monitoring detected repeated unauthorized bulk requests to a customer-data export function.

We investigated the alerts and determined that personal information may have been exposed.

## What Information Was Involved

The affected information may include:

{categories_md}

The available evidence did not indicate that health, biometric, religious, political, or other GDPR Article 9 special-category information was involved.

## What This Could Mean for You

Because contact information and government-issued identifiers may have been exposed, there is a risk that the information could be used for:

- Identity fraud
- Impersonation
- Targeted phishing
- Social-engineering attempts
- Attempts to access accounts using known personal information

## What We Are Doing

We have:

- Investigated and preserved the security alerts
- Reviewed the affected export activity
- Identified the categories of information involved
- Strengthened monitoring around sensitive-data exports
- Begun reviewing access controls and authorization for export functions
- Started the formal incident-response and regulatory-notification process

Additional remediation will be prioritized based on the investigation findings.

## What You Should Do

You should remain alert for suspicious emails, messages, calls, or account-access attempts that reference your identity or personal information.

Do not provide passwords, verification codes, or other authentication information in response to unsolicited communications.

Where appropriate, monitor accounts associated with the affected information and report suspicious activity through the organization's official support or privacy channels.

## Contact

For questions about this incident, contact:

**Privacy and Security Response Team**

**privacy-response@example.com**

This contact address is a simulation placeholder and would be replaced by the organization's real privacy contact in production.

## Notification Decision

Data Subject notification required: **{yes_no(subject_required)}**

The simulated incident was classified **{risk_level}** with a risk score of **{risk_score}/10** because unauthorized bulk exposure involved government-issued identifiers and contact information.

The direct notification is therefore issued under the exercise's GDPR Article 34 high-risk determination.
"""

compliance_document = f"""# 72-Hour Notification Deadline Compliance

## Detection Time

T0:

**{t0.isoformat()}**

T0 is derived directly from the first qualifying Wazuh rule 100100 alert.

## Calculated Deadline

T0 + 72 hours:

**{deadline.isoformat()}**

## Notification Preparation Time

Drafts generated:

**{draft_time.isoformat()}**

## Compliance Result

**{status}**

The notification documents were generated {"before" if deadline_met else "after"} the calculated 72-hour supervisory-authority notification deadline.

Supervisory authority notification required:

**{yes_no(authority_required)}**

Data Subject notification required:

**{yes_no(subject_required)}**

## Important Timing Distinction

The GDPR 72-hour period applies to supervisory-authority notification under Article 33 following awareness of a qualifying breach.

Article 34 requires communication to affected individuals without undue delay when the breach is likely to result in a high risk to their rights and freedoms.

Accordingly, the 72-hour calculation is tracked as the authority-notification deadline, while Data Subject notification is separately evaluated against the without-undue-delay requirement.
"""

AUTHORITY_OUTPUT.write_text(
    authority_document,
    encoding="utf-8"
)

SUBJECT_OUTPUT.write_text(
    subject_document,
    encoding="utf-8"
)

COMPLIANCE_OUTPUT.write_text(
    compliance_document,
    encoding="utf-8"
)

print(
    f"Authority notification: {AUTHORITY_OUTPUT}"
)

print(
    f"Data Subject notification: {SUBJECT_OUTPUT}"
)

print(
    f"Deadline statement: {COMPLIANCE_OUTPUT}"
)

print()
print(f"T0: {t0.isoformat()}")
print(f"Deadline: {deadline.isoformat()}")
print(f"Draft time: {draft_time.isoformat()}")
print(f"Status: {status}")
