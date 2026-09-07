# Continuous Security Monitoring and Governance Automation

A governance-focused continuous security monitoring implementation that combines Wazuh telemetry, configuration assessment, file integrity monitoring, drift detection, evidence preservation, and executive risk reporting.

The workflow demonstrates how operational security signals can be transformed into defensible governance evidence for continuous authorization, remediation tracking, control reassessment, and risk-based decision support.

## Architecture

    Monitored Linux System
            |
            | FIM / SCA / security telemetry
            v
       Wazuh Manager
            |
            +--------------------+
            |                    |
            v                    v
      Wazuh Indexer         Filebeat
            |
            v
      Wazuh Dashboard
            |
            v
    Governance Automation
            |
            +--> Control-effectiveness metrics
            +--> Configuration-drift detection
            +--> Evidence integrity
            +--> Monthly risk reporting
            +--> Authorization decision support

## Security Monitoring Capabilities

The implementation includes:

- Wazuh Manager, Indexer, Filebeat, and Dashboard
- File Integrity Monitoring
- CIS Ubuntu 24.04 Security Configuration Assessment
- security configuration baseline tracking
- automated configuration-drift detection
- platform health monitoring
- monitoring evidence collection
- control-effectiveness scoring
- governance reporting
- SHA-256 evidence integrity validation

## Continuous Monitoring Strategy

Monitoring frequencies are intentionally risk-based rather than relying only on product defaults.

| Monitoring Activity | Frequency |
|---|---|
| Security event monitoring | Continuous |
| Platform and agent availability | Hourly |
| File integrity monitoring | Every 6 hours |
| Security configuration assessment | Daily |
| Vulnerability review | Daily |
| Monitoring coverage review | Weekly |
| Risk and remediation review | Weekly |
| Executive continuous-monitoring report | Monthly |

## File Integrity Monitoring

The monitoring profile protects high-value operating system and security configuration locations, including:

    /etc
    /boot
    /usr/bin
    /usr/sbin
    /bin
    /sbin

A controlled security configuration area is also monitored for validation and evidence-generation purposes.

Sensitive files are excluded from content-difference reporting to reduce the risk of secrets or credentials appearing in monitoring evidence.

## Security Configuration Assessment

The environment uses the CIS Ubuntu 24.04 policy through Wazuh Security Configuration Assessment.

Assessment evidence supports:

- baseline compliance review
- control-effectiveness analysis
- configuration hardening
- drift identification
- remediation prioritization

## Configuration Drift Detection

The workflow establishes SHA-256 configuration baselines and compares monitored assets against their approved state.

Drift classifications include:

- Compliant
- Drift Detected
- Missing

A controlled configuration modification was introduced to validate the detection workflow.

The change was identified as configuration drift, preserved as monitoring evidence, remediated, and revalidated against the approved baseline.

## Control Effectiveness

Control-effectiveness indicators are generated from measurable security signals rather than manual assertions.

Examples include:

- FIM operational status
- SCA operational status
- monitoring-stack availability
- monitoring-interface availability
- configuration baseline integrity

Results are exported as JSON and CSV for dashboarding, evidence review, and governance reporting.

## Governance Metrics

The monitoring plan tracks ten governance-oriented metrics covering:

- unauthorized file changes
- configuration assessment failures
- Critical vulnerabilities
- High vulnerability exposure
- authentication anomalies
- monitoring availability
- configuration drift
- monitoring coverage
- open security findings
- residual monitoring risk

Each metric defines:

- monitoring source
- frequency
- threshold
- accountable owner
- escalation requirement

## Automated Evidence Collection

The metric collector produces machine-readable JSON evidence describing:

- Wazuh service health
- required network listeners
- FIM execution evidence
- SCA execution evidence
- controlled-asset state
- overall continuous-monitoring health

This allows governance conclusions to remain traceable to technical telemetry.

## Executive Reporting

The reporting pipeline automatically creates a monthly continuous-monitoring report for risk and authorization stakeholders.

The report summarizes:

- monitoring-platform status
- control-effectiveness indicators
- monitoring cadence
- residual monitoring risk
- escalation conditions
- authorization decision-support considerations

Continuous monitoring is treated as an input into risk and authorization decisions rather than as a replacement for formal security assessments.

## Dashboard Design

The dashboard specification organizes security telemetry into governance-focused views:

- platform health
- control effectiveness
- file integrity events
- security configuration assessment
- configuration drift
- vulnerability exposure
- remediation status
- residual risk

The executive view prioritizes material changes that could affect the authorization decision.

## Evidence Integrity

Evidence artifacts are protected with SHA-256 manifests so modifications can be detected during later review.

Example validation:

    sha256sum -c evidence-manifest.sha256

This provides integrity verification without presenting a checksum as a cryptographic identity signature.

## Repository Structure

    continuous-security-monitoring/
    ├── automation/
    │   ├── build-dashboard-data.py
    │   ├── collect-conmon-metrics.py
    │   ├── detect-configuration-drift.py
    │   └── generate-monthly-report.py
    ├── configuration/
    │   ├── conmon-monitoring-plan.csv
    │   └── conmon-policy.md
    ├── dashboard/
    │   ├── conmon-dashboard.md
    │   ├── configuration-drift.csv
    │   ├── configuration-drift.json
    │   ├── control-effectiveness.csv
    │   └── control-effectiveness.json
    ├── evidence-samples/
    │   ├── drift-test-summary.md
    │   ├── final-conmon-metrics.json
    │   └── post-remediation-drift-check.json
    ├── reports/
    │   ├── conmon-executive-summary.md
    │   └── monthly-conmon-report-YYYY-MM.md
    ├── .gitignore
    └── README.md

## Engineering Decisions

Several implementation choices were deliberate:

- monitoring frequencies are risk-driven instead of blindly accepting product defaults
- sensitive content is excluded from FIM difference reporting
- operational telemetry is separated from governance decisions
- configuration drift is validated through repeatable baseline comparison
- evidence integrity is independently verifiable
- executive reporting emphasizes changes in risk rather than raw alert volume
- monitoring results feed remediation and authorization workflows

## Technologies

- Wazuh
- OpenSearch-based Wazuh Indexer
- Filebeat
- Linux
- Python
- CIS Benchmarks
- SHA-256
- JSON
- CSV
- continuous monitoring
- configuration management
- security governance

## Security and Governance Outcomes

This implementation demonstrates the ability to bridge security operations and governance by converting live technical evidence into:

- control-effectiveness measurements
- configuration-management evidence
- remediation signals
- risk indicators
- monitoring trends
- authorization decision support

That connection between operational telemetry and risk governance is the core objective of the workflow.
