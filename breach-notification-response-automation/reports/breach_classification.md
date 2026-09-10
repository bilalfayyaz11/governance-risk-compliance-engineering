# Breach Risk Classification

## Incident Summary

Affected subjects observed in alert evidence: 4

Maximum records reported in a bulk export: 650

Primary Wazuh breach alerts: 4

First seen: 2026-09-10T21:17:43.961000+00:00

Last seen: 2026-09-10T21:17:47.961000+00:00

Observed exposure duration: 4 seconds

## Exposed Data Categories

- Email addresses
- Government-issued national identifiers

GDPR Article 9 special-category data detected: NO

The simulation contains contact information and government-issued identifiers. These are sensitive personal identifiers, but the evidence generated in this simulation does not include health, biometric, religious, political, sexual-orientation, or other Article 9 special-category data.

## Attack Vector

The Wazuh evidence indicates repeated unauthorized bulk GET requests against a sensitive customer export endpoint from the same external source.

Sensitive endpoint(s):

- /export/customers.csv

Source IP(s):

- 203.0.113.77

## Risk Score

Score: 9/10

Classification: HIGH

### Scoring Rationale

- Government-issued identifiers were exposed (+3)
- Contact identifiers were exposed (+1)
- Bulk export involved at least 500 records (+2)
- Unauthorized external-source access indicator present (+2)
- Repeated exfiltration activity detected (+1)

The score is an exercise-specific decision rubric rather than a statutory formula. It is used to consistently evaluate the nature of the data, scale of exposure, attack characteristics, and potential impact on individuals.

## GDPR Article 33 Decision

Supervisory authority notification required: **YES**

GDPR Article 33(1) requires notification unless the breach is unlikely to result in a risk to the rights and freedoms of natural persons.

This incident involves unauthorized bulk exposure of email addresses and government-issued identifiers. The combination creates credible risks including identity fraud, targeted phishing, impersonation, and misuse of government identifiers. It therefore cannot reasonably be characterized as unlikely to create risk.

## GDPR Article 34 Decision

Data subject notification required: **YES**

GDPR Article 34 applies when a personal data breach is likely to result in a high risk to individuals.

The simulated incident is classified HIGH because government identifiers were included in a bulk unauthorized export and repeated exfiltration indicators were detected. Direct notification is therefore appropriate under the exercise risk model.

## KSA PDPL Decision

Competent Authority notification required: **YES**

Data Subject notification required: **YES**

KSA PDPL Implementing Regulations Article 24 requires notification to the Competent Authority within 72 hours where a breach may harm personal data or the Data Subject or conflict with their rights or interests.

It also requires notification of affected Data Subjects without undue delay where the incident may cause damage to their data or prejudice their rights or interests.

The simulated exposure satisfies those thresholds because government identifiers and contact data were exposed through unauthorized bulk-access activity.

## Decision

This incident proceeds to both:

1. Supervisory / Competent Authority notification.
2. Data Subject notification.

The actual notification deadline is maintained separately from this analysis using the Wazuh detection timestamp recorded as T0.
