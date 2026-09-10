# Breach Detection and 72-Hour Notification Response Automation

## What This Does

This implementation automates the technical and operational response to a simulated personal-data breach using Wazuh SIEM, Python, and evidence-backed regulatory workflows.

A custom Wazuh decoder and rule set detects unauthorized bulk exports containing personal identifiers, records the actual SIEM detection timestamp as T0, calculates the 72-hour notification deadline, analyzes breach impact, determines regulator and data-subject notification requirements, generates notification drafts, and produces an incident after-action report.

The workflow demonstrates how security detection, incident response, privacy operations, and regulatory notification processes can operate from the same structured evidence.

## Architecture

~~text
                     Simulated Breach Activity
                              |
                              v
                  +---------------------------+
                  |   Mock Application Log    |
                  |                           |
                  | /var/log/mock-app/        |
                  | access.log                |
                  +-------------+-------------+
                                |
                                v
                  +---------------------------+
                  |       Wazuh Manager       |
                  |                           |
                  | Log Collector             |
                  | Custom Decoder            |
                  | Custom Rules              |
                  +-------------+-------------+
                                |
                  +-------------+-------------+
                  |                           |
                  v                           v
          Rule 100100                 Rule 100101
      Bulk PII Exposure            Correlated Activity
          Level 13                     Level 15
                  |                           |
                  +-------------+-------------+
                                |
                                v
                  +---------------------------+
                  |       alerts.json         |
                  |   Evidence / Detection    |
                  +-------------+-------------+
                                |
                                v
                  +---------------------------+
                  |         Detection T0      |
                  |   72-Hour Clock Start     |
                  +-------------+-------------+
                                |
                                v
                  +---------------------------+
                  |   Breach Analysis Engine  |
                  |                           |
                  | Subject Deduplication     |
                  | Data Classification       |
                  | Exposure Window           |
                  | Risk Scoring              |
                  +-------------+-------------+
                                |
                  +-------------+-------------+
                  |                           |
                  v                           v
        Authority Notification      Data Subject Notification
                  |                           |
                  +-------------+-------------+
                                |
                                v
                  +---------------------------+
                  |    After-Action Review    |
                  |                           |
                  | Timeline                  |
                  | Detection Gaps            |
                  | Remediation Plan          |
                  +---------------------------+
~~

## Prerequisites

- Ubuntu 22.04+ or equivalent Linux environment
- Python 3
- Git
- jq
- curl
- wget
- OpenSSL
- sudo/root privileges
- Native Wazuh Manager
- systemd
- Sufficient resources for the Wazuh Manager

The full Wazuh Docker stack is not required for this implementation.

## Setup & Installation

Add the Wazuh repository and install the native manager:

~~bash
sudo apt update

sudo apt install -y \
  gnupg \
  apt-transport-https \
  ca-certificates

curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH \
| sudo gpg --no-default-keyring \
  --keyring gnupg-ring:/usr/share/keyrings/wazuh.gpg \
  --import

sudo chmod 644 /usr/share/keyrings/wazuh.gpg

echo "deb [signed-by=/usr/share/keyrings/wazuh.gpg] https://packages.wazuh.com/4.x/apt/ stable main" \
| sudo tee /etc/apt/sources.list.d/wazuh.list >/dev/null

sudo apt update
sudo apt install -y wazuh-manager

sudo systemctl enable --now wazuh-manager
~~

Verify:

~~bash
sudo systemctl is-active wazuh-manager
sudo /var/ossec/bin/wazuh-control info
sudo /var/ossec/bin/wazuh-control status || true
~~

## How to Reproduce

### 1. Prepare the Mock Log Source

~~bash
sudo mkdir -p /var/log/mock-app
sudo touch /var/log/mock-app/access.log
sudo chown ubuntu:ubuntu /var/log/mock-app/access.log
sudo chmod 640 /var/log/mock-app/access.log
~~

Configure Wazuh log collection in `/var/ossec/etc/ossec.conf`:

~~xml
<localfile>
  <location>/var/log/mock-app/access.log</location>
  <log_format>syslog</log_format>
</localfile>
~~

Restart the manager after configuration changes:

~~bash
sudo systemctl daemon-reload
sudo systemctl restart wazuh-manager
~~

### 2. Configure the Custom Decoder

Custom decoder:

~~xml
<decoder name="mock-breach">
  <prematch type="pcre2">^MOCKAPP </prematch>
</decoder>

<decoder name="mock-breach-fields">
  <parent>mock-breach</parent>
  <regex type="pcre2">^MOCKAPP src_ip=(\S+) method=(GET|POST) endpoint=(\S+) records=(\d+) email=(\S+) national_id=(\S+) session=(\S+)</regex>
  <order>srcip,method,endpoint,records,email,national_id,session</order>
</decoder>
~~

The decoder extracts:

- Source IP
- HTTP method
- Sensitive endpoint
- Export record count
- Email address
- National identifier
- Session ID

### 3. Configure Custom Wazuh Rules

Primary breach indicator:

~~xml
<rule id="100100" level="13">
  <if_sid>100099</if_sid>

  <field name="endpoint" type="pcre2">^/export/(customers|users|accounts)\.csv$</field>

  <field name="records" type="pcre2">^(?:5\d\d|[6-9]\d\d|[1-9]\d{3,})$</field>

  <field name="email" type="pcre2">^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$</field>

  <field name="national_id" type="pcre2">^784-\d{4}-\d{7}-\d$</field>

  <description>Potential personal data breach: bulk export of PII from sensitive endpoint.</description>

  <group>pii_exposure,data_exfiltration,gdpr_breach_indicator,</group>
</rule>
~~

Correlated escalation rule:

~~xml
<rule id="100101" level="15" frequency="3" timeframe="60">
  <if_matched_sid>100100</if_matched_sid>
  <same_srcip />

  <description>Critical breach indicator: repeated bulk PII exports from the same source.</description>

  <group>pii_exposure,data_exfiltration,correlated_breach,</group>
</rule>
~~

Validate the rules:

~~bash
sudo /var/ossec/bin/wazuh-analysisd -t
~~

### 4. Generate Simulated Breach Activity

Run:

~~bash
python3 scripts/generate_breach.py
~~

The generator writes repeated security events containing:

- Sensitive export endpoint
- More than 500 exported records
- Email addresses
- Government-issued identifiers
- External source IP
- Shared exfiltration session

Example structure:

~~text
MOCKAPP src_ip=203.0.113.77 method=GET endpoint=/export/customers.csv records=650 email=ahmed.mansoori@example.com national_id=784-1990-1234567-1 session=exfil-session-001
~~

### 5. Validate Detection

Test the rule interactively:

~~bash
printf '%s\n' \
'MOCKAPP src_ip=203.0.113.77 method=GET endpoint=/export/customers.csv records=650 email=ahmed.mansoori@example.com national_id=784-1990-1234567-1 session=exfil-session-001' \
| sudo /var/ossec/bin/wazuh-logtest
~~

Search generated alerts:

~~bash
sudo jq -c \
'select(.rule.id=="100100" or .rule.id=="100101")' \
/var/ossec/logs/alerts/alerts.json
~~

### 6. Establish Detection T0

The first qualifying Wazuh alert timestamp is treated as T0.

Conceptually:

~~text
First Rule 100100 Alert
        |
        v
Detection / Awareness T0
        |
        v
T0 + 72 Hours
        |
        v
Authority Notification Deadline
~~

The workflow stores:

~~text
evidence/detection_t0.txt
evidence/notification_deadline.txt
~~

This ensures the notification clock is based on actual SIEM evidence rather than manually entered timestamps.

### 7. Preserve Breach Evidence

The implementation preserves:

~~text
evidence/
├── breach_alerts_raw.jsonl
├── detection_t0.txt
├── notification_deadline.txt
├── local_decoder.xml
├── local_rules.xml
├── mock_access.log
├── rule_100100_alerts.jsonl
├── rule_100101_alerts.jsonl
└── t0_note.md
~~

These artifacts provide the technical evidence supporting the incident timeline and regulatory decisions.

### 8. Analyze Breach Impact

Run:

~~bash
python3 scripts/analyze_breach.py
~~

The analysis engine:

- Parses Wazuh JSONL alerts
- Deduplicates affected subjects
- Counts observed email addresses
- Counts government-issued identifiers
- Identifies affected data categories
- Calculates first-seen and last-seen timestamps
- Calculates observed exposure duration
- Identifies attack source IPs
- Records targeted endpoints
- Scores breach risk
- Determines notification requirements

Outputs:

~~text
breach_analysis_output.json
reports/breach_classification.md
~~

### 9. Risk Classification

The implementation uses a documented exercise-specific risk rubric.

Example scoring factors include:

~~text
Government-issued identifiers exposed       +3
Email/contact identifiers exposed            +1
Bulk export >= 500 records                   +2
Unauthorized external source detected        +2
Repeated exfiltration activity               +1
Special-category data if present             +1
~~

Risk levels:

~~text
0-3   LOW
4-6   MEDIUM
7-10  HIGH
~~

The scoring model is decision support and is not represented as a statutory formula.

### 10. Regulatory Notification Decision

For GDPR:

- Article 33 authority notification is evaluated against the risk-to-rights-and-freedoms threshold.
- Article 34 individual communication is evaluated against the higher high-risk threshold.

Government-issued identifiers are highly sensitive personal data but are not automatically GDPR Article 9 special-category data.

The simulated incident involves government identifiers, contact information, repeated unauthorized access, and bulk export activity, resulting in a high-risk classification.

### 11. Generate Notifications

Run:

~~bash
python3 scripts/generate_notifications.py
~~

Generated artifacts:

~~text
notifications/
├── supervisory_authority_notification.md
├── data_subject_notification.md
└── deadline_compliance_statement.md
~~

The authority notification includes:

- Nature of the breach
- Affected data categories
- Approximate number of affected subjects and records
- Contact point
- Likely consequences
- Mitigation measures
- T0
- 72-hour deadline
- Notification timing result

The Data Subject notification uses plain language and describes:

- What happened
- Information potentially exposed
- Potential consequences
- Measures being taken
- Actions affected individuals should consider
- Contact information

### 12. Verify the 72-Hour Deadline

The deadline is calculated as:

~~text
Authority Notification Deadline = T0 + 72 hours
~~

The workflow records whether notification preparation occurred before or after the calculated deadline.

The GDPR 72-hour deadline applies to supervisory-authority notification.

Where Article 34 applies, communication to affected individuals is required without undue delay rather than under the same fixed 72-hour deadline.

### 13. Generate the After-Action Report

Run:

~~bash
python3 scripts/generate_after_action.py
~~

The final report includes:

- Incident executive summary
- Evidence-based timeline
- Detection T0
- Risk-classification time
- Notification-drafting times
- 72-hour deadline
- What worked
- What failed
- Detection blind spots
- Process gaps
- Remediation owners and priorities
- Updated response recommendations
- Lessons learned

Output:

~~text
after_action_report.md
~~

## Tools Used

- Wazuh Manager
- Wazuh Log Collector
- Wazuh custom decoders
- Wazuh custom rules
- Wazuh correlation rules
- wazuh-logtest
- Python 3
- JSON / JSONL
- jq
- Linux
- systemd
- Bash
- Git

## Key Skills Demonstrated

- Designing custom SIEM detection logic
- Parsing structured security telemetry
- Detecting sensitive-data exfiltration
- Building frequency-based correlation rules
- Establishing incident T0 from SIEM evidence
- Preserving breach evidence
- Automating breach impact analysis
- Deduplicating affected Data Subjects
- Classifying exposed data categories
- Automating exposure-window calculations
- Designing repeatable incident-risk scoring
- Translating SIEM evidence into regulatory decisions
- Automating breach-notification deadlines
- Generating regulator-ready notifications
- Producing plain-language Data Subject communications
- Conducting incident after-action reviews
- Identifying detection blind spots
- Producing structured remediation plans

## Real-World Use Case

Security teams frequently detect suspicious behavior before privacy or compliance teams have enough structured information to determine regulatory obligations.

This workflow connects those functions by using SIEM evidence as the source for breach analysis, notification timing, risk classification, regulatory decision support, and post-incident review.

A production implementation could integrate SIEM telemetry with incident-management platforms, case-management systems, data catalogs, DLP platforms, identity providers, regulatory workflow systems, and legal-review processes.

## Lessons Learned

- Security detection and privacy-response teams benefit from using the same evidence-backed incident record.
- Regulatory deadlines should be calculated automatically from a documented awareness timestamp.
- Custom SIEM rules should combine behavioral signals with sensitive-data context rather than rely on a single indicator.
- Fixed record thresholds alone cannot reliably detect slow or distributed exfiltration.
- Plaintext PII should not be intentionally logged merely to make SIEM detection easier.
- Structured data-classification metadata is safer and more scalable than detecting raw identifiers in logs.
- Automated risk scoring improves consistency but does not replace qualified legal or privacy review.
- Notification documents should derive from a common incident record to reduce conflicting facts.
- Infrastructure capacity should be validated before selecting a SIEM deployment architecture.

## Troubleshooting Log

### Full Wazuh Docker Stack Exceeded Host Capacity

The original architecture proposed a Docker deployment containing the manager, indexer, and dashboard.

The available host had approximately:

~~text
2 CPU cores
7.7 GiB RAM
21 GiB available disk
~~

This was below the recommended sizing for the complete Wazuh Docker stack.

The architecture was therefore changed to a native Wazuh Manager.

This preserved:

- Log collection
- Decoding
- Detection rules
- Correlation
- Alert generation
- CLI validation
- alerts.json evidence

without introducing unnecessary indexer/dashboard resource pressure.

### Docker and systemd Architecture Mismatch

The original workflow mixed Docker-based Wazuh deployment with commands such as:

~~bash
systemctl status wazuh-manager
~~

Those administration models are inconsistent.

The implementation standardized the environment on a native Wazuh Manager, making `/var/ossec` and systemd management directly available on the host.

### Same-Host Agent Was Unnecessary

The exercise originally proposed deploying an agent on the same machine as the manager.

The native manager already provides log collection through `<localfile>`, so `/var/log/mock-app/access.log` can be monitored directly.

Removing the redundant agent simplified the architecture and reduced operational overhead.

### wazuh-logtest Permission Check

`/var/ossec/bin/wazuh-logtest` was installed with permissions allowing root and the Wazuh group to execute it.

The normal Ubuntu account could therefore not execute it directly.

The correct invocation is:

~~bash
sudo /var/ossec/bin/wazuh-logtest
~~

### systemd Unit Reload Warning

After package/configuration changes, systemd reported that the Wazuh service definition had changed on disk.

The warning was resolved with:

~~bash
sudo systemctl daemon-reload
~~

before restarting the manager.

### Global set -e Closed SSH Sessions

Some diagnostic blocks initially used:

~~bash
set -e
~~

and subsequently executed:

~~bash
sudo /var/ossec/bin/wazuh-control status
~~

Several optional Wazuh components are normally inactive in this standalone deployment.

The diagnostic command could therefore return a non-zero status even while critical Wazuh processes remained healthy.

With global fail-fast behavior enabled, the login shell exited and the SSH session closed.

The corrected approach explicitly tolerates diagnostic non-zero results:

~~bash
sudo /var/ossec/bin/wazuh-control status || true
~~

and handles actual failures individually.

### Optional Wazuh Components Not Running

The standalone manager reported components such as:

~~text
wazuh-clusterd
wazuh-maild
wazuh-agentlessd
wazuh-integratord
wazuh-csyslogd
~~

as inactive.

These were not required for the implemented detection workflow.

Critical components including:

~~text
wazuh-analysisd
wazuh-logcollector
wazuh-remoted
wazuh-syscheckd
wazuh-execd
wazuh-db
wazuh-authd
wazuh-apid
~~

remained operational.

### PII Detection Visibility

The simulation includes personal identifiers inside log events so the custom decoder and rules can demonstrate detection.

Production applications should not intentionally write complete sensitive identifiers into logs.

A stronger design would log structured security metadata such as:

~~text
contains_pii=true
data_classification=restricted
records_exported=650
export_category=customer_identity
~~

and combine it with application, DLP, and access-control telemetry.

## Detection Gaps Identified

### Sensitive Endpoint Coverage

The custom rule covers a defined set of export paths.

Applications with alternative API endpoints, background export jobs, GraphQL operations, or internal services could bypass endpoint-specific detection.

### Slow Exfiltration

An attacker could intentionally export fewer than 500 records per request.

Production detection should aggregate export volumes across longer time windows and multiple sessions.

### Identity Context

The simulation does not include full authenticated-user context, MFA status, authorization decision, device posture, or role information.

Those signals would significantly improve attribution and insider-threat detection.

### Data Classification

The detection currently relies partly on raw PII patterns.

Production SIEM events should use structured classification labels and integrate with DLP or data-governance tooling.

### Human Regulatory Review

Automated breach scoring can support decisions but cannot capture every legal, jurisdictional, and contextual factor.

Final notification decisions should include appropriate privacy/legal review and auditable approval.

## Compliance Mapping

### GDPR Article 33

The workflow establishes a traceable detection timestamp and calculates the 72-hour authority-notification deadline.

It also produces the information required to support authority notification, including breach nature, affected-person estimates, likely consequences, and mitigation actions.

### GDPR Article 34

The workflow separately evaluates whether the breach is likely to result in a high risk to affected individuals.

Where that threshold is met, a plain-language communication is generated for impacted Data Subjects.

### GCC Privacy Requirements

The incident-classification workflow can be adapted to applicable GCC privacy regimes by replacing or extending the jurisdiction-specific notification thresholds and timelines.

The implementation demonstrates how jurisdiction rules can be layered on top of a common technical incident record.

## Production Improvements

A production implementation should additionally:

- Deploy a properly sized Wazuh indexer/dashboard architecture
- Centralize security telemetry across multiple hosts
- Add authentication and authorization context
- Integrate DLP and data-classification platforms
- Correlate cumulative export activity
- Detect slow and distributed exfiltration
- Integrate incident-management tooling
- Add immutable evidence preservation
- Add qualified legal/privacy approval workflows
- Track actual notification submission timestamps
- Maintain jurisdiction-specific notification matrices
- Protect SIEM logs against unauthorized modification
- Automate remediation tracking through closure
