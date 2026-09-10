# Supervisory Authority Breach Notification

## Notification Status

Notification required: **YES**

Detection timestamp (T0): **2026-09-10T21:17:43.961000+00:00**

72-hour notification deadline: **2026-09-13T21:17:43.961000+00:00**

Draft prepared: **2026-09-10T21:19:47.746725+00:00**

Simulated deadline status: **MET**

## 1. Nature of the Personal Data Breach

A security monitoring rule detected repeated unauthorized bulk access to a customer export endpoint.

Observed sensitive endpoint(s):

- /export/customers.csv

Observed source IP address(es):

- 203.0.113.77

The activity was detected through custom Wazuh rules designed to identify high-volume exports containing personal identifiers.

The evidence indicates repeated retrieval of customer information containing email addresses and government-issued national identifiers.

Observed activity window:

- First seen: 2026-09-10T21:17:43.961000+00:00
- Last seen: 2026-09-10T21:17:47.961000+00:00

## 2. Categories and Approximate Number of Data Subjects and Records

Unique affected data subjects directly observed in the alert evidence:

**4**

Maximum records reported in an individual bulk export event:

**650**

Exposed data categories:

- Email addresses
- Government-issued national identifiers

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

Exercise risk score: **9/10**

Risk classification: **HIGH**

The incident was classified as reportable because unauthorized disclosure of government identifiers and contact information creates a credible risk to the rights and freedoms of affected individuals.

## 7. Regulatory Basis

Under GDPR Article 33, notification to the competent supervisory authority is required unless the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons.

The simulated incident does not meet that exception because sensitive identity information was exposed through repeated unauthorized bulk export activity.

The exercise also treats the event as notifiable under the Saudi PDPL breach-notification framework because the incident may cause harm to personal data or prejudice the rights or interests of Data Subjects.

## 8. Notification Timing

Detection T0:

**2026-09-10T21:17:43.961000+00:00**

72-hour deadline:

**2026-09-13T21:17:43.961000+00:00**

Draft completion:

**2026-09-10T21:19:47.746725+00:00**

Deadline status:

**MET**

This exercise therefore records the notification preparation as **MET** relative to the calculated 72-hour deadline.
