# Continuous Monitoring Dashboard

## Purpose

Provide operational and governance visibility into security-control effectiveness, configuration drift, monitoring coverage, and changes in system risk.

## Executive Scorecards

### Monitoring Platform Health

Display:

- Wazuh Indexer state
- Wazuh Manager state
- Filebeat state
- Wazuh Dashboard state
- Manager API availability
- monitoring interface availability

Target:

All required components operational.

## Control Effectiveness

Visualize control-effectiveness status by capability.

Required fields:

- control family
- capability
- monitoring metric
- status
- monitoring frequency
- evidence source

Status categories:

- Effective
- Degraded

Recommended visualization:

Horizontal status table plus effective/degraded count.

## File Integrity Monitoring

Display:

- FIM events over time
- monitored critical assets
- new files
- modified files
- deleted files
- high-value configuration changes

Priority paths:

- /etc
- /boot
- /usr/bin
- /usr/sbin
- /bin
- /sbin
- /opt/conmon/critical-files

## Security Configuration Assessment

Display:

- SCA policy
- passed checks
- failed checks
- score trend
- latest assessment time

Primary policy:

CIS Ubuntu 24.04.

## Configuration Drift

Display:

- assets checked
- compliant assets
- drifted assets
- missing assets
- baseline hash
- current hash
- last verification time

Status categories:

- Compliant
- Drift Detected
- Missing

Any drift affecting a security-relevant configuration must be investigated.

## Vulnerability Risk

Display:

- Critical vulnerabilities
- High vulnerabilities
- vulnerability trend
- affected assets
- remediation aging

Critical vulnerabilities require priority escalation.

## Governance Metrics

Display:

- monitoring coverage
- overdue findings
- unresolved High/Critical findings
- POA&M aging
- current residual monitoring risk

## AO View

The Authorizing Official view should prioritize:

1. residual risk
2. control degradation
3. Critical/High vulnerabilities
4. configuration drift
5. monitoring coverage loss
6. overdue remediation
7. material changes since previous reporting period

The dashboard supports decision-making but does not itself constitute an authorization decision.
