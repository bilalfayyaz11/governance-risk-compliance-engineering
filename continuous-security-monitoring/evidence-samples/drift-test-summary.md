# Configuration Drift Validation

## Objective

Validate that unauthorized or unexpected modification of a monitored configuration asset is detectable through the continuous-monitoring workflow.

## Test Asset

/opt/conmon/critical-files/application.conf

## Test Method

A controlled configuration change was introduced after establishing a SHA-256 baseline.

The test changed:

logging=enabled

to:

logging=disabled

## Detection Mechanisms

The workflow validates drift using:

- Wazuh File Integrity Monitoring
- SHA-256 configuration baseline comparison
- configuration-drift automation
- retained monitoring evidence

## Expected Result

The modified configuration should be identified as:

Drift Detected

The evidence should support investigation, remediation, and risk escalation where required.

## Governance Use

Validated configuration-drift detection supports:

- continuous monitoring
- configuration management
- security control effectiveness assessment
- incident triage
- remediation tracking
- authorization decision support
