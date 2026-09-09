# BCM and Disaster Recovery Control Testing

A hands-on business continuity and disaster recovery implementation that validates whether a stateful containerized workload can meet defined recovery objectives through encrypted backups, near-real-time replication, automated failover, tabletop testing, and evidence-driven control assessment.

## Overview

This implementation simulates a critical transaction-processing service running on a single Linux host.

The environment includes:

- containerized stateful workload
- persistent SQLite transaction database
- continuous synthetic transactions
- Business Impact Analysis
- encrypted restic backups
- rsync-based secondary replication
- automated failover
- tabletop disaster exercise
- destructive live recovery test
- measured RTO and RPO
- independent restic restore validation
- POA&M-style deficiency tracking
- NIST SP 800-53 CP-family control mapping

## Recovery Objectives

The Business Impact Analysis derives the following targets:

| Metric | Target |
|---|---:|
| Recovery Time Objective | 15 minutes |
| Recovery Point Objective | 5 minutes |
| Maximum Tolerable Downtime | 4 hours |

These values are tied directly to financial, operational, reputational, and regulatory impact over increasing outage durations.

## Architecture

    Primary Transaction Workload
             |
             | Persistent SQLite Data
             v
       workload/data/
          /       \
         /         \
        v           v
    restic        rsync
    encrypted     replication
    backups           |
        |             v
        |      backups-secondary/
        |             |
        |             v
        |       Failover Container
        |             |
        +-------------+
              |
              v
        Recovery Testing

Primary service:

    127.0.0.1:8080

Failover service:

    127.0.0.1:8081

## Stateful Workload

The workload is a lightweight Python HTTP service backed by SQLite.

Endpoints include:

    /health
    /transactions

Application data is stored outside the container through a persistent mount so that container lifecycle events do not destroy business data.

Synthetic transaction generation continuously inserts timestamped records into the database.

## Business Impact Analysis

The BIA evaluates outage impact across:

- 1 hour
- 4 hours
- 24 hours
- 72 hours

Impact dimensions include:

- financial
- operational
- reputational
- regulatory

The increasing impact profile resulted in:

    RTO = 15 minutes
    RPO = 5 minutes
    MTD = 4 hours

The recovery objectives therefore drive the technical backup, replication, and failover design.

## Encrypted Backup

restic provides encrypted and deduplicated historical backups of workload data.

Capabilities implemented:

- encrypted repository
- incremental snapshots
- workload tagging
- timestamp tagging
- execution logging
- repository integrity validation
- independent recovery testing

Backup cadence:

    Every 5 minutes

This cadence aligns with the five-minute RPO.

## Secondary Replication

rsync maintains a secondary recovery copy of workload data.

Replication behavior includes:

- archive mode
- checksum-based comparison
- delete-after synchronization
- structured JSON logging
- scheduled execution

Replication cadence:

    Every 5 minutes

The secondary replica provides the preferred recovery path because the data is already staged and does not require a full backup restore before service reconstitution.

## Automated Failover

The failover workflow:

1. records recovery start time
2. stops the primary workload
3. starts a secondary container
4. mounts replicated recovery data
5. performs HTTP health validation
6. validates recovered transactions
7. records recovery completion
8. calculates actual RTO

The failover process is designed to remain below the approved 15-minute RTO.

## Tabletop Exercise

A structured disaster scenario simulates primary storage corruption.

The exercise evaluates:

- detection
- escalation
- disaster declaration
- RACI responsibilities
- recovery-path selection
- failover authorization
- stakeholder communication
- RTO/RPO decision-making

The exercise identified several meaningful weaknesses rather than assuming control effectiveness.

Key findings include:

- delayed incident detection
- primary and secondary storage sharing a common host
- corruption or deletion potentially propagating through replication
- manual disaster declaration
- application-consistency concerns during live SQLite copies

## Destructive Recovery Test

The functional recovery exercise intentionally removes primary workload data after creating a controlled known-good recovery point.

The test validates:

- primary failure simulation
- secondary service activation
- HTTP service recovery
- transaction recovery
- checksum comparison
- measured RTO
- measured RPO
- independent backup restoration

Recovery evidence is captured under:

    docs/evidence/

## Independent Restic Recovery

The latest restic snapshot is restored separately from the replicated failover path.

This demonstrates that recovery does not depend entirely on the continuously synchronized secondary copy.

The separate recovery path helps address scenarios such as:

- deletion propagated to replica
- corruption replicated from production
- recovery to an earlier historical state
- loss of the secondary copy

## Control Assessment

### CP-2 — Contingency Plan

Evidence includes:

- Business Impact Analysis
- recovery objectives
- roles and responsibilities
- recovery strategy
- communication planning
- BCP/DRP updates

Assessment:

    Implemented with findings

### CP-4 — Contingency Plan Testing

Evidence includes:

- tabletop exercise
- destructive failover
- recovery timing
- service validation
- recorded test evidence

Assessment:

    Tested successfully with findings

### CP-9 — System Backup

Evidence includes:

- encrypted restic repository
- scheduled backups
- snapshot history
- repository integrity validation
- successful restore

Assessment:

    Operational with findings

### CP-10 — System Recovery and Reconstitution

Evidence includes:

- secondary replication
- automated failover
- service reconstitution
- transaction validation
- measured RTO/RPO

Assessment:

    Successfully demonstrated in the controlled environment

## Key Deficiencies

The assessment identified several risks requiring remediation before production reliance.

### Shared Failure Domain

Primary data, replicated recovery data, and backups reside on the same VM.

Production recovery infrastructure should use independent failure domains.

### Replicated Corruption

Near-real-time synchronization can propagate destructive changes to the recovery copy.

Versioned and immutable recovery mechanisms should remain independent from replication.

### Detection Delay

Delayed detection can consume the recovery objective before failover begins.

Production environments require automated availability monitoring and explicit RTO clock-start criteria.

### SQLite Consistency

Filesystem-level copying of an actively changing SQLite database is weaker than an application-consistent backup mechanism.

A production implementation should use SQLite's backup API, checkpointing, or another controlled snapshot process.

### Backup Credential Placement

The backup password and repository exist on the same host in this simulated environment.

Production implementations should separate backup credentials through dedicated secrets management.

## Evidence and Documentation

    docs/
    ├── bia.md
    ├── bcp-updates.md
    ├── control-mapping.md
    ├── deficiency-log.md
    ├── recovery-design.md
    ├── tabletop-results.md
    ├── tabletop-scenario.md
    ├── technical-failover-results.md
    ├── test-plan.md
    ├── test-results.md
    └── evidence/

## Automation

    scripts/
    ├── backup.sh
    ├── failover.sh
    ├── generate_transaction.sh
    └── replicate.sh

Sensitive runtime artifacts such as backup passwords are not intended for source control.

## Skills Demonstrated

- Business Continuity Management
- Disaster Recovery
- Business Impact Analysis
- RTO / RPO / MTD design
- Docker
- Linux
- SQLite
- restic
- rsync
- shell automation
- scheduled recovery controls
- backup and restore validation
- failover engineering
- disaster-recovery testing
- evidence collection
- POA&M-style deficiency management
- NIST SP 800-53 CP-family control assessment
- governance, risk, and compliance engineering

## Outcome

This implementation demonstrates the full control lifecycle:

    business impact
        -> recovery objectives
        -> technical control design
        -> implementation
        -> tabletop exercise
        -> destructive recovery testing
        -> evidence collection
        -> control assessment
        -> deficiency tracking
        -> BCP/DRP improvement

The final assessment is intentionally not represented as perfect compliance.

The recovery mechanisms function successfully in the controlled environment, while documented deficiencies identify the architectural and operational improvements required before production deployment.
